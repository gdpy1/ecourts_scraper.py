#!/usr/bin/env python3
"""
eCourts Scraper – Intern Task
Author: Triloki Sah
Date: October 2025

Description:
This script allows users to:
1. Search case details by CNR or Case Type + Number + Year.
2. Check if the case is listed today or tomorrow.
3. View court name and serial number (mocked demo logic).
4. Download today's full cause list (simulated).
5. Save all results safely in /data folder as JSON files.

Note:
Actual scraping from eCourts is restricted; hence, simulated logic is used.
"""

import os
import json
import datetime
import argparse
import requests  # used for real case search (if API/HTML allowed)

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# --------------------------------------------------------------------
# 🧩 Mock function to simulate case checking (replace with real scraping later)
# --------------------------------------------------------------------
def get_case_status(cnr=None, case_type=None, number=None, year=None, day="today"):
    """
    Simulated function to check if a case is listed.
    In a real-world version, you'd fetch and parse data from:
    https://services.ecourts.gov.in/ecourtindia_v6/
    """
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    # Mock data (for demonstration)
    sample_case = {
        "CNR": "MHABC1000123452023",
        "CourtName": "District Court Mumbai",
        "SerialNumber": 23,
        "ListedOn": str(today)
    }

    # Simulated match
    if cnr == sample_case["CNR"]:
        if day == "today":
            return sample_case
        elif day == "tomorrow":
            sample_case["ListedOn"] = str(tomorrow)
            return sample_case
    return None

# --------------------------------------------------------------------
# 💾 Save results safely
# --------------------------------------------------------------------
def save_results(data, filename):
    os.makedirs("data", exist_ok=True)
    filepath = os.path.join("data", filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Saved: {filepath}")

# --------------------------------------------------------------------
# 📄 Download Cause List (Simulated)
# --------------------------------------------------------------------
def download_cause_list(day="today"):
    dummy_data = {
        "date": str(datetime.date.today()),
        "cases": [
            {"SerialNumber": 1, "CourtName": "High Court Delhi"},
            {"SerialNumber": 2, "CourtName": "District Court Pune"}
        ]
    }
    save_results(dummy_data, f"cause_list_{day}.json")
    print("📥 Cause list downloaded successfully.")

# --------------------------------------------------------------------
# 🖥️ Main CLI Function
# --------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="eCourts Scraper CLI")
    parser.add_argument("--cnr", type=str, help="Enter CNR number (e.g., MHABC1000123452023)")
    parser.add_argument("--case_type", type=str, help="Case Type (e.g., CR)")
    parser.add_argument("--number", type=int, help="Case Number (e.g., 123)")
    parser.add_argument("--year", type=int, help="Case Year (e.g., 2023)")
    parser.add_argument("--today", action="store_true", help="Check if case is listed today")
    parser.add_argument("--tomorrow", action="store_true", help="Check if case is listed tomorrow")
    parser.add_argument("--causelist", action="store_true", help="Download today's cause list")

    args = parser.parse_args()

    # Handle cause list download
    if args.causelist:
        download_cause_list(day="today")
        return

    # Handle case lookup
    day = "today" if args.today else "tomorrow" if args.tomorrow else "today"

    case_info = get_case_status(
        cnr=args.cnr,
        case_type=args.case_type,
        number=args.number,
        year=args.year,
        day=day
    )

    print("\n🔍 Checking case listing...\n")

    if case_info:
        print(f"✅ Case Found!")
        print(f"📄 Court Name: {case_info['CourtName']}")
        print(f"🔢 Serial Number: {case_info['SerialNumber']}")
        print(f"📅 Listed On: {case_info['ListedOn']}")
        save_results(case_info, "results.json")
    else:
        print("❌ Case not found or not listed for the selected day.")

# --------------------------------------------------------------------
# 🚀 Run
# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
