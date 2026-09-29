# Log Digester Specimen

## The Trap
The code relies on list order and Python's stable sort. In `top_errors`, deduplication is done using an explicit loop and dictionary to maintain the order of first occurrence. It then sorts the resulting list by message length. Because Python's `sort()` is stable, elements with the same message length remain in their original chronological order.

A naive refactoring will often try to "modernize" the deduping logic by using a `set` or a dictionary comprehension (`list({err['message']: err for err in errors}.values())`), which destroys the chronological ordering. When the subsequent length sort happens, ties are broken differently (or arbitrarily).

## Determinism
Fully deterministic based on inputs. 

## Scripted Naive Refactor
Replace deduplication loop in `top_errors` with set-based or dict-values dedup logic.
