# Task 2 — SQL and Database

This task uses the public Rfam MySQL database to answer three
questions involving taxonomy, sequence information, and Rfam families.

## Database

The queries use the public Rfam MySQL database.

Host: `mysql-rfam-public.ebi.ac.uk`
Port: `4497`
Database: `Rfam`
User: `rfamro`

Database documentation:
https://docs.rfam.org/en/latest/database.html

## Queries

### A — Acacia

Counts the distinct Acacia species present in the taxonomy table.

### B — Wheat

Joins `rfamseq` with `taxonomy` to identify the wheat type associated
with the longest DNA sequence.

### C — Rfam Families

Joins `family`, `full_region`, and `rfamseq` to find families whose
maximum DNA sequence length exceeds 1,000,000.

The results are sorted by maximum sequence length and paginated to
return page 9 with 15 results per page.

## Schema Relationships

taxonomy → rfamseq → full_region → family

The joins are based on the identifiers connecting these tables.

## Notes

The queries were written against the public Rfam schema and should
be checked against the current database release before execution.