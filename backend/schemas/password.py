from enum import Enum

from pydantic import BaseModel, Field


class PasswordStrength(str, Enum):
    very_weak = "very_weak"  # 0
    weak = "weak"  # 1
    fair = "fair"  # 2
    strong = "strong"  # 3
    very_strong = "very_strong"  # 4


class CrackTimes(BaseModel):
    offline_fast_hashing: str = Field(
        ..., description="Offline attack, fast hashing (10B/sec)"
    )
    offline_slow_hashing: str = Field(
        ..., description="Offline attack, slow hashing (10K/sec)"
    )
    online_no_throttling: str = Field(
        ..., description="Online attack, no rate limiting (10/sec)"
    )
    online_throttling: str = Field(
        ..., description="Online attack, with rate limiting (100/hour)"
    )


class PasswordFeedback(BaseModel):
    warning: str = Field(default="", description="Warning about password weakness")
    suggestions: list[str] = Field(
        default_factory=list, description="Suggestions to improve password"
    )


class PasswordStrengthInfo(BaseModel):
    """Password strength analysis from zxcvbn"""

    strength: PasswordStrength = Field(
        ..., description="Overall password strength (0-4)"
    )
    score: int = Field(..., ge=0, le=4, description="Strength score from zxcvbn (0-4)")
    guesses: int = Field(..., description="Estimated guesses needed to crack")
    guesses_log10: float = Field(..., description="log10 of guesses")
    crack_times: CrackTimes = Field(
        ..., description="Time to crack in different scenarios"
    )
    feedback: PasswordFeedback = Field(
        ..., description="Suggestions to improve password"
    )


class PasswordGenerateRequest(BaseModel):
    length: int = Field(
        default=16,
        ge=4,
        le=128,
        description="Length of password to generate (4-128 characters)",
    )
    include_uppercase: bool = Field(
        default=True, description="Include uppercase letters (A-Z)"
    )
    include_lowercase: bool = Field(
        default=True, description="Include lowercase letters (a-z)"
    )
    include_numbers: bool = Field(default=True, description="Include numbers (0-9)")
    include_symbols: bool = Field(
        default=True, description="Include symbols (!@#$%^&*()_+-=[]{}|;:,.<>?)"
    )
    include_similar: bool = Field(
        default=False, description="Include similar characters (i, l, 1, L, o, 0, O)"
    )


class PasswordGenerateResponse(BaseModel):
    password: str = Field(..., description="Generated password")
    strength: PasswordStrengthInfo = Field(
        ..., description="Password strength analysis"
    )


class PasswordAnalyzeRequest(BaseModel):
    password: str = Field(..., max_length=128, description="Password to analyze")


class PasswordAnalyzeResponse(BaseModel):
    info: PasswordStrengthInfo = Field(..., description="Password strength analysis")
