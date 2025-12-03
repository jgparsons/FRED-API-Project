from app.collect_FRED_data import sofr_data

def test_sofr_december_1():
    # Loop through observations and find the 2025-12-01 entry
    value = None
    for observation in sofr_data["observations"]:
        if observation["date"] == "2025-12-01":
            value = float(observation["value"])
            break
    # Check the expected value
    assert value == 4.12
