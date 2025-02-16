import pytest
import os
import json
import sys
import matplotlib
from datetime import datetime

# Setează matplotlib să nu deschidă ferestre grafice
matplotlib.use('Agg')

# Adaugă directorul părinte în sys.path pentru a putea importa app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import save_transaction, generate_graph, generate_annual_report, generate_report, add_transaction, transactions_file

# Test for save_transaction
def test_save_transaction():
    if os.path.exists(transactions_file):
        os.remove(transactions_file)

    save_transaction(100, "Food", "EUR", str(datetime.now().date()))

    assert os.path.exists(transactions_file)
    with open(transactions_file, 'r') as file:
        transactions = file.readlines()
        assert len(transactions) == 1
        data = json.loads(transactions[0])
        assert data["amount"] == 100
        assert data["category"] == "Food"
        assert data["currency"] == "EUR"

# Test for generate_graph
def test_generate_graph():
    if not os.path.exists(transactions_file):
        with open(transactions_file, 'w') as file:
            file.write('{"amount": 100, "category": "Food", "currency": "EUR", "date": "2025-02-16"}\n')

    generate_graph()  # Testăm funcția

    assert os.path.exists(transactions_file)  # Verificăm că fișierul există

# Test for generate_annual_report
def test_generate_annual_report():
    if not os.path.exists(transactions_file):
        with open(transactions_file, 'w') as file:
            file.write('{"amount": 100, "category": "Food", "currency": "EUR", "date": "2025-02-16"}\n')

    year = 2025
    generate_annual_report(year)

    report_filename = f"annual_report_{year}.txt"
    assert os.path.exists(report_filename)

    with open(report_filename, 'r') as report_file:
        content = report_file.read()
        assert "Food" in content
        assert "2025" in content

# Test for generate_report
def test_generate_report():
    if not os.path.exists(transactions_file):
        with open(transactions_file, 'w') as file:
            file.write('{"amount": 100, "category": "Food", "currency": "EUR", "date": "2025-02-16"}\n')

    month, year = 2, 2025
    generate_report(month, year)

    report_filename = f"monthly_report_February_2025.txt"
    assert os.path.exists(report_filename)

    with open(report_filename, 'r') as report_file:
        content = report_file.read()
        assert "Food" in content
        assert "February" in content

# Test for add_transaction
def test_add_transaction():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    add_transaction()
    root.quit()
