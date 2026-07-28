"""Panel validation — attacking "confounded-away" with cross-country fixed effects (Iters 33–34).

The modal way a real-data coupling was cut is **confounded-away**: a strong correlation between two
trending series that vanishes once a trend is removed. A *panel* of many countries with **two-way fixed
effects** — removing every country's level *and* every year's common shock (the shared global trend) —
isolates the **within-country** relationship, the mechanism stripped of the confounding trend.

Two applications, deliberately contrasting:

- **Carbon leakage** (openness → consumption/production CO₂ ratio): a clean confounded-away confirmation —
  a positive pooled correlation nearly vanishes within (Iter 33).
- **Co-benefit** (PM2.5 → all-cause mortality): the mechanism is *real at the cohort level*, yet the panel
  **cannot recover it** — all-cause mortality carries strong within-country development/aging trends, so
  the within correlation is weak/wrong-signed. A reminder that panel FE isolates the mechanism only when
  the **outcome** is not itself dominated by a confounded within-country trajectory (Iter 34).

The fixed-effects estimator is validated on synthetic panels (a pure confound demeans to ≈0; a real
within-effect survives), so the tool — not just each datum — is trustworthy.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..data.loaders import (
    load_real_demographic_panel,
    load_real_leakage_panel,
    load_real_pm25_mortality_panel,
    load_real_preston_panel,
)


def _group_demean(v: np.ndarray, group: np.ndarray) -> np.ndarray:
    out = v.astype(float).copy()
    for g in np.unique(group):
        mask = group == g
        out[mask] -= out[mask].mean()
    return out


def two_way_within(value: np.ndarray, driver: np.ndarray, unit: np.ndarray, time: np.ndarray, iters: int = 60) -> float:
    """Correlation of ``value`` and ``driver`` after two-way (unit + time) fixed-effects demeaning."""
    v, d = value.astype(float).copy(), driver.astype(float).copy()
    for _ in range(iters):
        v = _group_demean(_group_demean(v, unit), time)
        d = _group_demean(_group_demean(d, unit), time)
    if np.std(v) == 0 or np.std(d) == 0:
        return 0.0
    return float(np.corrcoef(d, v)[0, 1])


@dataclass(frozen=True)
class PanelFEResult:
    coupling: str
    assumed_sign: int  # +1 (driver raises target) or −1
    n_obs: int
    n_countries: int
    n_years: int
    pooled_corr: float
    within_corr: float

    @property
    def attenuation(self) -> float:
        """Fraction of the pooled correlation that disappears under two-way FE (1 ⇒ fully a shared trend)."""
        if self.pooled_corr == 0:
            return 0.0
        return 1.0 - abs(self.within_corr) / abs(self.pooled_corr)

    @property
    def within_has_assumed_sign(self) -> bool:
        return (self.within_corr > 0) == (self.assumed_sign > 0) and abs(self.within_corr) > 0.1

    def verdict(self) -> str:
        pooled_right = (self.pooled_corr > 0) == (self.assumed_sign > 0) and abs(self.pooled_corr) > 0.2
        if pooled_right and abs(self.within_corr) < 0.1:
            return "cut-confirmed (confounded-away)"
        if self.within_has_assumed_sign:
            return "within-signal survives"
        return "no within-country mechanism (outcome confounded)"


def _panel_fe(coupling: str, assumed_sign: int, iso, year, driver, target) -> PanelFEResult:
    return PanelFEResult(
        coupling=coupling,
        assumed_sign=assumed_sign,
        n_obs=len(target),
        n_countries=int(len(np.unique(iso))),
        n_years=int(len(np.unique(year))),
        pooled_corr=float(np.corrcoef(driver, target)[0, 1]),
        within_corr=two_way_within(target, driver, iso, year),
    )


def run_leakage_panel() -> PanelFEResult:
    """Carbon leakage: does trade openness explain the consumption/production CO₂ ratio *within* countries?"""
    iso, year, ratio, openness = load_real_leakage_panel()
    return _panel_fe("Trade⇄Emissions (leakage)", +1, iso, year, openness, ratio)


def run_pm25_mortality_panel() -> PanelFEResult:
    """Co-benefit: does PM2.5 explain the all-cause death rate *within* countries? (outcome is confounded)."""
    iso, year, pm25, death = load_real_pm25_mortality_panel()
    return _panel_fe("Urban⇄Transport⇄Energy⇄Health (co-benefit)", +1, iso, year, pm25, death)


def run_preston_panel() -> PanelFEResult:
    """The Preston curve: does income explain life expectancy *within* countries? A **surviving** panel
    coupling — a real within-unit mechanism, so the within-FE correlation stays positive (the boundary of
    the aggregate-forecasting generalization: panels with a genuine mechanism are *not* all confounded-away).
    """
    iso, year, log_gdppc, life_exp = load_real_preston_panel()
    return _panel_fe("Income⇄LifeExpectancy (Preston)", +1, iso, year, log_gdppc, life_exp)


def run_demographic_panel() -> PanelFEResult:
    """The demographic transition: does income lower fertility *within* countries? A **second surviving**
    panel coupling (assumed sign −1), confirming that the panel domain finds real within-unit mechanisms."""
    iso, year, log_gdppc, fertility = load_real_demographic_panel()
    return _panel_fe("Income⇄Fertility (demographic transition)", -1, iso, year, log_gdppc, fertility)


def run_all_panels() -> tuple[PanelFEResult, ...]:
    """Every panel coupling — the panel domain's own taxonomy: two survivors (real within-unit mechanisms)
    and two cut/confounded, mirroring the aggregate story."""
    return (run_preston_panel(), run_demographic_panel(), run_leakage_panel(), run_pm25_mortality_panel())
