# Datasets — real historical series (provenance)

Every real result in Polyphony is backed by a committed CSV here, each rebuildable from public sources by
`python -m polyphony.data.fetch_real` (World Bank WDI + OWID + FRED; no credentials, no license-restricted
data). Loaders live in `polyphony/data/loaders.py`; when a CSV is absent the loader falls back to a
**clearly-labeled synthetic** series (for offline harness testing only — it proves the machinery, never
real-world skill).

## Aggregate time-series (the forecasting couplings)

| File | Columns | Sources | Backs |
|------|---------|---------|-------|
| `real_gdp_co2.csv` | year, gdp, co2, temp | WB `NY.GDP.MKTP.KD` · OWID CO₂ · Hadley temp | Real climate→GDP (cut) |
| `real_food.csv` | year, cereal_yield, temp | WB `AG.YLD.CREL.KG` · Hadley temp | Land⇄Climate⇄Food real (cut: wrong sign) |
| `real_cobenefit.csv` | year, pm25, death_rate | WB `EN.ATM.PM25.MC.M3` · WB `SP.DYN.CDRT.IN` | Co-benefit real (cut: confounded) |
| `real_nexus.csv` | year, food_price, energy_price | FRED `PFOODINDEXM` · `PNRGINDEXM` | Water⇄Energy⇄Food real (cut: no skill) |
| `real_finance.csv` | year, gdp, spread | FRED `GDPC1` · `BAA10Y` | Macro⇄Finance real (cut: regime-dependent) |
| `real_trade.csv` | year, production_co2, consumption_co2, openness | OWID (UK) · WB `NE.TRD.GNFS.ZS` | Trade⇄Emissions real (cut: confounded) |
| `real_inflation.csv` | year, energy, cpi | FRED `PNRGINDEXM` · `CPIAUCSL` | **Energy⇄Inflation (KEPT)** |
| `real_inflation_q.csv` | year, quarter, energy, cpi | FRED `PNRGINDEXM` · `CPIAUCSL` (quarterly) | Energy⇄Inflation higher-power confirmation |
| `real_housing.csv` | year, rate, hpi | FRED `MORTGAGE30US` · `CSUSHPINSA` | Interest-Rate⇄Housing real (cut: reverse causation) |
| `real_okun.csv` | year, unrate, gdp | FRED `UNRATE` · `GDPC1` | Okun probe (cut: coincident) |
| `real_yieldcurve.csv` | year, spread, gdp | FRED `T10Y3M` · `GDPC1` | Yield-curve probe (cut: washed out annually) |

## Cross-country panels (the within-unit mechanisms)

| File | Columns | Sources | Backs |
|------|---------|---------|-------|
| `real_leakage_panel.csv` | iso, year, cons_prod_ratio, openness | OWID CO₂ · WB `NE.TRD.GNFS.ZS` | Leakage panel (cut: confounded-away) |
| `real_pm25_mortality_panel.csv` | iso, year, pm25, death_rate | WB `EN.ATM.PM25.MC.M3` · `SP.DYN.CDRT.IN` | Co-benefit panel (cut: confounded outcome) |
| `real_preston_panel.csv` | iso, year, log_gdppc, life_exp | WB `NY.GDP.PCAP.KD` · `SP.DYN.LE00.IN` | **Preston curve (SURVIVES)** |
| `real_demographic_panel.csv` | iso, year, log_gdppc, fertility | WB `NY.GDP.PCAP.KD` · `SP.DYN.TFRT.IN` | **Demographic transition (SURVIVES)** |
| `real_inequality_panel.csv` | iso, year, log_gdppc, gini | WB `NY.GDP.PCAP.KD` · `SI.POV.GINI` | Kuznets / equity — income→*relative* inequality (cut: confounded-away) |
| `real_poverty_panel.csv` | iso, year, log_gdppc, poverty | WB `NY.GDP.PCAP.KD` · `SI.POV.DDAY` | Equity — income→*absolute* poverty (**SURVIVES**) |

## Reproduce

```
python -m polyphony.data.fetch_real   # rebuilds every CSV above from source
```

Network egress is intermittent in the loop; run when it is up. The test suite `skipif`s the real-data tests
when a CSV is absent, so the suite never depends on the network. See `docs/polyphony/04-validation.md` for
what each series establishes, and `docs/polyphony/failure-modes.md` for the two-domain epistemology the whole
collection supports.
