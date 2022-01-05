package org.ctfcracktools.fuction

class CodeMode {
    companion object{
        const val CRYPTO_FENCE = "Fence"
        const val CRYPTO_CAESAR = "CaesarCode"
        const val CRYPTO_PIG = "PigCode"
        const val CRYPTO_ROT13 = "ROT13"
        const val CRYPTO_HEX_2_STRING = "Hex2String"
        const val CRYPTO_STRING_2_HEX = "String2Hex"
        const val CRYPTO_UNICODE_2_ASCII = "Unicode2Ascii"
        const val CRYPTO_ASCII_2_UNICODE = "Ascii2Unicode"
        const val CRYPTO_REVERSE = "Reverse"

        const val DECODE_MORSE = "MorseDecode"
        const val DECODE_BACON = "BaconDecode"
        const val DECODE_BASE64 = "Base64Decode"
        const val DECODE_BASE32 = "BASE32Decode"
        const val DECODE_URL = "UrlDecode"
        const val DECODE_UNICODE = "UnicodeDecode"
        const val DECODE_HTML = "HtmlDecode"
        const val DECODE_VIGENERE = "VigenereDeCode"

        const val ENCODE_MORSE = "MorseEncode"
        const val ENCODE_BACON = "BaconEncode"
        const val ENCODE_BASE64 = "Base64Encode"
        const val ENCODE_BASE32 = "Base32Encode"
        const val ENCODE_URL = "UrlEncode"
        const val ENCODE_UNICODE = "UnicodeEncode"
        const val ENCODE_HTML = "HtmlEncode"
        const val ENCODE_VIGENERE = "VigenereEnCode"
    }
}