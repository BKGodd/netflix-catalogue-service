"""
Created by: Brandon Goddard
Description: This module is for testing the database module,
             which handles Elasticsearch interactions.
"""
from ..app.database import filter_row, filter_text, filter_dates, filter_strings
from .constants import MOCK_CSV_ROW

def test_filtering():
    """
    Test the filtering function for database insertion.

    Returns:
        None
    """
    row = MOCK_CSV_ROW.copy()
    filter_strings(row)
    filter_dates(row)
    filter_row(row)

    # Assert transformations
    assert row['type'] == 1
    assert row['title'] == 'The Starling'
    assert row['director'] == 'Theodore Melfi'
    assert row['cast'] == ['Melissa McCarthy', "Chris O'Dowd", 'Kevin Kline',
                           'Timothy Olyphant', 'Daveed Diggs', 'Skyler Gisondo',
                           'Laura Harrier', 'Rosalind Chao', 'Kimberly Quinn',
                           'Loretta Devine', 'Ravi Kapoor']
    assert row['genres'] == ['Comedies', 'Dramas']
    assert row['date_added'] == '09242021'
    assert row['release_year'] == 2021
    assert row['rating'] == 0
    assert row['duration'] == 104
    assert row['description'] == ("A woman adjusting to life after a loss "
                                  "contends with a feisty bird that's taken "
                                  "over her garden - and a husband who's "
                                  "struggling to find a way forward.")


def test_filter_text():
    """
    Test the filtering text function for
    removing punctuations and accents.

    Returns:
        None
    """
    text_to_filter = "Hello éàççè!? Name's Band-aid, James Band-aid."
    text_with_punct = "Hello eacce!? Name's Band-aid, James Band-aid."
    text_fully_filtered = "Hello eacce Name's Band-aid, James Band-aid"

    # Test with only accents removed
    filtered_text = filter_text(text_to_filter, punct=False)
    assert filtered_text == text_with_punct

    # Test with both punctuations and accents removed
    filtered_text = filter_text(text_to_filter)
    assert filtered_text == text_fully_filtered
