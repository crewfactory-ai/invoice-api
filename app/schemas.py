from datetime import date
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

InvoiceStatus = Literal["draft", "issued", "paid", "void"]


class InvoiceLineIn(BaseModel):
    description: str = Field(min_length=1, max_length=200)
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=3)
    unit_price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    vat_rate: Decimal = Field(ge=0, le=1, decimal_places=4)


class InvoiceIn(BaseModel):
    customer_name: str = Field(min_length=1, max_length=200)
    cust_ref: str | None = Field(default=None, max_length=64)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    status: InvoiceStatus = "draft"
    issue_date: date
    due_date: date
    lines: list[InvoiceLineIn] = Field(min_length=1, max_length=100)


class InvoiceLineOut(InvoiceLineIn):
    net: Decimal


class InvoiceOut(BaseModel):
    id: UUID
    customer_name: str
    cust_ref: str | None
    currency: str
    status: InvoiceStatus
    issue_date: date
    due_date: date
    lines: list[InvoiceLineOut]
    net: Decimal
    vat: Decimal
    gross: Decimal


class InvoicePage(BaseModel):
    items: list[InvoiceOut]
    offset: int
    limit: int
    total: int


class ErrorOut(BaseModel):
    code: str
    message: str
