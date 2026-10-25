# 🏦 DACH B2B Factoring-, Einkaufsfinanzierungs- & Working-Capital-Rechner 2026 (`factoring_dach`)

[![CI & Pytest](https://github.com/DACHDigitalwerk/factoring-working-capital-rechner-dach/actions/workflows/ci.yml/badge.svg)](https://github.com/DACHDigitalwerk/factoring-working-capital-rechner-dach/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Live Web-App](https://img.shields.io/badge/Live_Web_App-100%25_Client_Side-10b981)](https://dachdigitalwerk.github.io/factoring-working-capital-rechner/)

Finanzmathematische Python-Bibliothek und CLI (`dach-factoring`) zur Berechnung von **B2B-Factoring (Full-Service vs. Inhouse / Stilles Factoring)**, **Working-Capital-Freisetzung (DSO)**, **Delkredereschutz**, **Kontokorrent-Zinsersparnis** und **Lieferanten-Skonto-Hebel** für mittelständische Unternehmen (KMU) in **Deutschland (DE), Österreich (AT) und der Schweiz (CH)**.

---

## 🌐 Interaktive Web-Applikation & B2B-Fachratgeber (100 % Client-Side)

Nutzen Sie den kostenlosen Online-Kalkulator mit **druckfertigem DIN-A4 Working-Capital- & Factoring-Entscheidungsblatt** direkt im Browser:

- 🚀 **[DACH B2B Factoring-, Einkaufsfinanzierungs- & Working-Capital-Rechner 2026](https://dachdigitalwerk.github.io/factoring-working-capital-rechner/)**
- 📘 **[Factoring-Kosten berechnen 2026: Formel, Gebühren & Rechenbeispiel für KMU](https://dachdigitalwerk.github.io/factoring-kosten-berechnen-formel-kmu-2026.html)**
- ⚖️ **[Echtes vs. Unechtes Factoring: Delkredereschutz, Bilanzverkürzung & § 354a HGB](https://dachdigitalwerk.github.io/echtes-vs-unechtes-factoring-delkredere-vergleich.html)**
- 📈 **[Working Capital optimieren: Wie DSO-Senkung Ihren Einkaufs-Skonto finanziert](https://dachdigitalwerk.github.io/working-capital-optimieren-dso-skonto-hebel-b2b.html)**
- 🏠 **[DACH Digitalwerk – Alle 31 Self-Serve Web-Tools im Überblick](https://dachdigitalwerk.github.io/)**

---

## ✨ Kernfunktionen

1. **Working-Capital-Freisetzung (DSO-Formel):**
   - Berechnet den durchschnittlich gebundenen Forderungsbestand ($\text{Umsatz} \times \frac{\text{DSO}}{360}$) sowie die sofortige Liquiditätsauszahlung (z. B. 85 % – 90 % Bevorschussungsquote) und den Sicherheitseinbehalt.
2. **Vollständige Kosten- & Gegenfinanzierungs-Analyse:**
   - **Factoring-Jahreskosten:** Factoring-Servicegebühr + Delkrederegebühr + Debitorenprüfgebühren + Vorfinanzierungszinsen p.a.
   - **Einsparungen & Erträge:** Eingesparte Kontokorrentzinsen + vermiedene Forderungsausfälle (100 % Delkredereschutz) + realisierte **Einkaufs-Skontoerträge** durch sofortige Liquidität.
3. **Länderspezifische DACH-Standards:**
   - 🇩🇪 **Deutschland:** § 354a Abs. 1 HGB (Wirksamkeit der Abtretung trotz Zessionsverbot im B2B) & BaFin-Regulierung (§ 1 Abs. 1a KWG).
   - 🇦🇹 **Österreich:** §§ 1392 ff. ABGB (Zession) & § 1396a ABGB (Unwirksamkeit gröblich benachteiligender Zessionsverbote).
   - 🇨🇭 **Schweiz:** Art. 164 ff. OR (Forderungsabtretung in CHF).

---

## 📦 Installation & CLI-Nutzung

```bash
pip install -e .
dach-factoring --country DE --revenue 2500000 --dso 45 --purchasing-share 35 --skonto 2.5
```

### Python-API Beispiel

```python
from factoring_dach import FactoringInput, calculate_factoring

res = calculate_factoring(
    FactoringInput(
        country="DE",
        annual_revenue=2_500_000,
        dso_days=45,
        advance_rate_pct=90.0,
        service_fee_pct=0.85,
        delkredere_fee_pct=0.25,
        factoring_interest_pct=5.20,
        overdraft_interest_pct=8.90,
        bad_debt_loss_pct=0.40,
        purchasing_share_pct=35.0,
        supplier_skonto_pct=2.50,
    )
)

print(f"Sofortige Liquidität: {res.immediate_liquidity:,.2f} {res.currency}")
print(f"Netto-Ergebnisvorteil p.a.: {res.net_annual_benefit:+,.2f} {res.currency}")
```

---

## ⚠️ Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG)

Dieses Paket dient ausschließlich der unverbindlichen finanzmathematischen und betriebswirtschaftlichen Modellberechnung. Es stellt keine Rechts-, Steuer-, Bank- oder Finanzierungsberatung dar.
