from logging import getLogger

from fastapi import APIRouter, HTTPException

from schemas.error import ErrorResponse
from schemas.password import (
    PasswordAnalyzeRequest,
    PasswordAnalyzeResponse,
    PasswordGenerateRequest,
    PasswordGenerateResponse,
)
from services.exceptions import ServiceError
from services.password import PasswordGeneratorService

router = APIRouter(prefix="/password")

logger = getLogger(__name__)


@router.post(
    "/generate",
    response_model=PasswordGenerateResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def generate_password(request: PasswordGenerateRequest):
    """
    Generate secure password with realistic strength analysis

    Uses the industry-standard zxcvbn (Dropbox) library to provide realistic password
    strength estimates that account for:

    - **Dictionary attacks**: Common words, names, places
    - **Keyboard patterns**: qwerty, asdfgh, etc.
    - **l33t speak**: P@ssw0rd, h4ck3r, etc.
    - **Repeating characters**: aaaa, 1111, etc.
    - **Sequences**: abcd, 1234, etc.
    - **Common passwords**: password123, admin, etc.

    ## Strength Scoring (0-4)

    - **0 (Very Weak)**: Cracked instantly
    - **1 (Weak)**: Cracked in seconds to minutes
    - **2 (Fair)**: Cracked in hours to days
    - **3 (Strong)**: Cracked in months to years
    - **4 (Very Strong)**: Cracked in centuries or never

    ## Example Response:

    ```
    {
        "password": "aB3!dF7&hK9@mN2$",
        "strength": {
            "strength": "very_strong",
            "score": 4,
            "guesses": 1000000000000,
            "guesses_log10": 12.0,
            "crack_times": {
                "offline_fast_hashing": "3 months",
                "offline_slow_hashing": "centuries",
                "online_no_throttling": "centuries",
                "online_throttling": "centuries"
            },
            "feedback": {
                "warning": "",
                "suggestions": []
            }
        }
    }
    ```
    """
    try:
        result = PasswordGeneratorService.generate_password(
            length=request.length,
            uppercase=request.include_uppercase,
            lowercase=request.include_lowercase,
            numbers=request.include_numbers,
            symbols=request.include_symbols,
            similar=request.include_similar,
        )
        return PasswordGenerateResponse(
            password=result["password"],
            strength=result["strength"],
        )
    except ServiceError as e:
        logger.warning("Password generation error: %s", e.message)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": e.code,
                "message": e.message,
                "context": e.context,
            },
        )
    except Exception:
        logger.exception("Unexpected error during password generation")
        raise HTTPException(
            status_code=500,
            detail="Internal password generation error",
        )


@router.post(
    "/analyze",
    response_model=PasswordAnalyzeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
async def analyze_password(request: PasswordAnalyzeRequest):
    try:
        result = PasswordGeneratorService.analyze_strength(request.password)
        return PasswordAnalyzeResponse(info=result)
    except ServiceError as e:
        logger.warning("Password analysis error: %s", e.message)
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "code": e.code,
                "message": e.message,
                "context": e.context,
            },
        )
    except Exception:
        logger.exception("Unexpected error during password analysis")
        raise HTTPException(
            status_code=500,
            detail="Internal password analysis error",
        )
