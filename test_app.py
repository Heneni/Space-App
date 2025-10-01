import pandas as pd

def test_csv_load():
    url = "https://storage.googleapis.com/workthisfucker/THEHISTORYORACLE.csv"
    df = pd.read_csv(url)
    assert not df.empty
    assert "track" in df.columns
    assert "date" in df.columns
    assert "artist" in df.columns
