# -*- coding: utf-8 -*-
"""
Finanzmathematisches Kernmodul für B2B-Factoring, Working-Capital-Freisetzung (DSO),
Kontokorrent-Zinsvergleich, Delkredereschutz und Lieferanten-Skonto-Hebel im DACH-Raum (DE, AT, CH).

Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG):
Rein mathematisch-betriebswirtschaftliches Kalkulationsmodell ohne Rechts-, Steuer- oder Finanzierungsberatung.
"""

from dataclasses import dataclass
from typing import Dict, Any


COUNTRY_STANDARDS: Dict[str, Dict[str, Any]] = {
    "DE": {
        "currency": "EUR",
        "legal_norm": "§ 354a HGB (Wirksamkeit der Abtretung trotz Zessionsverbot im B2B) & § 1 Abs. 1a KWG (BaFin)",
        "default_factoring_interest_pct": 5.20,
        "default_overdraft_interest_pct": 8.90,
    },
    "AT": {
        "currency": "EUR",
        "legal_norm": "§§ 1392 ff. ABGB (Zession) & § 1396a ABGB (Unwirksamkeit gröblich benachteiligender Zessionsverbote)",
        "default_factoring_interest_pct": 5.40,
        "default_overdraft_interest_pct": 9.10,
    },
    "CH": {
        "currency": "CHF",
        "legal_norm": "Art. 164 ff. OR (Forderungsabtretung / Zession in CHF)",
        "default_factoring_interest_pct": 3.60,
        "default_overdraft_interest_pct": 6.80,
    },
}


@dataclass
class FactoringInput:
    country: str = "DE"
    annual_revenue: float = 2_500_000.0
    dso_days: float = 45.0
    factoring_type: str = "full"  # 'full', 'inhouse', 'silent'
    advance_rate_pct: float = 90.0
    service_fee_pct: float = 0.85
    delkredere_fee_pct: float = 0.25
    audit_fees_annual: float = 1_200.0
    factoring_interest_pct: float = 5.20
    overdraft_interest_pct: float = 8.90
    bad_debt_loss_pct: float = 0.40
    purchasing_share_pct: float = 35.0
    supplier_skonto_pct: float = 2.50


@dataclass
class FactoringResult:
    country: str
    currency: str
    legal_norm: str
    average_receivables: float
    immediate_liquidity: float
    retention_amount: float
    service_fee_cost: float
    delkredere_and_audit_cost: float
    factoring_interest_cost: float
    total_factoring_costs: float
    total_cost_pct_of_revenue: float
    saved_overdraft_interest: float
    saved_bad_debt: float
    realized_skonto_gain: float
    total_savings: float
    total_savings_pct_of_revenue: float
    net_annual_benefit: float
    effective_net_cost_ratio_pct: float


def get_country_legal_standard(country: str) -> Dict[str, Any]:
    c = country.upper().strip()
    if c not in COUNTRY_STANDARDS:
        raise ValueError(f"Unsupported country '{country}'. Choose from DE, AT, CH.")
    return COUNTRY_STANDARDS[c]


def calculate_factoring(inp: FactoringInput) -> FactoringResult:
    std = get_country_legal_standard(inp.country)
    if inp.annual_revenue < 0:
        raise ValueError("annual_revenue must be non-negative")
    if inp.dso_days <= 0:
        raise ValueError("dso_days must be positive")
    if not (0.0 < inp.advance_rate_pct <= 100.0):
        raise ValueError("advance_rate_pct must be between 0 and 100")

    rev = float(inp.annual_revenue)
    dso = float(inp.dso_days)
    adv_ratio = float(inp.advance_rate_pct) / 100.0

    # 1. Working Capital / gebundener Forderungsbestand (kaufmännisch 360 Tage)
    average_receivables = rev * (dso / 360.0)
    immediate_liquidity = average_receivables * adv_ratio
    retention_amount = average_receivables - immediate_liquidity

    # 2. Factoring-Jahreskosten
    service_fee_cost = rev * (float(inp.service_fee_pct) / 100.0)
    delkredere_and_audit_cost = rev * (float(inp.delkredere_fee_pct) / 100.0) + max(0.0, float(inp.audit_fees_annual))
    factoring_interest_cost = immediate_liquidity * (float(inp.factoring_interest_pct) / 100.0)
    total_factoring_costs = service_fee_cost + delkredere_and_audit_cost + factoring_interest_cost
    total_cost_pct = (total_factoring_costs / rev * 100.0) if rev > 0 else 0.0

    # 3. Gegenrechnung: Einsparungen & Skontoerträge
    saved_overdraft_interest = immediate_liquidity * (float(inp.overdraft_interest_pct) / 100.0)
    saved_bad_debt = rev * (float(inp.bad_debt_loss_pct) / 100.0)
    realized_skonto_gain = rev * (float(inp.purchasing_share_pct) / 100.0) * (float(inp.supplier_skonto_pct) / 100.0)
    total_savings = saved_overdraft_interest + saved_bad_debt + realized_skonto_gain
    total_savings_pct = (total_savings / rev * 100.0) if rev > 0 else 0.0

    # 4. Netto-Vorteil & Effektive Kostenquote
    net_annual_benefit = total_savings - total_factoring_costs
    effective_net_cost_ratio_pct = ((total_factoring_costs - total_savings) / rev * 100.0) if rev > 0 else 0.0

    return FactoringResult(
        country=inp.country.upper().strip(),
        currency=std["currency"],
        legal_norm=std["legal_norm"],
        average_receivables=round(average_receivables, 2),
        immediate_liquidity=round(immediate_liquidity, 2),
        retention_amount=round(retention_amount, 2),
        service_fee_cost=round(service_fee_cost, 2),
        delkredere_and_audit_cost=round(delkredere_and_audit_cost, 2),
        factoring_interest_cost=round(factoring_interest_cost, 2),
        total_factoring_costs=round(total_factoring_costs, 2),
        total_cost_pct_of_revenue=round(total_cost_pct, 4),
        saved_overdraft_interest=round(saved_overdraft_interest, 2),
        saved_bad_debt=round(saved_bad_debt, 2),
        realized_skonto_gain=round(realized_skonto_gain, 2),
        total_savings=round(total_savings, 2),
        total_savings_pct_of_revenue=round(total_savings_pct, 4),
        net_annual_benefit=round(net_annual_benefit, 2),
        effective_net_cost_ratio_pct=round(effective_net_cost_ratio_pct, 4),
    )
