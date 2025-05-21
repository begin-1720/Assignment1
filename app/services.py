from datetime import date, timedelta
from typing import List, Dict

from .data import JSONRepository
from .models import Policyholder, Claim, ClaimStatus, PolicyholderCreate, ClaimCreate

# instantiate once
ph_repo = JSONRepository("policyholders.json", Policyholder)
cl_repo = JSONRepository("claims.json", Claim)




def create_policyholder(data: PolicyholderCreate) -> Policyholder:
    ph_list = ph_repo.load()
    next_id = max((p.id for p in ph_list), default=-1) + 1
    ph = Policyholder(id=next_id, **data.model_dump())
    ph_list.append(ph)
    ph_repo.save(ph_list)
    return ph


def list_policyholders() -> List[Policyholder]:
    return ph_repo.load()




def create_policyholder(data: PolicyholderCreate) -> Policyholder:
    ph_list = ph_repo.load()
    next_id = max((p.id for p in ph_list), default=-1) + 1
    ph = Policyholder(id=next_id, **data.model_dump())
    ph_list.append(ph)
    ph_repo.save(ph_list)
    return ph

def create_claim(data: ClaimCreate) -> Claim:
    ph_list = ph_repo.load()
    if not any(p.id == data.policyholder_id for p in ph_list):
        raise ValueError(f"No policyholder with id {data.policyholder_id}")
    cl_list = cl_repo.load()
    next_id = max((c.id for c in cl_list), default=-1) + 1
    cl = Claim(id=next_id, **data.model_dump())
    cl_list.append(cl)
    cl_repo.save(cl_list)
    return cl

def list_claims() -> List[Claim]:
    return cl_repo.load()


# ─── Analytics Services ──────────────────────────────────

def claim_frequency(policyholder_id: int) -> Dict[str, int]:
    cl_list = cl_repo.load()
    freq = sum(1 for c in cl_list if c.policyholder_id == policyholder_id)
    return {"policyholder_id": policyholder_id, "claim_count": freq}

def high_risk_policyholders() -> List[Policyholder]:
    ph_list = ph_repo.load()
    cl_list = cl_repo.load()
    one_year_ago = date.today() - timedelta(days=365)

    high_risk: List[Policyholder] = []
    for ph in ph_list:
        recent = [
            c for c in cl_list
            if c.policyholder_id == ph.id and c.date_filed >= one_year_ago
        ]
        total_all = sum(c.amount for c in cl_list if c.policyholder_id == ph.id)
        if len(recent) > 3 or total_all > 0.8 * ph.sum_insured:
            high_risk.append(ph)
    return high_risk

def aggregate_by_policy_type() -> Dict[str, Dict[str, float]]:
    ph_list = ph_repo.load()
    cl_list = cl_repo.load()
    agg: Dict[str, Dict[str, float]] = {}
    for c in cl_list:
        pt = next((p.policy_type for p in ph_list if p.id == c.policyholder_id), None)
        if not pt:
            continue
        agg.setdefault(pt, {"count": 0, "total_amount": 0.0})
        agg[pt]["count"] += 1
        agg[pt]["total_amount"] += c.amount
    return agg


# ─── Reporting Services ──────────────────────────────────

def monthly_claims() -> Dict[str, int]:
    cl_list = cl_repo.load()
    by_month: Dict[str, int] = {}
    for c in cl_list:
        m = c.date_filed.strftime("%Y-%m")
        by_month[m] = by_month.get(m, 0) + 1
    return by_month

def average_claim_by_policy_type() -> Dict[str, float]:
    ph_list = ph_repo.load()
    cl_list = cl_repo.load()
    sums: Dict[str, float] = {}
    counts: Dict[str, int] = {}
    for c in cl_list:
        pt = next((p.policy_type for p in ph_list if p.id == c.policyholder_id), None)
        if not pt:
            continue
        sums[pt] = sums.get(pt, 0.0) + c.amount
        counts[pt] = counts.get(pt, 0) + 1
    return {pt: sums[pt] / counts[pt] for pt in sums}

def highest_claim_of_all_time() -> Dict:
    cl_list = cl_repo.load()
    if not cl_list:
        return {"highest_claim": None}
    top = max(cl_list, key=lambda c: c.amount)
    return {"highest_claim": top.model_dump()}

def pending_claims() -> List[Claim]:
    cl_list = cl_repo.load()
    return [c for c in cl_list if c.status is ClaimStatus.Pending]