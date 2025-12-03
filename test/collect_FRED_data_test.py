from app.collect_FRED_data import collect_FRED_data


def test_collect_fred_data_runs():
    data = collect_FRED_data()  # should not crash
    assert len(data) == 6

