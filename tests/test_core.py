"""Tests standard tap features using the built-in SDK tests library."""

from tap_clari.client import get_list_item_values, flatten_record

# SAMPLE_CONFIG = {
#     "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
#     # TODO: Initialize minimal tap config
# }
#
#
# # Run standard built-in tap tests from the SDK:
# TestTapClari = get_tap_test_class(
#     tap_class=TapClari,
#     config=SAMPLE_CONFIG,
# )


sl = [
    {"id": 1, "name": "one", "other": "foo"},
    {"id": 2, "name": "two", "other": "bar"},
    {"id": 3, "name": "three", "other": "baz"},
]

def test_get_list_item_values_multiple():
    """Test the get_list_item_values function."""
    res = get_list_item_values(sl, ["name", "other"], {"id": 1})
    assert res == {"name": "one", "other": "foo"}


def test_get_list_item_values_one():
    """Test the get_list_item_values function."""
    res = get_list_item_values(sl, ["name"], {"id": 1})
    assert res == {"name": "one"}


def test_get_list_item_values_raise():
    """Test that oversized search_pair raise an ValueError."""
    try:
        get_list_item_values(sl, ["name"], {"id": 1, "other": "foo"})
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"


def test_flatten_record():
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
    res = flatten_record(record)
    assert res == {
        "entries": [
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
    }
