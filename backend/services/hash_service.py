import base64
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
