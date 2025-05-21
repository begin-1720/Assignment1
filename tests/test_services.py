# tests/test_services.py

import sys, os
import pytest
from datetime import date, timedelta

# ensure app/ is on PYTHONPATH
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.services import (
    ph_repo, cl_repo,
    create_policyholder, list_policyholders,
    create_claim, list_claims,
    claim_frequency, high_risk_policyholders,
    aggregate_by_policy_type, monthly_claims,
    average_claim_by_policy_type, highest_claim_of_all_time,
    pending_claims
)
from app.models import PolicyholderCreate, ClaimCreate, PolicyType, ClaimStatus


def setup_repos(tmp_path):
    # point repos at temp files, initialize them empty
    ph_repo.path = tmp_path / "policyholders.json"
    cl_repo.path = tmp_path / "claims.json"
    ph_repo.path.write_text("[]")
    cl_repo.path.write_text("[]")


def test_create_and_list_policyholders(tmp_path):
    setup_repos(tmp_path)
    ph = create_policyholder(PolicyholderCreate(
        name="Alice",
        policy_type=PolicyType.Health,
        sum_insured=1000.0
    ))
    assert ph.id == 0
    assert ph.name == "Alice"
    ph_list = list_policyholders()
    assert len(ph_list) == 1
    assert ph_list[0].id == 0


def test_create_multiple_policyholders(tmp_path):
    setup_repos(tmp_path)
    ph1 = create_policyholder(PolicyholderCreate(
        name="Bob",
        policy_type=PolicyType.Vehicle,
        sum_insured=2000.0
    ))
    ph2 = create_policyholder(PolicyholderCreate(
        name="Bob-dup",
        policy_type=PolicyType.Life,
        sum_insured=3000.0
    ))
    # No name-based constraint → both succeed, IDs auto-increment
    assert ph1.id == 0
    assert ph2.id == ph1.id + 1


def test_create_and_list_claims(tmp_path):
    setup_repos(tmp_path)
    create_policyholder(PolicyholderCreate(
        name="Carol",
        policy_type=PolicyType.Life,
        sum_insured=5000.0
    ))
    cl = create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=date.today(),
        amount=500.0,
        status=ClaimStatus.Pending
    ))
    assert cl.id == 0
    assert cl.amount == 500.0
    cl_list = list_claims()
    assert len(cl_list) == 1
    assert cl_list[0].id == 0


def test_create_claim_without_policyholder(tmp_path):
    setup_repos(tmp_path)
    with pytest.raises(ValueError):
        create_claim(ClaimCreate(
            policyholder_id=99,
            date_filed=date.today(),
            amount=10.0,
            status=ClaimStatus.Pending
        ))


def test_claim_frequency(tmp_path):
    setup_repos(tmp_path)
    create_policyholder(PolicyholderCreate(
        name="Dave",
        policy_type=PolicyType.Health,
        sum_insured=1000.0
    ))
    create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=date.today(),
        amount=100.0,
        status=ClaimStatus.Pending
    ))
    create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=date.today(),
        amount=50.0,
        status=ClaimStatus.Pending
    ))
    freq = claim_frequency(0)
    assert freq["claim_count"] == 2


def test_high_risk_policyholders(tmp_path):
    setup_repos(tmp_path)
    create_policyholder(PolicyholderCreate(
        name="Eve",
        policy_type=PolicyType.Vehicle,
        sum_insured=100.0
    ))
    # 4 recent small claims => high-risk by frequency
    for _ in range(4):
        create_claim(ClaimCreate(
            policyholder_id=0,
            date_filed=date.today(),
            amount=10.0,
            status=ClaimStatus.Pending
        ))
    high_risk = high_risk_policyholders()
    assert any(ph.id == 0 for ph in high_risk)


def test_aggregate_by_policy_type(tmp_path):
    setup_repos(tmp_path)
    create_policyholder(PolicyholderCreate(
        name="Frank",
        policy_type=PolicyType.Life,
        sum_insured=200.0
    ))
    create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=date.today(),
        amount=20.0,
        status=ClaimStatus.Pending
    ))
    create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=date.today(),
        amount=30.0,
        status=ClaimStatus.Pending
    ))
    agg = aggregate_by_policy_type()
    assert agg["Life"]["count"] == 2
    assert agg["Life"]["total_amount"] == 50.0


def test_reporting_endpoints(tmp_path):
    setup_repos(tmp_path)
    create_policyholder(PolicyholderCreate(
        name="Grace",
        policy_type=PolicyType.Health,
        sum_insured=300.0
    ))
    today = date.today()
    older = today - timedelta(days=40)
    create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=older,
        amount=100.0,
        status=ClaimStatus.Pending
    ))
    create_claim(ClaimCreate(
        policyholder_id=0,
        date_filed=today,
        amount=200.0,
        status=ClaimStatus.Pending
    ))
    mc = monthly_claims()
    assert mc[today.strftime("%Y-%m")] == 1
    assert mc[older.strftime("%Y-%m")] == 1

    avg = average_claim_by_policy_type()
    assert avg["Health"] == pytest.approx(150.0)

    top = highest_claim_of_all_time()
    assert top["highest_claim"]["amount"] == 200.0

    pend = pending_claims()
    assert len(pend) == 2
