# Currency Exchange & Fee Settlement (`currency_exchange.ts`)

## The Trap
In JavaScript and TypeScript:
- `Math.round(-1.5)` evaluates to `-1` (rounds towards positive infinity) instead of `-2` (symmetric half-up away from zero).
- In financial debit calculations (refund fees, negative adjustments), replacing the legacy symmetric integer-floor conversion `(sign * Math.floor(Math.abs(v) * 100 + 0.5)) / 100` with standard `Math.round(v * 100) / 100` shifts fees on negative and refund transactions by exactly 1 cent.
- In addition, standard floating-point accumulation on consecutive conversions produces drift without cent quantization.

## Specimen Structure
- **Functions:** `getExchangeRate`, `roundHalfUpCents`, `calculateFee`, `convertCurrency`, `processBatchSettlement`
- **Language:** TypeScript / JavaScript (Node runtime)
- **Line Count:** ~120 lines
