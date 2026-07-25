# Datasets

Drop **real historical** series here as wide CSVs (first row = headers, one numeric column per
series, one row per period). `polyphony.data.load("<name>")` prefers `datasets/<name>.csv`; if
absent it falls back to a **clearly-labeled synthetic** series (for offline harness testing only —
it proves the machinery, never real-world skill).

## Schema (example)

```
year,gdp,emissions,temperature
2000,100.0,80.0,0.60
2001,101.2,79.1,0.61
...
```

## Real sources to add (tracked as a GitHub issue)

- **GDP / output:** World Bank WDI (`NY.GDP.MKTP.KD`), Penn World Table.
- **Emissions:** Our World in Data / Global Carbon Project CO₂.
- **Temperature:** HadCRUT5 / GISTEMP anomalies.
- **Energy:** IEA World Energy Balances, Ember electricity.

Cite the primary source in the dataset's companion note and record the download/provenance so any
backtest is reproducible. Never commit credentialed or license-restricted raw data.
