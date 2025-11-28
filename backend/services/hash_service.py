import base64
import binascii
import hashlib
import hmac

from schemas.hash import OutputFormat
from services.exceptions import ServiceError


class HashService:

    @staticmethod
    def generate_hash(
        data: str,
        algorithm: str,
        output_format: str,
        hmac_key: str | None = None,
    ) -> dict:
        data_bytes = data.encode("utf-8")
        try:
            if hmac_key:
                hash_func = getattr(hashlib, algorithm)
                digest = hmac.new(
                    hmac_key.encode("utf-8"),
                    data_bytes,
                    hash_func,
                ).digest()
            else:
                digest = hashlib.new(algorithm, data_bytes).digest()

            if output_format == OutputFormat.base64:
                hash_value = base64.b64encode(digest).decode()
            else:
                hash_value = digest.hex()

            return {"hash": hash_value, "algorithm": algorithm, "format": output_format}

        except ValueError as e:
            raise ServiceError(
                code="unknown_algorithm",
                message=f"Unknown hash algorithm: {algorithm}",
                status_code=400,
                context={"error": str(e)},
            )
        except AttributeError:
            raise ServiceError(
                code="unsupported_algorithm",
                message=f"Unsupported algorithm: {algorithm}",
                status_code=400,
            )

    @staticmethod
    def _detect_format(hash_str: str) -> OutputFormat:
        if all(c in "0123456789abcdefABCDEF" for c in hash_str):
            return OutputFormat.hex
        try:
            base64.b64decode(hash_str, validate=True)
            return OutputFormat.base64
        except (ValueError, binascii.Error):
            raise ServiceError(
                code="invalid_hash_format",
                message="Cannot detect hash format",
                status_code=400,
            )

    @staticmethod
    def verify_hash(
        data: str,
        expected_hash: str,
        algorithm: str,
        output_format: str | None,
        hmac_key: str | None,
    ) -> dict:
        if not output_format:
            output_format = HashService._detect_format(expected_hash)

        generated_hash = HashService.generate_hash(
            data, algorithm, output_format, hmac_key
        )
        is_valid = hmac.compare_digest(generated_hash["hash"], expected_hash)

        return {
            "valid": is_valid,
            "algorithm": algorithm,
        }
