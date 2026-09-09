# Data Privacy (GDPR / CCPA / PII) -- Platform-Wide

Real, current state, verified 2026-09-09: `git grep -c "GDPR\|CCPA"`
returns 0 hits anywhere in this repository prior to this document. This
is a genuine, previously-undocumented gap, closed here with an honest
policy rather than a fabricated compliance claim.

## What data this platform actually uses

Every one of the 14 problems is trained and evaluated on the public
Kaggle "AMEX Default Prediction" competition dataset. That dataset is
**already anonymized and feature-obfuscated by the competition's own
design** -- column names are opaque codes (e.g. `D_39`, `B_4`, `S_2`,
grouped into Delinquency / Spend / Payment / Balance / Risk categories),
not real applicant attributes, and `customer_ID` is Kaggle's own hashed
identifier, not a real-world account or SSN. This platform has never
touched a real individual's actual financial or personal data. See each
problem's `MODEL_CARD.md` for the per-problem confirmation of this.

## What that means for GDPR / CCPA today

Because no real personal data is processed, neither GDPR (EU) nor CCPA
(California) obligations are actually triggered by this platform as it
exists and is used today (a public portfolio/research project, not a
live product processing real applicants' data). This document does not
claim compliance with either regulation -- it states plainly why neither
currently applies, which is the honest and correct thing to say for a
project at this stage.

## What would be required if this platform ever processed real data

If any part of this platform were adapted to score real, identifiable
applicants, the following would become real, mandatory requirements
(none implemented today -- listed here as a genuine forward-looking
checklist, not as work already done):

- **Legal basis and consent**: a documented lawful basis (GDPR Art. 6)
  or CCPA-compliant notice-at-collection before processing any real
  applicant's data.
- **Data minimization and retention limits**: collect and retain only
  the fields a specific model genuinely needs, for a stated, bounded
  retention period.
- **Right to access / deletion / correction**: a real, working process
  for a data subject to request their data, request its deletion (GDPR
  Art. 17 "right to be forgotten"; CCPA's deletion right), or correct
  inaccuracies -- including in any trained model's cached features, not
  just a source database.
- **PII encryption at rest and in transit**: real applicant identifiers
  and any raw (non-anonymized) financial fields encrypted at rest, and
  TLS in transit (see `TLS.md` for this platform's current, separate
  gap on that front).
- **Access controls and audit logging**: role-based access to any real
  applicant data, with a real audit trail of who accessed what and when
  -- this platform currently has no authentication/authorization layer
  at all (a separate, already-tracked gap; see `ROADMAP.md`).
- **Data Processing Impact Assessment (DPIA)**: required under GDPR for
  processing likely to result in high risk to individuals -- automated
  credit-decisioning is a canonical example that would require one.
- **Cross-border transfer safeguards**: if any real applicant data or
  model artifacts were to move between jurisdictions, GDPR's transfer
  mechanisms (SCCs, adequacy decisions) would apply.

## Honest bottom line

This platform's current use of fully anonymized competition data is not
a loophole around privacy law -- it is the reason privacy law's
substantive obligations don't yet bind it. The checklist above is what
would need to become real, verified engineering work (not just another
markdown file) before this platform could responsibly touch real
applicant data.
