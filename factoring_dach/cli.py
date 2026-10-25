# -*- coding: utf-8 -*-
"""
CLI für den DACH B2B Factoring-, Einkaufsfinanzierungs- & Working-Capital-Rechner 2026
"""

import argparse
import json
from .calculator import FactoringInput, calculate_factoring


def main():
    parser = argparse.ArgumentParser(
        description="DACH B2B Factoring-, Einkaufsfinanzierungs- & Working-Capital-Rechner 2026 (DE, AT, CH)"
    )
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH"], help="Land (DE, AT, CH)")
    parser.add_argument("--revenue", type=float, default=2_500_000.0, help="Factoringfaehiger Jahresumsatz")
    parser.add_argument("--dso", type=float, default=45.0, help="Zahlungsziel der Debitoren in Tagen (DSO)")
    parser.add_argument("--advance-rate", type=float, default=90.0, help="Bevorschussungsquote in Prozent (%%)")
    parser.add_argument("--service-fee", type=float, default=0.85, help="Factoring-Servicegebuehr in Prozent (%%)")
    parser.add_argument("--delkredere-fee", type=float, default=0.25, help="Delkrederegebuehr in Prozent (%%)")
    parser.add_argument("--factoring-interest", type=float, default=5.20, help="Factoring-Zinssatz p.a. in Prozent (%%)")
    parser.add_argument("--overdraft-interest", type=float, default=8.90, help="Kontokorrent-Zinssatz p.a. in Prozent (%%)")
    parser.add_argument("--bad-debt", type=float, default=0.40, help="Historisches Forderungsausfallrisiko in Prozent (%%)")
    parser.add_argument("--purchasing-share", type=float, default=35.0, help="Skontierfaehiges Einkaufsvolumen (%% vom Umsatz)")
    parser.add_argument("--skonto", type=float, default=2.50, help="Lieferanten-Skontosatz in Prozent (%%)")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    args = parser.parse_args()

    inp = FactoringInput(
        country=args.country,
        annual_revenue=args.revenue,
        dso_days=args.dso,
        advance_rate_pct=args.advance_rate,
        service_fee_pct=args.service_fee,
        delkredere_fee_pct=args.delkredere_fee,
        factoring_interest_pct=args.factoring_interest,
        overdraft_interest_pct=args.overdraft_interest,
        bad_debt_loss_pct=args.bad_debt,
        purchasing_share_pct=args.purchasing_share,
        supplier_skonto_pct=args.skonto,
    )
    res = calculate_factoring(inp)

    if args.json:
        print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))
    else:
        print("=" * 72)
        print(f"DACH B2B FACTORING- & WORKING-CAPITAL-ANALYSE 2026 ({res.country} / {res.currency})")
        print("=" * 72)
        print(f"Rechtsnorm                 : {res.legal_norm}")
        print(f"Forderungsbestand (DSO)    : {res.average_receivables:,.2f} {res.currency}")
        print(f"Sofortige Liquiditaet      : {res.immediate_liquidity:,.2f} {res.currency}")
        print(f"Jahreskosten Factoring     : {res.total_factoring_costs:,.2f} {res.currency} ({res.total_cost_pct_of_revenue:.2f} %)")
        print(f"Summe Einsparungen/Skonto  : {res.total_savings:,.2f} {res.currency} ({res.total_savings_pct_of_revenue:.2f} %)")
        print(f"Netto-Ergebnisvorteil p.a. : {res.net_annual_benefit:+,.2f} {res.currency}")
        print("=" * 72)


if __name__ == "__main__":
    main()
