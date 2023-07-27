import pytest
from ..app.database import filter_row, get_row, filter_text
from .constants import MOCK_CSV_ROW

def test_filter_row():
    row = MOCK_CSV_ROW.copy()
    filter_row(row)

    # Assert transformations
    assert row['type'] == 1
    assert row['title'] == 'The Starling'
    assert row['director'] == 'Theodore Melfi'
    assert row['cast'] == ['Melissa McCarthy', "Chris ODowd", 'Kevin Kline',
                           'Timothy Olyphant', 'Daveed Diggs', 'Skyler Gisondo',
                           'Laura Harrier', 'Rosalind Chao', 'Kimberly Quinn',
                           'Loretta Devine', 'Ravi Kapoor']
    assert row['genres'] == ['Comedies', 'Dramas']
    assert row['date_added'] == '09242021'
    assert row['release_year'] == 2021
    assert row['rating'] == 0
    assert row['duration'] == 104
    assert row['description'] == ("A woman adjusting to life after a loss contends with a feisty bird "
                                  "that's taken over her garden - and a husband who's struggling to find a way forward.")


def test_filter_text():
    text_with_punctuations = "Sample, text! with punctuations?"
    text_with_accents = "Sample text with éàççè accents"
    text_with_both = "Sample, text! with éàççè accents?"
    
    # Test with punctuations removed
    filtered_text = filter_text(text_with_punctuations, punct=True)
    assert filtered_text == "Sample text with punctuations"

    # Test with accents removed
    filtered_text = filter_text(text_with_accents, accents=True)
    assert filtered_text == "Sample text with eacce accents"
    
    # Test with both punctuations and accents removed
    filtered_text = filter_text(text_with_both)
    assert filtered_text == "Sample text with eacce accents"
