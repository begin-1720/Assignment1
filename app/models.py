
from pydantic import BaseModel, Field, field_validator
from datetime import date
from enum import Enum

class PolicyType(str, Enum):
    Health  = "Health"
    Vehicle = "Vehicle"
    Life    = "Life"

class ClaimStatus(str, Enum):
    Pending  = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"

class PolicyholderCreate(BaseModel):
    
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="Full name of the policyholder"
    )
    policy_type: PolicyType = Field(
        ..., 
        description="One of: Health, Vehicle, Life"
    )
    sum_insured: float = Field(
        ..., 
        gt=0, 
        description="Sum insured must be positive"
    )

class ClaimCreate(BaseModel):
    
    policyholder_id: int = Field(
        ..., 
        ge=0, 
        description="Must refer to an existing policyholder"
    )
    date_filed: date = Field(
        ..., 
        description="Date the claim was filed (YYYY-MM-DD)"
    )
    amount: float = Field(
        ..., 
        gt=0, 
        description="Claim amount must be positive"
    )
    status: ClaimStatus = Field(
        default=ClaimStatus.Pending, 
        description="Current status of the claim"
    )

    @field_validator("date_filed")
    @classmethod
    def date_not_in_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("date_filed cannot be in the future")
        return v

class Policyholder(PolicyholderCreate):
    id: int = Field(
        ..., 
        ge=0, 
        description="Unique, non-negative policyholder ID"
    )

class Claim(ClaimCreate):
    id: int = Field(
        ..., 
        ge=0, 
        description="Unique, non-negative claim ID"
    )