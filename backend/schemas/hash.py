from enum import Enum

from pydantic import BaseModel, Field


class HashAlgorithm(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"
    sha512 = "sha512"
    sha3_256 = "sha3_256"
    sha3_512 = "sha3_512"
    blake2b = "blake2b"
    blake2s = "blake2s"


class OutputFormat(str, Enum):
    hex = "hex"
    base64 = "base64"


class HashGenerateRequest(BaseModel):
    data: str = Field(..., description="Data to be hashed")
    algorithm: HashAlgorithm = Field(
        default=HashAlgorithm.sha256, description="Hash algorithm"
    )
    hmac_key: str | None = Field(default=None, description="HMAC key (optional)")
    output_format: OutputFormat = Field(
        default=OutputFormat.hex, description="Output format (hex or base64)"
    )


class HashGenerateResponse(BaseModel):
    hash: str
    algorithm: HashAlgorithm
    format: OutputFormat


class HashVerifyRequest(BaseModel):
    data: str = Field(..., description="Data to be verified")
    expected_hash: str = Field(..., description="Expected hash")
    algorithm: HashAlgorithm = Field(..., description="Hash algorithm")
    hmac_key: str | None = Field(default=None, description="HMAC key (optional)")
    output_format: OutputFormat | None = Field(
        default=None, description="Output format (auto-detect if not specified)"
    )


class HashVerifyResponse(BaseModel):
    valid: bool = Field(..., description="Whether the hash is valid")
    algorithm: HashAlgorithm
