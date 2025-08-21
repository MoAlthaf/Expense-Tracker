from backend import db_helper


def test_fetch_expenses():
    expenses = db_helper.fetch_expenses("2024-08-02")
    assert len(expenses)==6




def test_fetch_expenses_invalid_date():
    expenses = db_helper.fetch_expenses("20200-08-32")
    assert len(expenses) == 0