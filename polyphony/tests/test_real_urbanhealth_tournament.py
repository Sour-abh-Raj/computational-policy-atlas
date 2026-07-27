"""Real Urban⇄Transport⇄Energy⇄Health (co-benefits) tournament tests (issue #7-real).

The synthetic coupling was kept (Iter 19); this checks the real-data verdict. The honest outcome is a
**CUT with the right sign**: PM2.5 is positively correlated with the all-cause death rate (as the
mechanism assumes), but once a trend is removed the exposure adds no skill (hazard k → 0) and a generic
placebo does as well or better. The positive correlation is a shared downward trend, not an independent
co-benefit signal in aggregate mortality.
"""

from __future__ import annotations

import pytest

from polyphony.data.loaders import has_real_cobenefit, load_real_cobenefit
from polyphony.experiments.real_urbanhealth_tournament import run_real_cobenefit_tournament

pytestmark = pytest.mark.skipif(
    not has_real_cobenefit(),
    reason="real co-benefit dataset not fetched; run `python -m polyphony.data.fetch_real`",
)


def test_real_cobenefit_dataset_loads_and_is_not_synthetic():
    ds = load_real_cobenefit()
    assert not ds.synthetic
    assert len(ds) >= 20
    assert "pm25" in ds.series and "death_rate" in ds.series


def test_real_cobenefit_coupling_is_cut_but_with_the_right_sign():
    r = run_real_cobenefit_tournament()
    # The raw correlation has the assumed sign (more PM2.5 ↔ more mortality)…
    assert r.pm25_death_corr > 0.0
    assert r.sign_as_assumed
    # …but the exposure adds NO skill above a trend (the partial coefficient clamps to zero)…
    assert r.hazard_coef == 0.0
    assert r.synergy_delta <= 0.05
    # …and a generic time-trend placebo does as well or better ⇒ the co-benefit is confounding, not signal.
    assert not r.beats_placebo
    assert r.verdict() == "cut"
