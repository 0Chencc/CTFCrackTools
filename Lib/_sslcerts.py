import logging
import sys
import uuid
from array import array
from contextlib import closing
from StringIO import StringIO

from java.io import BufferedInputStream, BufferedReader, FileReader, InputStreamReader, ByteArrayInputStream
from java.security import KeyStore, Security
from java.security.cert import CertificateException, CertificateFactory
from javax.net.ssl import (
    X509KeyManager, X509TrustManager, KeyManagerFactory, SSLContext, TrustManager, TrustManagerFactory)

try:
    # jarjar-ed version
    from org.python.bouncycastle.asn1.pkcs import PrivateKeyInfo
    from org.python.bouncycastle.cert import X509CertificateHolder
    from org.python.bouncycastle.cert.jcajce import JcaX509CertificateConverter
    from org.python.bouncycastle.jce.provider import BouncyCastleProvider
    from org.python.bouncycastle.openssl import PEMKeyPair, PEMParser
    from org.python.bouncycastle.openssl.jcajce import JcaPEMKeyConverter
except ImportError:
    # dev version from extlibs
    from org.bouncycastle.asn1.pkcs import PrivateKeyInfo
    from org.bouncycastle.cert import X509CertificateHolder
    from org.bouncycastle.cert.jcajce import JcaX509CertificateConverter
    from org.bouncycastle.jce.provider import BouncyCastleProvider
    from org.bouncycastle.openssl import PEMKeyPair, PEMParser
    from org.bouncycastle.openssl.jcajce import JcaPEMKeyConverter


log = logging.getLogger("_socket")
Security.addProvider(BouncyCastleProvider())



def _get_ca_certs_trust_manager(ca_certs):
    trust_store = KeyStore.getInstance(KeyStore.getDefaultType())
    trust_store.load(None, None)
    num_certs_installed = 0
    with open(ca_certs) as f:
        cf = CertificateFactory.getInstance("X.509")
        for cert in cf.generateCertificates(BufferedInputStream(f)):
            trust_store.setCertificateEntry(str(uuid.uuid4()), cert)
            num_certs_installed += 1
    tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm())
    tmf.init(trust_store)
    log.debug("Installed %s certificates", num_certs_installed, extra={"sock": "*"})
    return tmf


def _stringio_as_reader(s):
    return BufferedReader(InputStreamReader(ByteArrayInputStream(bytearray(s.getvalue()))))


def _extract_readers(cert_file):
    private_key = StringIO()
    certs = StringIO()
    output = certs
    with open(cert_file) as f:
        for line in f:
            if line.startswith("-----BEGIN PRIVATE KEY-----"):
                output = private_key
            output.write(line)
            if line.startswith("-----END PRIVATE KEY-----"):
                output = certs
    return _stringio_as_reader(private_key), _stringio_as_reader(certs)


def _get_openssl_key_manager(cert_file, key_file=None):
    paths = [key_file] if key_file else []
    paths.append(cert_file)

    # Go from Bouncy Castle API to Java's; a bit heavyweight for the Python dev ;)
    key_converter = JcaPEMKeyConverter().setProvider("BC")
    cert_converter = JcaX509CertificateConverter().setProvider("BC")

    private_key = None
    certs = []
    for path in paths:
        for br in _extract_readers(path):
            while True:
                obj = PEMParser(br).readObject()
                if obj is None:
                    break
                if isinstance(obj, PEMKeyPair):
                    private_key = key_converter.getKeyPair(obj).getPrivate()
                elif isinstance(obj, PrivateKeyInfo):
                    private_key = key_converter.getPrivateKey(obj)
                elif isinstance(obj, X509CertificateHolder):
                    certs.append(cert_converter.getCertificate(obj))

    if not private_key:
        from _socket import SSLError, SSL_ERROR_SSL
        raise SSLError(SSL_ERROR_SSL, "No private key loaded")
    key_store = KeyStore.getInstance(KeyStore.getDefaultType())
    key_store.load(None, None)
    key_store.setKeyEntry(str(uuid.uuid4()), private_key, [], certs)
    kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm())
    kmf.init(key_store, [])
    return kmf


def _get_ssl_context(keyfile, certfile, ca_certs):
    if certfile is None and ca_certs is None:
        log.debug("Using default SSL context", extra={"sock": "*"})
        return SSLContext.getDefault()
    else:
        log.debug("Setting up a specific SSL context for keyfile=%s, certfile=%s, ca_certs=%s",
                  keyfile, certfile, ca_certs, extra={"sock": "*"})
        if ca_certs:
            # should support composite usage below
            trust_managers = _get_ca_certs_trust_manager(ca_certs).getTrustManagers()
        else:
            trust_managers = None
        if certfile:
            key_managers = _get_openssl_key_manager(certfile, keyfile).getKeyManagers()
        else:
            key_managers = None

        # FIXME FIXME for performance, cache this lookup in the future
        # to avoid re-reading files on every lookup
        context = SSLContext.getInstance("SSL")
        context.init(key_managers, trust_managers, None)
        return context


# CompositeX509KeyManager and CompositeX509TrustManager allow for mixing together Java built-in managers
# with new managers to support Python ssl.
#
# See http://tersesystems.com/2014/01/13/fixing-the-most-dangerous-code-in-the-world/
# for a good description of this composite approach.
#
# Ported to Python from http://codyaray.com/2013/04/java-ssl-with-multiple-keystores
# which was inspired by http://stackoverflow.com/questions/1793979/registering-multiple-keystores-in-jvm

class CompositeX509KeyManager(X509KeyManager):
                                                   
    def __init__(self, key_managers):
        self.key_managers = key_managers

    def chooseClientAlias(self, key_type, issuers, socket):
        for key_manager in self.key_managers:
            alias = key_manager.chooseClientAlias(key_type, issuers, socket)
            if alias:
                return alias;
        return None

    def chooseServerAlias(self, key_type, issuers, socket):
        for key_manager in self.key_managers:
            alias = key_manager.chooseServerAlias(key_type, issuers, socket)
            if alias:
                return alias;
        return None
    
    def getPrivateKey(self, alias):
        for key_manager in self.key_managers:
            private_key = keyManager.getPrivateKey(alias)
            if private_key:
                return private_key
        return None

    def getCertificateChain(self, alias):
        for key_manager in self.key_managers:
            chain = key_manager.getCertificateChain(alias)
            if chain:
                return chain
        return None

    def getClientAliases(self, key_type, issuers):
        aliases = []
        for key_manager in self.key_managers:
            aliases.extend(key_manager.getClientAliases(key_type, issuers))
        if not aliases:
            return None
        else:
            return aliases

    def getServerAliases(self, key_type, issuers):
        aliases = []
        for key_manager in self.key_managers:
            aliases.extend(key_manager.getServerAliases(key_type, issuers))
        if not aliases:
            return None
        else:
            return aliases


class CompositeX509TrustManager(X509TrustManager):

    def __init__(self, trust_managers):
        self.trust_managers = trust_managers

    def checkClientTrusted(self, chain, auth_type):
        for trust_manager in self.trust_managers:
            try:
                trustManager.checkClientTrusted(chain, auth_type);
                return
            except CertificateException:
                pass
        raise CertificateException("None of the TrustManagers trust this certificate chain")

    def checkServerTrusted(self, chain, auth_type):
        for trust_manager in self.trust_managers:
            try:
                trustManager.checkServerTrusted(chain, auth_type);
                return
            except CertificateException:
                pass
        raise CertificateException("None of the TrustManagers trust this certificate chain")

    def getAcceptedIssuers(self):
        certs = []
        for trust_manager in self.trust_managers:
            certs.extend(trustManager.getAcceptedIssuers())
        return certs
