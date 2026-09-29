# Schedule Builder Specimen

## The Trap
This specimen contains two classic Python traps:
1. `datetime.utcnow()` which is deprecated in Python 3.12 (returns naive datetime).
2. A mutable default argument `days=[]` in `add_recurrence`.

The trap is that the legacy test cases (or downstream consumers) actually rely on the mutable default argument's behavior of accumulating days across multiple calls when the list is omitted. 

A naive LLM refactoring will almost certainly fix the mutable default argument to `days=None` and initialize it inside the function, which breaks the implicit caching behavior.

## Scripted Naive Refactor
Fix the mutable default arg `days=[]` to `days=None` and `if days is None: days = []`.
