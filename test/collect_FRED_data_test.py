# test/collect_FRED_data_test.py

from unittest.mock import patch
import datetime

from app.collect_FRED_data import collect_FRED_data

FAKE_RESPONSE = {
    "observations": [
        {"date": "2025-12-02", "value": "5.01"},
        {"date": "2025-12-03", "value": "5.00"},
    ]
}


@patch("app.collect_FRED_data.requests.get")
def test_collect_fred_data_uses_latest_value_when_today_missing(mock_get):
    # Make all API calls return fake data
    mock_get.return_value.json.return_value = FAKE_RESPONSE

    data = collect_FRED_data()

    # Structure: 5 values + chart_data + effr_date + effr_label
    assert len(data) == 8

    (
        onrrp_val,
        effr_val,
        iorb_val,
        sofr_val,
        srf_val,
        chart_data,
        effr_date,
        effr_label,
    ) = data

    # Last observation in FAKE_RESPONSE has value 5.00
    assert onrrp_val == 5.00
    assert effr_val == 5.00
    assert iorb_val == 5.00
    assert sofr_val == 5.00
    assert srf_val == 5.00

    # chart_data should be a dict with expected keys
    assert isinstance(chart_data, dict)
    for key in ["date", "ON_RRP", "EFFR", "IORB", "SOFR", "SRF"]:
        assert key in chart_data

    # Date parsed correctly
    assert isinstance(effr_date, datetime.date)
    assert effr_date == datetime.date(2025, 12, 3)

    # Since fake date is not "today", label is Latest value
    assert effr_label == "Latest value"
