from fastapi import APIRouter, HTTPException, Query
from typing import List

from .models import Policyholder, Claim, PolicyholderCreate, ClaimCreate
from .services import (
    create_policyholder, list_policyholders,
    create_claim, list_claims,
    claim_frequency, high_risk_policyholders,
    aggregate_by_policy_type,
    monthly_claims, average_claim_by_policy_type,
    highest_claim_of_all_time, pending_claims
)

router = APIRouter()

# ─── Policyholder Routes ────────────────────────────────
@router.post("/policyholders", response_model=Policyholder, status_code=201)
def api_create_policyholder(ph: PolicyholderCreate):
    try:
        return create_policyholder(ph)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    

@router.get("/policyholders", response_model=List[Policyholder])
def api_list_policyholders():
    return list_policyholders()


# ─── Claim Routes ───────────────────────────────────────
@router.post("/claims", response_model=Claim, status_code=201)
def api_create_claim(cl: ClaimCreate):
    try:
        return create_claim(cl)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/claims", response_model=List[Claim])
def api_list_claims():
    return list_claims()


# ─── Analytics Routes ──────────────────────────────────
@router.get("/claims/frequency")
def api_claim_frequency(policyholder_id: int = Query(...)):
    return claim_frequency(policyholder_id)

@router.get("/policyholders/high-risk", response_model=List[Policyholder])
def api_high_risk():
    return high_risk_policyholders()

@router.get("/claims/aggregate-by-policy-type")
def api_aggregate_by_policy_type():
    return aggregate_by_policy_type()


# ─── Reporting Routes ──────────────────────────────────
@router.get("/reports/monthly-claims")
def api_monthly_claims():
    return monthly_claims()

@router.get("/reports/average-claim-by-policy-type")
def api_average_by_policy_type():
    return average_claim_by_policy_type()

@router.get("/reports/highest-claim-of-all-time")
def api_highest_claim():
    return highest_claim_of_all_time()

@router.get("/reports/pending-claims", response_model=List[Claim])
def api_pending_claims():
    return pending_claims()