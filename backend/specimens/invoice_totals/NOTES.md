# Invoice Totals Specimen

## The Trap
The legacy code mixes Python's built-in `round()` (which implements banker's rounding / round-half-to-even) with a manual half-up rounding algorithm for tax calculations (`int(tax * 100 + 0.5) / 100.0`). 

A naive LLM refactoring will often notice this inconsistency and unify the rounding strategy (usually by replacing the manual calculation with `round(tax, 2)`). This changes the mathematical result for specific edge-case inputs where the exact value ends in exactly .5 cents (e.g., 2.505).

## Determinism
This specimen is fully deterministic and contains no I/O, networking, or randomness.

## Scripted Naive Refactor
Replace `tax_cents = int(tax * 100 + 0.5); return tax_cents / 100.0` with `return round(tax, 2)`.
