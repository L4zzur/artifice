import secrets
import string

from zxcvbn import zxcvbn

from schemas.password import (
    CrackTimes,
    PasswordFeedback,
    PasswordStrength,
    PasswordStrengthInfo,
)
from services.exceptions import ServiceError


class PasswordGeneratorService:

    UPPERCASE = string.ascii_uppercase
    LOWERCASE = string.ascii_lowercase
    NUMBERS = string.digits
    SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    SIMILAR = "il1Lo0O"

    STRENGTH_MAP = {
        0: PasswordStrength.very_weak,
        1: PasswordStrength.weak,
        2: PasswordStrength.fair,
        3: PasswordStrength.strong,
        4: PasswordStrength.very_strong,
    }

    @classmethod
    def _build_charset(
        cls,
        uppercase: bool,
        lowercase: bool,
        numbers: bool,
        symbols: bool,
        similar: bool,
    ) -> str:
        charset = ""
        charset += cls.UPPERCASE if uppercase else ""
        charset += cls.LOWERCASE if lowercase else ""
        charset += cls.NUMBERS if numbers else ""
        charset += cls.SYMBOLS if symbols else ""
        charset += cls.SIMILAR if similar else ""
        return charset

    # Based on Dropbox's zxcvbn
    @classmethod
    def analyze_strength(cls, password: str) -> PasswordStrengthInfo:
        result = zxcvbn(password)

        crack_times = CrackTimes(
            offline_fast_hashing=result["crack_times_display"][
                "offline_fast_hashing_1e10_per_second"
            ],
            offline_slow_hashing=result["crack_times_display"][
                "offline_slow_hashing_1e4_per_second"
            ],
            online_no_throttling=result["crack_times_display"][
                "online_no_throttling_10_per_second"
            ],
            online_throttling=result["crack_times_display"][
                "online_throttling_100_per_hour"
            ],
        )

        feedback = PasswordFeedback(
            warning=result["feedback"]["warning"],
            suggestions=result["feedback"]["suggestions"],
        )

        return PasswordStrengthInfo(
            strength=cls.STRENGTH_MAP[result["score"]],
            score=result["score"],
            guesses=int(result["guesses"]),
            guesses_log10=result["guesses_log10"],
            crack_times=crack_times,
            feedback=feedback,
        )

    @classmethod
    def generate_password(
        cls,
        length: int,
        uppercase: bool = True,
        lowercase: bool = True,
        numbers: bool = True,
        symbols: bool = True,
        similar: bool = True,
    ) -> dict:
        charset = cls._build_charset(uppercase, lowercase, numbers, symbols, similar)

        if not charset:
            raise ServiceError(
                code="invalid_character_types",
                message="At least one character type must be enabled",
                status_code=400,
            )

        password = "".join(secrets.choice(charset) for _ in range(length))
        strength = cls.analyze_strength(password)

        return {
            "password": password,
            "strength": strength,
        }
