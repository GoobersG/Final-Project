import pytest
from unittest.mock import MagicMock, patch
import sqlite3
import os
from datetime import datetime
from tkinter import Tk
from project import (
    create_tbl,
    check_item,
    generate_random_id,
    display_items,
    save_inventory,
)


@pytest.fixture
def setup_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    create_tbl(c)
    yield c, conn
    conn.close()


def test_create_tbl(setup_db):
    c, _ = setup_db
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
    assert c.fetchone() is not None


def test_check_item_valid(setup_db):
    c, _ = setup_db
    result = check_item(c, "Test Item", "Description", "10", "1234567890", MagicMock())
    assert result is True


def test_check_item_invalid_id(setup_db):
    c, _ = setup_db
    result = check_item(c, "Test Item", "Description", "10", "12345", MagicMock())
    assert result is False


@pytest.fixture
def setup_db():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE inventory (item_id TEXT PRIMARY KEY)")
    yield cursor, connection
    connection.close()


def test_generate_random_id(setup_db):
    cursor, _ = setup_db
    random_id = generate_random_id(cursor)
    assert len(random_id) == 10
    cursor.execute("SELECT item_id FROM inventory WHERE item_id = ?", (random_id,))
    assert cursor.fetchone() is None


@pytest.fixture
def setup_db():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE inventory (item_id TEXT PRIMARY KEY, item_name TEXT, item_description TEXT, item_quantity TEXT)"
    )
    yield cursor, connection
    connection.close()


def test_display_items(setup_db):
    cursor, _ = setup_db
    cursor.execute(
        "INSERT INTO inventory (item_id, item_name, item_description, item_quantity) VALUES (?, ?, ?, ?)",
        ("1234567890", "Test Item", "Description", "10"),
    )
    tree = MagicMock()
    tree.get_children.return_value = ["item1", "item2"]
    display_items("Test Item", cursor, tree)
    assert tree.delete.called
    assert tree.delete.call_count == 2
    assert tree.insert.called


@patch("project.webbrowser.open_new")
@patch("project.messagebox.askquestion")
@patch("project.fetch_data_from_db")
@patch("project.FPDF")
def test_save_inventory(
    mock_FPDF, mock_fetch_data_from_db, mock_askquestion, mock_open_new
):
    mock_pdf = MagicMock()
    mock_FPDF.return_value = mock_pdf
    mock_fetch_data_from_db.return_value = [
        ["Item1", "Description1", 10, "ID1"],
        ["Item2", "Description2", 5, "ID2"],
    ]
    mock_askquestion.return_value = "yes"
    save_inventory()
    mock_FPDF.assert_called_once()
    mock_pdf.add_page.assert_called_once()
    mock_pdf.image.assert_called_once_with(r"Logos\PyVentory.png", 170, 10, 30)
    mock_pdf.set_xy.assert_called_with(0, 10)
    mock_pdf.set_font.assert_any_call("Helvetica", "B", 16)
    mock_pdf.cell.assert_any_call(40, 10, "Name", 1, align="C")
    mock_pdf.cell.assert_any_call(40, 10, "Description", 1, align="C")
    mock_pdf.cell.assert_any_call(40, 10, "Quantity", 1, align="C")
    mock_pdf.cell.assert_any_call(40, 10, "ID", 1, align="C")
    mock_pdf.ln.assert_any_call()
    today = datetime.today().strftime("%Y-%m-%d")
    expected_pdf_file = f"inventory_{today}.pdf"
    mock_pdf.output.assert_called_once_with(expected_pdf_file)
    mock_askquestion.assert_called_once_with(
        "Success",
        f"PDF has been created successfully: {expected_pdf_file}. Would you like to open it?",
        icon="info",
    )
    mock_open_new.assert_called_once_with(expected_pdf_file)
    if os.path.exists(expected_pdf_file):
        os.remove(expected_pdf_file)
