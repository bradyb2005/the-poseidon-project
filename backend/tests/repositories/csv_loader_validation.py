from backend.repositories.csv_loader import default_csv_path, load_csv, validate_csv


def test_csv_loader_can_load_rows():
    rows = load_csv()
    assert isinstance(rows, list)
    assert len(rows) > 0


def test_csv_loader_validation_passes():
    ok, errors = validate_csv()
    assert ok is True, f"Validation failed: {errors}"


def test_csv_path_exists():
    path = default_csv_path()
    assert path.endswith("food_delivery.csv")