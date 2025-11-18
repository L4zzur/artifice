from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Error code (e.g., 'invalid_embedded_image')")
    message: str = Field(..., description="Human-readable error message")
    context: dict = Field(default_factory=dict, description="Additional error context")


class ErrorResponse(BaseModel):
    detail: ErrorDetail | str = Field(
        ...,
        description="Error details: object for custom errors, "
        "string for generic errors",
    )
