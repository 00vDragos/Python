from pydantic import BaseModel, Field, validator


class FibonacciRequest(BaseModel):
    n: int

    @validator("n")
    def validate_n(cls, value):
        if value < 0:
            raise ValueError("Valoarea lui n trebuie sa fie >= 0")
        if value > 1000:
            raise ValueError("Valoarea lui n nu poate fi mai mare de 1000")
        return value


class FactorialRequest(BaseModel):
    n: int

    @validator("n")
    def validate_n(cls, value):
        if value < 0:
            raise ValueError("Factorialul nu este definit pentru valori negative.")
        return value


class PowRequest(BaseModel):
    base: float = Field(..., description="Base number")
    exponent: float = Field(..., description="Exponent")


class LoginRequest(BaseModel):
    email: str
    password: str
