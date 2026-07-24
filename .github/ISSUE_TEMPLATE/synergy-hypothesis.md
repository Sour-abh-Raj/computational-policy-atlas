---
name: Synergy hypothesis
about: Propose a cross-domain coupling to test (coupled must beat sum-of-parts on real data)
title: "[synergy] <domain-A> ⇄ <domain-B>: <one-line feedback>"
labels: ["synergy", "phase-3", "needs-evidence"]
---

## The coupling
<!-- Which two (or more) models/domains, and the feedback loop between them.
     e.g. energy prices ⇄ CGE output ⇄ emissions ⇄ climate damages ⇄ energy demand. -->

## Falsifiable prediction
<!-- What should the COUPLED ensemble predict better than the best combination of the
     ISOLATED parts, on what real historical data? Be specific about the target metric
     and the out-of-sample / holdout / distribution-shift test. -->

## Literature grounding
<!-- Primary sources motivating this feedback. Link relevant atlas dossiers, the
     comparative matrix that frames the contested assumption, and graph nodes/edges. -->

## How we'll decide
<!-- Tournament design: coupled config vs decoupled baseline(s) vs rival couplings.
     A coupling advances ONLY if it adds demonstrable synergy. "No synergy" is an
     acceptable, publishable outcome — say how we'd record it on the leaderboard. -->

## Definition of done for this issue
- [ ] Coupling implemented behind a dial (can be switched off)
- [ ] Backtested coupled vs sum-of-parts on real data (out-of-sample)
- [ ] Leaderboard row added with the interaction effect
- [ ] Survived a red-team attempt, or the break re-entered selection
