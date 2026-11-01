# 0004. VAT is rounded per line

- Status: accepted
- Date: 2026-11-01

## Context

An invoice can have many lines, each with its own VAT rate. Rounding the VAT of the whole invoice
once gives a different amount from rounding each line, and our customers' accounting systems
book VAT line by line. An invoice whose VAT does not equal the sum of its lines is rejected by
their imports.

## Decision

- A line's net amount is quantity times unit price, rounded to cents, half-even.
- A line's VAT is its net amount times its VAT rate, rounded to cents, half-even.
- The invoice's VAT is the sum of the rounded line VAT amounts. The sum is not rounded again.
- The invoice's gross amount is its net amount plus its VAT.
- All amounts are `Decimal`. A float never holds money.

## Consequences

The VAT of an invoice can differ by a cent from the VAT of its net total. That difference is
expected and is not a defect.
