# BenMAP-CE — Environmental Benefits Mapping and Analysis Program

!!! info "Bronze dossier"
    BenMAP-CE is the **air-pollution health-impact and benefits** model — the canonical tool for
    turning a change in ambient pollution (chiefly fine particulate **PM2.5** and ozone) into
    **attributable health outcomes** (premature deaths, hospitalizations) and their **monetized value**.
    Where [Covasim](covasim.md)/[GLEAM](gleam.md) simulate *transmission*, BenMAP is an **accounting /
    exposure–response** engine: it multiplies a population's exposure change by an epidemiological
    **concentration–response function** and a valuation, over a GIS grid. It is the workhorse behind
    U.S. EPA regulatory impact analyses and a template for the WHO's AirQ+.

> A GIS-based exposure–response accounting tool that estimates the health impacts and economic value of
> changes in ambient air quality, using epidemiological concentration–response functions.

## Positioning card

| Axis (see [Taxonomy](../../foundations/taxonomy.md)) | BenMAP-CE |
|------|------|
| Optimization vs Simulation | **Simulation** (accounting / impact assessment) |
| Top-down vs Bottom-up | **Grid-cell population** (bottom-up exposure) |
| Equilibrium | N/A |
| Foresight | N/A (static, scenario-differenced) |
| Deterministic vs Stochastic | **Deterministic point estimate + Monte-Carlo uncertainty bands** |
| Time / Space | Annual / GIS grid (county or finer) |
| Solution method | **Concentration–response function × exposed population × valuation** |

| Field | Value |
|-------|-------|
| Full name | BenMAP-CE — Environmental Benefits Mapping and Analysis Program, Community Edition |
| Domain | Health / Epidemiology (environmental) |
| First release / current | 2000s / ongoing (open-source CE since 2015) |
| Institution · lead | U.S. Environmental Protection Agency |
| Language · solver | C# / open source |
| License / access | Public domain (freely available) |

---

## 🎓 Scholar Track

**History & motivation.** BenMAP grew out of the U.S. EPA's need to quantify the **benefits** side of
Clean Air Act regulation — the counterpart to compliance-cost accounting. Its scientific foundation is
the epidemiology that established that **long-term PM2.5 exposure raises mortality**: the **Harvard Six
Cities study** (Dockery et al. 1993) and the ACS cohort (Pope et al. 2002), later synthesized into
global concentration–response forms such as the **GEMM** (Burnett et al. 2018). BenMAP operationalizes
that literature so a modeled *air-quality change* becomes a defensible *health and dollar* number.

**Mathematical formulation.** The core is a **concentration–response function (CRF)**. For a pollutant
change $\Delta C$ over a population $P$ with baseline incidence $y_0$, the attributable cases are
$\Delta y = y_0 \, P \,\bigl(1 - e^{-\beta \Delta C}\bigr)$, where $\beta$ is the log-linear CRF slope
estimated from a cohort study (relative risk $RR = e^{\beta \Delta C}$). Impacts are summed over grid
cells and health endpoints, then **monetized** (value of a statistical life, cost of illness). Uncertainty
is propagated by **Monte-Carlo** sampling of $\beta$ and valuation distributions, yielding confidence
intervals rather than a single point.

**Calibration & validation.** BenMAP does not fit dynamics; it **imports** exposure surfaces (monitors +
models), population and baseline-incidence data, and **peer-reviewed CRFs**. Its credibility rests on the
**external validity of the borrowed epidemiology** — which endpoints, which cohort, which exposure
window — so the honest reporting of CRF choice and its uncertainty is the whole ball game.

**Strengths / weaknesses / criticisms.** *Strengths:* transparent, auditable, GIS-resolved, standard
CRFs, native uncertainty bands. *Criticisms:* only as good as the input CRF (transferability across
populations, confounding, the shape of the low-dose response); static (no feedbacks); attributes
association as if causal — the sign and magnitude are **hypotheses inherited from epidemiology**, not
re-derived.

## 🛠️ Engineer Track

**Architecture & engines.** BenMAP is a **[Data Pipeline](../../patterns/data-pipeline.md)** (fuse
exposure grids + population + incidence) feeding a **[Welfare/Equity Engine](../../patterns/welfare-equity-engine.md)**
(attributable outcomes and their monetized, distributable value), with a
**[Sensitivity Engine](../../patterns/sensitivity-engine.md)** wrapper (Monte-Carlo over CRF/valuation).
It is the cleanest example in the atlas of an **exposure–response accounting** engine: no state dynamics,
just a well-instrumented multiply-and-sum with uncertainty carried end to end.

**Data & complexity.** Cheap: a grid × endpoints × Monte-Carlo draws. The heavy lift is assembling
consistent exposure surfaces and choosing/citing CRFs.

**Openness / extensibility.** Fully open (Community Edition); users can load custom CRFs, endpoints,
exposure surfaces, and valuations — which is also how it is misused (cherry-picked CRFs).

## 🏛️ Architect Track

**Reusable patterns.** The transferable idea is the **co-benefits bridge**: a single CRF turns the
*output of one domain* (transport/energy → ambient PM2.5) into a *welfare outcome in another*
(mortality), making **cross-domain co-benefits** computable. This is exactly the coupling Polyphony's
Urban⇄Transport⇄Energy⇄Health loop tests — and BenMAP is the reference for doing it honestly, with the
CRF as an **inspectable dial** and its uncertainty reported, never a hidden constant.

**Trade-offs & alternatives.** Static impact assessment (BenMAP, WHO **AirQ+**, GBD's exposure-response)
vs dynamic transmission models ([Covasim](covasim.md), [GLEAM](gleam.md)): the former is right for
**chronic-exposure** burdens where the epidemiology is external and stable; the latter for **infectious**
dynamics. They answer different questions and should not be conflated.

**Adoption.** The standard tool in U.S. EPA Regulatory Impact Analyses; adapted internationally (WHO
AirQ+); its CRFs underpin the Global Burden of Disease air-pollution estimates.

**Ecosystem.** U.S. EPA; WHO AirQ+; GBD exposure-response curves; the Harvard/ACS cohort epidemiology
that supplies the CRFs.

**Research gaps.** Low-dose CRF shape; transferability of cohort CRFs across populations; integrating
dynamic exposure (rather than annual means); coupling to upstream transport/energy models so the
co-benefit is computed *end to end* — the gap Polyphony's fourth loop probes.

!!! quote "Lesson for the integrated simulator"
    BenMAP teaches that a **co-benefit is only as honest as its concentration–response function**. The
    step from "policy changes PM2.5" to "policy saves lives" is a single, **borrowed, uncertain**
    parameter — so it belongs on a **dial** with its provenance and confidence band attached, and the
    resulting claim must survive the same **placebo / negative-control** discipline the atlas demands of
    any coupling, not ride on the intuitive appeal of "cleaner air is good."

## Major publications

- Dockery, D. W., et al. (1993). "An association between air pollution and mortality in six U.S.
  cities." *New England Journal of Medicine* 329(24).
- Pope, C. A., et al. (2002). "Lung cancer, cardiopulmonary mortality, and long-term exposure to fine
  particulate air pollution." *JAMA* 287(9).
- Burnett, R., et al. (2018). "Global estimates of mortality associated with long-term exposure to
  outdoor fine particulate matter (GEMM)." *PNAS* 115(38).
- Haines, A., et al. (2009). "Public health benefits of strategies to reduce greenhouse-gas emissions."
  *The Lancet* 374(9707).

## See also
- Contrast: [Covasim](covasim.md) · [GLEAM](gleam.md)
- Patterns: [Data Pipeline](../../patterns/data-pipeline.md) · [Welfare/Equity Engine](../../patterns/welfare-equity-engine.md) · [Sensitivity Engine](../../patterns/sensitivity-engine.md)
- Positioning: [Taxonomy](../../foundations/taxonomy.md) · Quality bar: [DICE dossier](../../model-families/climate-iam/dice.md)
