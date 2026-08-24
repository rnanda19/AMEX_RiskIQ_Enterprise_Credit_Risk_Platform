"""AMEX RiskIQ Enterprise Credit Risk Platform -- shared library.

Code in this package is extracted, verbatim-in-logic, from the notebook that
originally defined it (see each module's docstring for the source notebook).
Extraction does not change any computed value or algorithm -- it makes
duplicated logic importable and unit-testable in one place instead of copied
inline into every notebook that needs it.

As of this package's creation (2026-08-24), the existing Phase 1 notebooks
(Problem 1, Problem 2) still carry their own inline copies of this logic --
wiring them to import from here instead is a separate, deliberately staged
follow-up (see ROADMAP.md), so that no already-verified, already-pushed
notebook output changes as a side effect of adding this package.
"""
