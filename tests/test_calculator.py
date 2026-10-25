# -*- coding: utf-8 -*-
"""
Unit-Tests für factoring_dach (DACH B2B Factoring-, Einkaufsfinanzierungs- & Working-Capital-Rechner 2026)
"""

import pytest
from factoring_dach import (
    FactoringInput,
    calculate_factoring,
    get_country_legal_standard,
)


def test_default_de_calculation():
    """Prüft das Standard-Rechenmodell für ein deutsches KMU (2,5 Mio. € Umsatz, 45 Tage DSO)."""
    inp = FactoringInput()
    res = calculate_factoring(inp)
    assert res.country == "DE"
    assert res.currency == "EUR"
    # 2,500,000 * 45 / 360 = 312,500.0
    assert res.average_receivables == pytest.approx(312_500.0)
    # 90% Bevorschussung = 281,250.0
    assert res.immediate_liquidity == pytest.approx(281_250.0)
    assert res.retention_amount == pytest.approx(31_250.0)


def test_factoring_cost_breakdown():
    """Prüft die exakte Berechnung von Servicegebühr, Delkrederegebühr und Vorfinanzierungszinsen."""
    inp = FactoringInput(
        annual_revenue=2_500_000.0,
        dso_days=45.0,
        advance_rate_pct=90.0,
        service_fee_pct=0.85,
        delkredere_fee_pct=0.25,
        audit_fees_annual=1_200.0,
        factoring_interest_pct=5.20,
    )
    res = calculate_factoring(inp)
    assert res.service_fee_cost == pytest.approx(21_250.0)
    assert res.delkredere_and_audit_cost == pytest.approx(7_450.0)
    assert res.factoring_interest_cost == pytest.approx(14_625.0)
    assert res.total_factoring_costs == pytest.approx(43_325.0)


def test_savings_and_skonto_leverage():
    """Prüft die Gegenrechnung aus Kontokorrentzins-Ersparnis, Ausfallschutz und Einkaufs-Skonto."""
    inp = FactoringInput(
        annual_revenue=2_500_000.0,
        dso_days=45.0,
        advance_rate_pct=90.0,
        overdraft_interest_pct=8.90,
        bad_debt_loss_pct=0.40,
        purchasing_share_pct=35.0,
        supplier_skonto_pct=2.50,
    )
    res = calculate_factoring(inp)
    assert res.saved_overdraft_interest == pytest.approx(25_031.25)
    assert res.saved_bad_debt == pytest.approx(10_000.0)
    assert res.realized_skonto_gain == pytest.approx(21_875.0)
    assert res.total_savings == pytest.approx(56_906.25)
    assert res.net_annual_benefit == pytest.approx(13_581.25)


def test_austria_legal_standard():
    """Prüft den österreichischen Modus (§ 1392 ABGB / § 1396a ABGB)."""
    inp = FactoringInput(country="AT", annual_revenue=1_800_000.0, dso_days=30.0)
    res = calculate_factoring(inp)
    assert res.country == "AT"
    assert res.currency == "EUR"
    assert "ABGB" in res.legal_norm
    assert res.average_receivables == pytest.approx(150_000.0)


def test_switzerland_chf_standard():
    """Prüft den Schweizer Modus (Art. 164 ff. OR in CHF)."""
    inp = FactoringInput(
        country="CH",
        annual_revenue=3_600_000.0,
        dso_days=60.0,
        advance_rate_pct=85.0,
        factoring_interest_pct=3.50,
        overdraft_interest_pct=6.50,
    )
    res = calculate_factoring(inp)
    assert res.country == "CH"
    assert res.currency == "CHF"
    assert "Art. 164" in res.legal_norm
    assert res.average_receivables == pytest.approx(600_000.0)
    assert res.immediate_liquidity == pytest.approx(510_000.0)


def test_inhouse_factoring_lower_fee():
    """Prüft, dass Inhouse-Factoring mit reduzierter Gebühr höhere Netto-Vorteile erzielt."""
    full_res = calculate_factoring(FactoringInput(service_fee_pct=0.90))
    inhouse_res = calculate_factoring(FactoringInput(service_fee_pct=0.45))
    assert inhouse_res.total_factoring_costs < full_res.total_factoring_costs
    assert inhouse_res.net_annual_benefit > full_res.net_annual_benefit


def test_high_dso_increases_working_capital_release():
    """Prüft den linearen Zusammenhang zwischen DSO und freigesetztem Working Capital."""
    res_30 = calculate_factoring(FactoringInput(dso_days=30.0))
    res_60 = calculate_factoring(FactoringInput(dso_days=60.0))
    assert res_60.immediate_liquidity == pytest.approx(res_30.immediate_liquidity * 2.0)


def test_zero_skonto_scenario():
    """Prüft die Berechnung für Dienstleister ohne nennenswertes Einkaufsvolumen."""
    inp = FactoringInput(purchasing_share_pct=0.0, supplier_skonto_pct=0.0)
    res = calculate_factoring(inp)
    assert res.realized_skonto_gain == 0.0
    assert res.total_savings == pytest.approx(res.saved_overdraft_interest + res.saved_bad_debt)


def test_invalid_country_raises():
    """Prüft Fehlerbehandlung bei ungültigem Ländercode."""
    with pytest.raises(ValueError, match="Unsupported country"):
        get_country_legal_standard("US")


def test_invalid_parameters_raise():
    """Prüft Fehlerbehandlung bei negativen Umsätzen, DSO <= 0 oder ungültiger Bevorschussungsquote."""
    with pytest.raises(ValueError):
        calculate_factoring(FactoringInput(annual_revenue=-100.0))
    with pytest.raises(ValueError):
        calculate_factoring(FactoringInput(dso_days=0.0))
    with pytest.raises(ValueError):
        calculate_factoring(FactoringInput(advance_rate_pct=120.0))


def test_effective_net_cost_ratio_sign():
    """Prüft das Vorzeichen der effektiven Netto-Kostenquote."""
    res_profit = calculate_factoring(FactoringInput(purchasing_share_pct=50.0, supplier_skonto_pct=3.0))
    assert res_profit.net_annual_benefit > 0
    assert res_profit.effective_net_cost_ratio_pct < 0
