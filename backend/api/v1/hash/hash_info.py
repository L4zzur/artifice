from fastapi import APIRouter

router = APIRouter()


@router.get("/algorithms")
async def list_algorithms():
    """
    List all supported hash algorithms with details

    Returns information about output length, security level,
    and recommended use cases for each algorithm.
    """
    return {
        "algorithms": [
            {
                "name": "md5",
                "output_bits": 128,
                "output_hex_length": 32,
                "output_base64_length": 24,
                "security": "Legacy",
                "description": "Fast but cryptographically broken. "
                "Use only for checksums.",
                "recommended": False,
            },
            {
                "name": "sha1",
                "output_bits": 160,
                "output_hex_length": 40,
                "output_base64_length": 28,
                "security": "Deprecated",
                "description": "Collision attacks exist. "
                "Avoid for security-critical applications.",
                "recommended": False,
            },
            {
                "name": "sha256",
                "output_bits": 256,
                "output_hex_length": 64,
                "output_base64_length": 44,
                "security": "Strong",
                "description": "Industry standard. "
                "Excellent balance of security and performance.",
                "recommended": True,
            },
            {
                "name": "sha512",
                "output_bits": 512,
                "output_hex_length": 128,
                "output_base64_length": 88,
                "security": "Very Strong",
                "description": "High security for sensitive data. Slower than SHA-256.",
                "recommended": True,
            },
            {
                "name": "sha3_256",
                "output_bits": 256,
                "output_hex_length": 64,
                "output_base64_length": 44,
                "security": "Strong",
                "description": "SHA-3 (Keccak) family. Modern alternative to SHA-2.",
                "recommended": True,
            },
            {
                "name": "sha3_512",
                "output_bits": 512,
                "output_hex_length": 128,
                "output_base64_length": 88,
                "security": "Very Strong",
                "description": "SHA-3 with 512-bit output. High security applications.",
                "recommended": True,
            },
            {
                "name": "blake2b",
                "output_bits": 512,
                "output_hex_length": 128,
                "output_base64_length": 88,
                "security": "Very Strong",
                "description": "Faster than SHA-2/SHA-3. Modern and secure.",
                "recommended": True,
            },
            {
                "name": "blake2s",
                "output_bits": 256,
                "output_hex_length": 64,
                "output_base64_length": 44,
                "security": "Strong",
                "description": "Optimized for 8-32 bit platforms. Fast and secure.",
                "recommended": True,
            },
        ]
    }
