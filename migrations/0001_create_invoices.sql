CREATE TABLE invoices (
    id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    cust_ref TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX ix_invoices_created_at ON invoices (created_at, id);
