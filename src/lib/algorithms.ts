/**
 * Algorithm definitions for the workflow editor
 */

export interface AlgorithmDef {
  value: string;
  label: string;
  icon: string;
}

export interface AlgorithmGroup {
  name: string;
  icon: string;
  algorithms: AlgorithmDef[];
}

// Single source of truth for all algorithms
export const ALGORITHM_GROUPS: AlgorithmGroup[] = [
  {
    name: "Encoding",
    icon: "E",
    algorithms: [
      { value: "base64", label: "Base64", icon: "64" },
      { value: "base32", label: "Base32", icon: "32" },
      { value: "base58", label: "Base58", icon: "58" },
      { value: "base85", label: "Base85", icon: "85" },
      { value: "hex", label: "Hex", icon: "0x" },
      { value: "url", label: "URL", icon: "%" },
      { value: "ascii", label: "ASCII", icon: "A" },
      { value: "binary", label: "Binary", icon: "01" },
      { value: "morse", label: "Morse", icon: "·-" },
      { value: "uuencode", label: "UUEncode", icon: "UU" },
      { value: "rot47", label: "ROT47", icon: "47" },
      { value: "unicode", label: "Unicode", icon: "U+" },
      { value: "html_entity", label: "HTML Entity", icon: "&" },
      { value: "jwt", label: "JWT Decode", icon: "JW" },
      { value: "brainfuck", label: "Brainfuck", icon: "BF" },
    ],
  },
  {
    name: "Cipher",
    icon: "C",
    algorithms: [
      { value: "rot13", label: "ROT13", icon: "R" },
      { value: "caesar", label: "Caesar", icon: "C" },
      { value: "vigenere", label: "Vigenère", icon: "V" },
      { value: "atbash", label: "Atbash", icon: "AZ" },
      { value: "railfence", label: "RailFence", icon: "RF" },
      { value: "bacon", label: "Bacon", icon: "AB" },
      { value: "xor", label: "XOR", icon: "^" },
      { value: "playfair", label: "Playfair", icon: "PF" },
      { value: "polybius", label: "Polybius", icon: "PO" },
      { value: "affine", label: "Affine", icon: "AF" },
      { value: "beaufort", label: "Beaufort", icon: "BT" },
    ],
  },
  {
    name: "Crypto",
    icon: "K",
    algorithms: [
      { value: "aes", label: "AES-128", icon: "AE" },
      { value: "rc4", label: "RC4", icon: "R4" },
      { value: "des", label: "DES", icon: "DE" },
      { value: "3des", label: "3DES", icon: "3D" },
      { value: "blowfish", label: "Blowfish", icon: "BF" },
    ],
  },
  {
    name: "Hash",
    icon: "H",
    algorithms: [
      { value: "md5", label: "MD5", icon: "#" },
      { value: "sha1", label: "SHA1", icon: "S1" },
      { value: "sha256", label: "SHA256", icon: "S2" },
      { value: "sha512", label: "SHA512", icon: "S5" },
      { value: "hmac_sha256", label: "HMAC-SHA256", icon: "HM" },
      { value: "pbkdf2", label: "PBKDF2", icon: "PB" },
    ],
  },
  {
    name: "Text",
    icon: "T",
    algorithms: [
      { value: "uppercase", label: "Uppercase", icon: "UP" },
      { value: "lowercase", label: "Lowercase", icon: "lo" },
      { value: "reverse", label: "Reverse", icon: "↔" },
      { value: "trim", label: "Trim", icon: "T" },
      { value: "capitalize", label: "Capitalize", icon: "Aa" },
      { value: "swap_case", label: "SwapCase", icon: "aA" },
      { value: "length", label: "Length", icon: "Ln" },
    ],
  },
];

// Single-operation algorithms (no decode button needed)
export const SINGLE_OPERATIONS = new Set([
  "md5", "sha1", "sha256", "sha512", "hmac_sha256", "pbkdf2",
  "uppercase", "lowercase", "reverse", "trim",
  "capitalize", "swap_case", "length", "remove_spaces",
]);

// Get button label based on algorithm type
export function getButtonLabel(algorithm: string): string {
  if (["md5", "sha1", "sha256", "sha512", "hmac_sha256", "pbkdf2"].includes(algorithm)) return "Hash";
  if (SINGLE_OPERATIONS.has(algorithm)) return "Run";
  return "Enc";
}

// Check if algorithm is single operation
export function isSingleOperation(algorithm: string): boolean {
  return SINGLE_OPERATIONS.has(algorithm);
}
