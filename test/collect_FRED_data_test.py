from unittest.mock import patch
from app.collect_FRED_data import collect_FRED_data

FAKE_RESPONSE = {
    "observations": [
        {"date": "2025-12-03", "value": "5.00"},
        {"date": "2025-12-02", "value": "5.01"},
    ]
}

@patch("app.collect_FRED_data.requests.get")
def test_collect_fred_data_runs(mock_get):
    # Make all API calls return fake data
    mock_get.return_value.json.return_value = FAKE_RESPONSE

    data = collect_FRED_data()

    # Check structure
    assert len(data) == 6

    # Check extracted today's value
    assert data[0] == 5.0  # ON_RRP value
