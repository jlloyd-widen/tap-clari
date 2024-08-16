"""Tests standard tap features using the built-in SDK tests library."""
from unittest.mock import Mock

import pytest

from tap_clari.streams import ForecastStream, OpportunityStream

CONFIG = {
    "api_key": "test",
    "forecast_ids": ["1"],
    "opp_ids": ["opp_id_1", "opp_id_2"],
}


# # Run standard built-in tap tests from the SDK:
# TestTapClari = get_tap_test_class(
#     tap_class=TapClari,
#     config=CONFIG,
# )


# fs = ForecastStream(tap=TestTapClari, forecast_id="1")
sl = [
    {"id": 1, "name": "one", "other": "foo"},
    {"id": 2, "name": "two", "other": "bar"},
    {"id": 3, "name": "three", "other": "baz"},
]


@pytest.fixture
def forecast_stream():
    mock_tap = Mock()
    mock_tap.logger = Mock()
    mock_tap.config = CONFIG
    return ForecastStream(tap=mock_tap, forecast_id="test_forecast_stream")


@pytest.fixture
def opportunity_stream():
    mock_tap = Mock()
    mock_tap.logger = Mock()
    mock_tap.config = CONFIG
    return OpportunityStream(tap=mock_tap)


def test_get_list_item_values_multiple(forecast_stream):
    """Test the get_list_item_values function."""
    res = forecast_stream.get_list_item_values(sl, ["name", "other"], {"id": 1})
    assert res == {"name": "one", "other": "foo"}


def test_get_list_item_values_one(forecast_stream):
    """Test the get_list_item_values function."""
    res = forecast_stream.get_list_item_values(sl, ["name"], {"id": 1})
    assert res == {"name": "one"}


def test_get_list_item_values_raise(forecast_stream):
    """Test that oversized search_pair raise an ValueError."""
    try:
        forecast_stream.get_list_item_values(sl, ["name"], {"id": 1, "other": "foo"})
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"


def test_forecast_flatten_record(forecast_stream):
    """Test the flatten_record function."""
    record = {
        "entries": [
            {'fieldId': 'field_id_1',
             'quotaValue': None,
             'timeFrameId': 'TF:2024-03-01',
             'timePeriodId': '2024_Q1',
             'userId': 'user_id_1'},
            {'fieldId': 'field_id_2',
             'quotaValue': None,
             'timeFrameId': 'TF:2024-03-01',
             'timePeriodId': '2024_Q1',
             'userId': 'user_id_1'}
        ],
        'users': [{'crmId': 'crm_id_1',
                   'email': 'name_1@example.com',
                   'hierarchyId': 'bar',
                   'hierarchyName': 'spam',
                   'name': 'name_1',
                   'parentHierarchyId': 'foo',
                   'parentHierarchyName': 'eggs',
                   'scopeId': '{"type":"blah"}',
                   'userId': 'user_id_1'},
                  {'crmId': 'crm_id_2',
                   'email': 'name_2@example.com',
                   'hierarchyId': 'bar',
                   'hierarchyName': 'spam',
                   'name': 'name_2',
                   'parentHierarchyId': 'foo',
                   'parentHierarchyName': 'eggs',
                   'scopeId': '{"type":"blah"}',
                   'userId': 'user_id_2'},
        ],
        'timePeriods': [{'crmId': 'crm_id_3',
                         'endDate': '2024-03-31',
                         'label': 'Q1',
                         'startDate': '2024-01-01',
                         'timePeriodId': '2024_Q1',
                         'type': 'quarter',
                         'year': '2024'}],
        'fields': [
                   {'fieldId': 'field_id_2',
                    'fieldName': 'field_name_2',
                    'fieldType': 'quota'},
                   {'fieldId': 'field_id_3',
                    'fieldName': 'field_name_3',
                    'fieldType': 'bar'},
                   {'fieldId': 'field_id_1',
                    'fieldName': 'field_name_1',
                    'fieldType': 'bar'},
        ],
        'timeFrames': [{'endDate': '2024-03-07',
                        'startDate': '2024-03-01',
                        'timeFrameId': 'TF:2024-03-01'}],

    }
    res = forecast_stream.flatten_record(record)
    assert res == [
        {
            'fieldId': 'field_id_1',
            'fieldName': 'field_name_1',
            'quotaValue': None,
            'timeFrameId': 'TF:2024-03-01',
            'timeFrameStartDate': '2024-03-01',
            'timeFrameEndDate': '2024-03-07',
            'timePeriodCrmId': 'crm_id_3',
            'timePeriodType': 'quarter',
            'timePeriodLabel': 'Q1',
            'year': '2024',
            'timePeriodStartDate': '2024-01-01',
            'timePeriodEndDate': '2024-03-31',
            'timePeriodId': '2024_Q1',
            'userId': 'user_id_1',
            'userName': 'name_1',
            'userEmail': 'name_1@example.com',
            'scopeId': '{"type":"blah"}',
            'userCrmId': 'crm_id_1',
            'hierarchyId': 'bar',
            'hierarchyName': 'spam',
            'parentHierarchyId': 'foo',
            'parentHierarchyName': 'eggs',
        },
        {
            'fieldId': 'field_id_2',
            'fieldName': 'field_name_2',
            'quotaValue': None,
            'timeFrameId': 'TF:2024-03-01',
            'timeFrameStartDate': '2024-03-01',
            'timeFrameEndDate': '2024-03-07',
            'timePeriodCrmId': 'crm_id_3',
            'timePeriodType': 'quarter',
            'timePeriodLabel': 'Q1',
            'year': '2024',
            'timePeriodStartDate': '2024-01-01',
            'timePeriodEndDate': '2024-03-31',
            'timePeriodId': '2024_Q1',
            'userId': 'user_id_1',
            'userName': 'name_1',
            'userEmail': 'name_1@example.com',
            'scopeId': '{"type":"blah"}',
            'userCrmId': 'crm_id_1',
            'hierarchyId': 'bar',
            'hierarchyName': 'spam',
            'parentHierarchyId': 'foo',
            'parentHierarchyName': 'eggs',
        },
    ]
