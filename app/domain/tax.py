"""Invoice totals.

VAT is rounded as ADR 0004 decides: each line's VAT is rounded to cents, half-even, and the
invoice's VAT is the sum of the rounded line amounts. The sum is not rounded again.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal
from typing import Protocol

CENT = Decimal("0.01")


class TaxableLine(Protocol):
    quantity: Decimal
    unit_price: Decimal
    vat_rate: Decimal


@dataclass(frozen=True)
class Totals:
    net: Decimal
    vat: Decimal
    gross: Decimal


def line_net(line: TaxableLine) -> Decimal:
    return (line.quantity * line.unit_price).quantize(CENT, rounding=ROUND_HALF_EVEN)


def invoice_totals(lines: Iterable[TaxableLine]) -> Totals:
    lines = list(lines)
    net = sum((line_net(line) for line in lines), Decimal("0.00"))
    vat = sum((line_net(line) * line.vat_rate for line in lines), Decimal("0"))
    vat = vat.quantize(CENT, rounding=ROUND_HALF_UP)
    return Totals(net=net, vat=vat, gross=net + vat)
