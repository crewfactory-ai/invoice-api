CREATE TABLE invoice_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id TEXT NOT NULL REFERENCES invoices (id),
    position INTEGER NOT NULL,
    description TEXT NOT NULL,
    quantity TEXT NOT NULL,
    unit_price TEXT NOT NULL,
    vat_rate TEXT NOT NULL
);

CREATE INDEX ix_invoice_lines_invoice_id ON invoice_lines (invoice_id);
