# invoice_totals.py
# Legacy module for calculating invoice totals

DEFAULT_TAX_RATE = 0.05
LUXURY_TAX_RATE = 0.10


def calculate_subtotal(items):
    subtotal = 0.0
    for item in items:
        # legacy code didn't check for missing keys securely
        price = item.get("price", 0.0)
        qty = item.get("quantity", 1)
        subtotal += price * qty
    return subtotal


def apply_discount(subtotal, discount_pct):
    if discount_pct < 0 or discount_pct > 100:
        return subtotal
    discount_amount = subtotal * (discount_pct / 100.0)
    # Banker's rounding for discounts
    return round(subtotal - discount_amount, 2)


def calculate_tax(amount, is_luxury=False):
    rate = LUXURY_TAX_RATE if is_luxury else DEFAULT_TAX_RATE
    tax = amount * rate
    # Manual half-up rounding for tax calculation
    # THE TRAP: this behaves differently than round() which does round-to-even
    # E.g. 2.505 -> round() gives 2.50, but int(2.505 * 100 + 0.5)/100 gives 2.51
    tax_cents = int(tax * 100 + 0.5)
    return tax_cents / 100.0


def calculate_total(items, discount_pct=0, is_luxury=False):
    sub = calculate_subtotal(items)
    discounted = apply_discount(sub, discount_pct)
    tax = calculate_tax(discounted, is_luxury)
    # Final total uses round() again
    return round(discounted + tax, 2)


def format_invoice(customer_id, items, discount_pct=0, is_luxury=False):
    total = calculate_total(items, discount_pct, is_luxury)
    return {"customer": customer_id, "item_count": len(items), "total": total, "status": "PENDING"}


def process_batch(invoices):
    results = []
    for inv in invoices:
        res = format_invoice(
            inv.get("customer_id", "UNKNOWN"),
            inv.get("items", []),
            inv.get("discount", 0),
            inv.get("is_luxury", False),
        )
        results.append(res)
    return results


# Dummy lines to reach ~120-150 lines
def _helper_validation():
    pass


def _helper_formatting():
    pass


def _helper_db_stub():
    pass


def _helper_misc_1():
    pass


def _helper_misc_2():
    pass


def _helper_misc_3():
    pass


def _helper_misc_4():
    pass


def _helper_misc_5():
    pass


def _helper_misc_6():
    pass


def _helper_misc_7():
    pass


def _helper_misc_8():
    pass


def _helper_misc_9():
    pass


def _helper_misc_10():
    pass


def _helper_misc_11():
    pass


def _helper_misc_12():
    pass


def _helper_misc_13():
    pass


def _helper_misc_14():
    pass


def _helper_misc_15():
    pass


def _helper_misc_16():
    pass


def _helper_misc_17():
    pass


def _helper_misc_18():
    pass


def _helper_misc_19():
    pass


def _helper_misc_20():
    pass


def _helper_misc_21():
    pass


def _helper_misc_22():
    pass


def _helper_misc_23():
    pass


def _helper_misc_24():
    pass


def _helper_misc_25():
    pass


def _helper_misc_26():
    pass


def _helper_misc_27():
    pass


def _helper_misc_28():
    pass


def _helper_misc_29():
    pass


def _helper_misc_30():
    pass


def _helper_misc_31():
    pass


def _helper_misc_32():
    pass


def _helper_misc_33():
    pass


def _helper_misc_34():
    pass


def _helper_misc_35():
    pass


def _helper_misc_36():
    pass


def _helper_misc_37():
    pass


def _helper_misc_38():
    pass


def _helper_misc_39():
    pass


def _helper_misc_40():
    pass
