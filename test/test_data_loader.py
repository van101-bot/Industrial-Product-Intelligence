from src.data_loader import load_input_data, load_expected_output


def test_input_dataset():
    df = load_input_data()

    assert len(df) == 1000
    assert len(df.columns) == 6


def test_expected_output_dataset():
    df = load_expected_output()

    assert len(df) == 2
    assert len(df.columns) == 252