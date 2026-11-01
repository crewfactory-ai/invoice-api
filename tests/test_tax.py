from dataclasses import dataclass
from decimal import Decimal

from app.domain.tax import invoice_totals, line_net


@dataclass
class Line:
    quantity: Decimal
    unit_price: Decimal
    vat_rate: Decimal


def line(quantity: str, unit_price: str, vat_rate: str) -> Line:
    return Line(Decimal(quantity), Decimal(unit_price), Decimal(vat_rate))


def test_line_net_is_quantity_times_unit_price():
    assert line_net(line("3", "19.99", "0.21")) == Decimal("59.97")


def test_line_net_rounds_half_even_to_cents():
    assert line_net(line("0.5", "0.15", "0")) == Decimal("0.08")
    assert line_net(line("0.5", "0.13", "0")) == Decimal("0.06")


def test_one_line_at_the_standard_rate():
    totals = invoice_totals([line("1", "100.00", "0.21")])

    assert (totals.net, totals.vat, totals.gross) == (
        Decimal("100.00"),
        Decimal("21.00"),
        Decimal("121.00"),
    )


def test_vat_is_rounded_to_cents():
    totals = invoice_totals([line("3", "19.99", "0.21")])

    assert totals.vat == Decimal("12.59")


def test_a_zero_rate_line_has_no_vat():
    totals = invoice_totals([line("1", "50.00", "0")])

    assert totals.vat == Decimal("0.00")


def test_lines_at_two_rates():
    totals = invoice_totals([line("1", "100.00", "0.21"), line("2", "20.00", "0.09")])

    assert (totals.net, totals.vat) == (Decimal("140.00"), Decimal("24.60"))


def test_gross_is_net_plus_vat():
    totals = invoice_totals([line("4", "12.35", "0.21"), line("1", "7.10", "0.09")])

    assert totals.gross == totals.net + totals.vat


def test_no_lines_have_zero_totals():
    totals = invoice_totals([])

    assert (totals.net, totals.vat, totals.gross) == (Decimal("0"), Decimal("0"), Decimal("0"))
