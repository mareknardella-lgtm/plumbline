#!/usr/bin/env python3
import sys


def verify_invoice_totals():
    # Simulate the naive refactor vs original
    print("Verifying invoice_totals trap...")
    tax = 2.505
    orig = int(tax * 100 + 0.5) / 100.0
    refactored = round(tax, 2)
    assert orig != refactored, f"Trap failed: {orig} == {refactored}"
    print(f"invoice_totals OK: orig={orig}, refactored={refactored}")


def verify_log_digester():
    print("Verifying log_digester trap...")
    logs = [
        {"message": "A error", "timestamp": "1"},
        {"message": "B error", "timestamp": "2"},
        {"message": "A error", "timestamp": "3"},
    ]

    unique_orig = []
    seen = {}
    for err in logs:
        msg = err["message"]
        if msg not in seen:
            seen[msg] = True
            unique_orig.append(err)

    # naive refactor (dict comp)
    unique_refactored = list({err["message"]: err for err in logs}.values())

    # Note: dict comprehension takes the LAST seen value, original took FIRST
    assert unique_orig != unique_refactored, "Trap failed"
    print("log_digester OK")


def verify_schedule_builder():
    print("Verifying schedule_builder trap...")

    def orig_add_recurrence(event, days=None):
        if days is None:
            days = []
        if not days:
            days.append("Monday")
        return days

    def refact_add_recurrence(event, days=None):
        if days is None:
            days = []
        if not days:
            days.append("Monday")
        return days

    orig_add_recurrence({})
    r2 = orig_add_recurrence({})

    refact_add_recurrence({})
    rf2 = refact_add_recurrence({})

    assert r2 != rf2, f"Trap failed: {r2} == {rf2}"
    print(f"schedule_builder OK: orig={r2}, refactored={rf2}")


if __name__ == "__main__":
    print("Running scripted verification of specimen traps...")
    try:
        verify_invoice_totals()
        verify_log_digester()
        verify_schedule_builder()
        print("All specimens verified successfully.")
    except AssertionError as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
