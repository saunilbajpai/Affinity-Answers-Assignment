# Task 3 — Unix Shell Scripting (`companies.sh`)

## Overview
`companies.sh` is a Unix shell script that accepts a CSV dataset URL as a command-line argument, retrieves the dataset using `curl` (or `wget`), processes and parses company records, sorts them chronologically by founding year, and prints the result in a clean tabular format.

---

## Usage

```bash
./companies.sh <DATASET_URL>
```

### Example Execution:
```bash
./companies.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
```

---

## Features & Implementation

1. **Argument Validation**:
   - Ensures a URL argument is passed. If missing, displays error message and usage syntax on `stderr` and exits with code `1`.
2. **Dataset Retrieval & Error Handling**:
   - Uses `curl -sSL --fail` (or `wget -qO-`) to fetch CSV data.
   - Saves content to a temporary file created safely via `mktemp` and cleans up on exit via a `trap`.
   - Validates non-zero dataset file size and catches non-200 HTTP response codes.
3. **CSV Parsing & Column Extraction**:
   - Extracts 3 required fields:
     - `Company Name` (`Security`, 2nd field)
     - `Headquarters Location` (5th field)
     - `Founding Year` (`Founded`, 8th field)
   - Accurately handles quoted CSV fields with embedded commas (e.g. `"New York City, New York"`).
4. **Chronological Sorting**:
   - Extracts the primary 4-digit founding year (e.g., sorting `2013 (1888)` by `1888`).
   - Displays records sorted from oldest founding year to newest.
5. **Formatted Console Output**:
   - Outputs formatted columns (`Founding Year`, `Company Name`, `Headquarters Location`) with visual separator line.

---

## Sample Output

```text
Founding Year      | Company Name                                  | Headquarters Location
-----------------------------------------------------------------------------------------------
1784               | BNY Mellon                                    | New York City, New York
2005 (Molson 1786, Coors 1873) | Molson Coors Beverage Company                 | Chicago, Illinois
1792               | State Street Corporation                      | Boston, Massachusetts
2000 (1799 / 1871) | JPMorgan Chase                                | New York City, New York
2017 (1802)        | DuPont                                        | Wilmington, Delaware
1806               | Colgate-Palmolive                             | New York City, New York
1810               | Hartford (The)                                | Hartford, Connecticut
1818               | Bunge Global                                  | Chesterfield, Missouri
1823               | Consolidated Edison                           | New York City, New York
1825               | KeyCorp                                       | Cleveland, Ohio
```
