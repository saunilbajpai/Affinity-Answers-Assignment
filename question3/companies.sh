#!/usr/bin/env bash

# ==============================================================================
# S&P 500 Companies Data Processor
#
# Description:
#   Retrieves a CSV dataset of S&P 500 companies from a user-supplied URL,
#   extracts Company Name, Headquarters Location, and Founding Year,
#   sorts the records chronologically by Founding Year, and displays the
#   output in a clean, formatted table.
#
# Usage:
#   ./companies.sh <DATASET_URL>
# ==============================================================================

# Enable strict mode: exit immediately if a command exits with non-zero status
set -euo pipefail

# ------------------------------------------------------------------------------
# 1. Validate Command-Line Arguments
# ------------------------------------------------------------------------------
if [ "$#" -lt 1 ] || [ -z "$1" ]; then
    echo "Error: Dataset URL argument is missing." >&2
    echo "Usage: $0 <DATASET_URL>" >&2
    exit 1
fi

DATASET_URL="$1"

# ------------------------------------------------------------------------------
# 2. Check for Required Utilities
# ------------------------------------------------------------------------------
if command -v curl >/dev/null 2>&1; then
    FETCH_CMD="curl -sSL --fail"
elif command -v wget >/dev/null 2>&1; then
    FETCH_CMD="wget -qO-"
else
    echo "Error: Neither 'curl' nor 'wget' is available on this system." >&2
    exit 1
fi

# Determine python command (python3 or python)
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    PYTHON_CMD=""
fi

# ------------------------------------------------------------------------------
# 3. Retrieve CSV Data
# ------------------------------------------------------------------------------
echo "Fetching dataset from: ${DATASET_URL} ..." >&2

# Create a temporary file to store fetched CSV data
TEMP_CSV=$(mktemp 2>/dev/null || mktemp -t 'sp500_csv')
trap 'rm -f "$TEMP_CSV"' EXIT

if ! $FETCH_CMD "$DATASET_URL" > "$TEMP_CSV"; then
    echo "Error: Failed to retrieve dataset from ${DATASET_URL}" >&2
    exit 1
fi

# Verify file is not empty
if [ ! -s "$TEMP_CSV" ]; then
    echo "Error: Retrieved CSV dataset is empty." >&2
    exit 1
fi

# ------------------------------------------------------------------------------
# 4. Process, Extract, Sort, and Format Data
# ------------------------------------------------------------------------------
if [ -n "$PYTHON_CMD" ]; then
    # Robust processing using Python's built-in csv module for quotes & commas handling
    "$PYTHON_CMD" - "$TEMP_CSV" << 'EOF'
import sys
import csv
import re

csv_file = sys.argv[1]

def extract_primary_year(founded_str):
    """
    Extracts a 4-digit year for sorting purposes.
    Handles values like '1902', '2013 (1888)', '1904/1946/1959', etc.
    """
    if not founded_str:
        return 9999
    # Find all 4-digit years in the string
    matches = re.findall(r'\b\d{4}\b', founded_str)
    if matches:
        # Return the earliest year mentioned (e.g. 1888 in '2013 (1888)')
        return min(int(y) for y in matches)
    return 9999

records = []

try:
    with open(csv_file, mode='r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            sys.exit(0)

        for row in reader:
            if len(row) >= 8:
                company = row[1].strip()
                location = row[4].strip()
                founded = row[7].strip()
                sort_year = extract_primary_year(founded)
                records.append((sort_year, company, location, founded))
except Exception as e:
    print(f"Error processing CSV data: {e}", file=sys.stderr)
    sys.exit(1)

# Sort chronologically by founding year
records.sort(key=lambda x: (x[0], x[1]))

# Output header
print(f"{'Founding Year':<18} | {'Company Name':<45} | {'Headquarters Location'}")
print("-" * 95)

for _, company, location, founded in records:
    print(f"{founded:<18} | {company:<45} | {location}")
EOF

else
    # Fallback using standard AWK if Python is unavailable
    awk -F',' '
    BEGIN {
        FPAT = "([^,]+)|(\"[^\"]+\")"
        printf "%-18s | %-45s | %s\n", "Founding Year", "Company Name", "Headquarters Location"
        print "-----------------------------------------------------------------------------------------"
    }
    NR > 1 {
        # Strip quotes if present
        gsub(/^"|"$/, "", $2)
        gsub(/^"|"$/, "", $5)
        gsub(/^"|"$/, "", $8)
        company = $2
        location = $5
        founded = $8
        if (company != "") {
            printf "%-18s | %-45s | %s\n", founded, company, location
        }
    }
    ' "$TEMP_CSV" | sort -t'|' -k1,1n
fi
