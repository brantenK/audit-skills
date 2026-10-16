"""Synthetic data only. Nothing here comes from a real client."""

from __future__ import annotations

import csv
import datetime as dt

import openpyxl
import pytest


@pytest.fixture(autouse=True)
def tool_home(tmp_path, monkeypatch):
    monkeypatch.setenv("AUDIT_SKILLS_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("HOME", str(tmp_path / "userhome"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "userhome"))
    return tmp_path


GL_ROWS = [
    # account, name, date, counterparty, reference, type, narrative, debit, credit
    ("8730/101", "Prepaid - Expo 2027", dt.date(2026, 4, 22), "Bank", "pmt", "Account Payment", "venue", 50000, 0),
    ("8730/101", "Prepaid - Expo 2027", dt.date(2026, 5, 2), "Venue Co", "SIV001", "Supplier Invoice", "deposit", 20000, 0),
    ("8730/102", "Prepaid - Summit 2026", dt.date(2026, 6, 5), "Bank", "pmt", "Account Payment", "venue", 8000, 0),
    ("8730/103", "Prepaid - Forum 2026", dt.date(2026, 6, 19), "Bank", "pmt", "Account Payment", "catering", 3000, 0),
    ("9100/101", "Income in advance - Expo 2027", dt.date(2026, 3, 1), "Sponsor A", "INV100", "Tax Invoice", "sponsor", 0, 90000),
    ("9100/101", "Income in advance - Expo 2027", dt.date(2026, 3, 9), "Sponsor B", "INV101", "Tax Invoice", "sponsor", 0, 30000),
    ("9100/101", "Income in advance - Expo 2027", dt.date(2026, 4, 1), "Sponsor B", "CR01", "Credit Note", "cancel", 5000, 0),
    ("9100/102", "Income in advance - Old event", dt.date(2025, 8, 20), "Journal", "JNL1", "Journal Entry", "release", 40000, 0),
]


@pytest.fixture
def gl_file(tmp_path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Account_Code", "Account_Name", "Date", "Counterparty", "Reference", "Txn_Type",
               "Narrative", "Debit", "Credit", "Net", "Month"])
    for r in GL_ROWS:
        ws.append(list(r) + [r[7] - r[8], r[2].strftime("%b %Y")])
    p = tmp_path / "gl.xlsx"
    wb.save(p)
    return p


@pytest.fixture
def tb_file(tmp_path):
    p = tmp_path / "tb.csv"
    with p.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Account", "Balance"])
        w.writerow(["8730/101", "70000"])
        w.writerow(["8730/102", "8000"])
        w.writerow(["8730/103", "3000"])
        w.writerow(["9100/101", "(140000)"])  # includes 25,000 opening balance
        w.writerow(["9100/102", "0"])
    return p


@pytest.fixture
def py_tb_file(tmp_path):
    p = tmp_path / "py_tb.csv"
    with p.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Account", "Balance"])
        w.writerow(["9100/101", "0"])        # auditor reclassified it away last year
        w.writerow(["9100/102", "(40000)"])
    return p


@pytest.fixture
def bank_file(tmp_path):
    p = tmp_path / "bank.csv"
    with p.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Date", "Description", "Debit", "Credit", "Source"])
        w.writerow(["2026-04-22", "PAYMENT TO - EXPO VENUE", "-50000.00", "0", "stmt-apr.pdf p7"])
        w.writerow(["2026-06-05", "TELETRANSMISSION OUTWARD - SUMMIT", "-8000.00", "0", "stmt-jun.pdf p4"])
        w.writerow(["2026-06-02", "PAYMENT TO - OTHER", "-3500.00", "0", "stmt-jun.pdf p2"])
    return p
