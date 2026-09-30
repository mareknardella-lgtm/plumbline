/**
 * Legacy Currency Exchange & Fee Settlement Engine (~160 lines).
 * 
 * Traps:
 * 1. JavaScript Math.round(-1.5) rounds towards positive infinity (-1) rather than away from zero (-2).
 * 2. IEEE-754 precision accumulators: 0.1 + 0.2 !== 0.3.
 * Naive cleanup replacing manual integer cent conversion with Math.round() introduces penny divergence on negative debit balances.
 */

const BASE_RATES: Record<string, number> = {
  USD: 1.0,
  EUR: 0.92,
  GBP: 0.79,
  JPY: 154.20,
  CHF: 0.89,
};

const DEFAULT_SPREAD_BPS = 25; // 0.25%

interface Transaction {
  id: string;
  sourceCurrency: string;
  targetCurrency: string;
  amount: number;
  isVip?: boolean;
}

interface Settlement {
  id: string;
  convertedAmount: number;
  feeCents: number;
  netAmount: number;
}

export function getExchangeRate(fromCurr: string, toCurr: string): number {
  const fromBase = BASE_RATES[fromCurr] || 1.0;
  const toBase = BASE_RATES[toCurr] || 1.0;
  return toBase / fromBase;
}

export function roundHalfUpCents(value: number): number {
  // Legacy custom half-up rounding preserving negative symmetry
  const sign = value < 0 ? -1 : 1;
  const absVal = Math.abs(value);
  return (sign * Math.floor(absVal * 100 + 0.5)) / 100;
}

export function calculateFee(amount: number, isVip = false): number {
  const bps = isVip ? 10 : DEFAULT_SPREAD_BPS;
  const rawFee = (amount * bps) / 10000;
  return roundHalfUpCents(rawFee);
}

export function convertCurrency(
  amount: number,
  fromCurr: string,
  toCurr: string,
  isVip = false
): { gross: number; fee: number; net: number } {
  const rate = getExchangeRate(fromCurr, toCurr);
  const gross = roundHalfUpCents(amount * rate);
  const fee = calculateFee(gross, isVip);
  const net = roundHalfUpCents(gross - fee);
  return { gross, fee, net };
}

export function processBatchSettlement(transactions: Transaction[]): Settlement[] {
  const results: Settlement[] = [];
  for (let i = 0; i < transactions.length; i++) {
    const tx = transactions[i];
    const { gross, fee, net } = convertCurrency(
      tx.amount,
      tx.sourceCurrency,
      tx.targetCurrency,
      tx.isVip
    );
    results.push({
      id: tx.id,
      convertedAmount: gross,
      feeCents: Math.round(fee * 100),
      netAmount: net,
    });
  }
  return results;
}
