from src.ingestion.sample_data_generator import generate_sample_data
from src.processing.clean_history import clean_history


def test_pipeline():
    df = generate_sample_data(50)
    clean_df = clean_history(df)

    assert not clean_df.empty
    assert "date" in clean_df.columns
    assert "result" in clean_df.columns
