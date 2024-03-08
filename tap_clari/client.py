"""REST client handling, including ClariStream base class."""

from __future__ import annotations

import typing as t
from typing import Any, Callable

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]


class ClariStream(RESTStream):
    """Clari stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.clari.com/v4"

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="apikey",
            value=self.config.get("api_key", ""),
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        return {}

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        return {
            # for forecast
            "timePeriod": self.config.get("time_period"),
            # "scopeId": "1905::MGR",
            "typesToExport": [
                "forecast",
                "quota",
                "forecast_updated",
                "adjustment",
                # "crm_total",
                # "crm_closed",
            ],
            # "currency": "USD",
            "exportFormat": "JSON",
        }

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: A raw :class:`requests.Response`

        Yields:
            One item for every item found in the response.
        """
        record = extract_jsonpath(self.records_jsonpath, input=response.json())
        yield from flatten_record(next(record))


def get_list_item_values(
    source_list: list, target_keys: list[str], search_pair: dict
) -> dict:
    """Return target items from a dict with a specific key value pair from an array of dicts."""
    if len(search_pair) > 1:
        raise ValueError("pair must be a dictionary with a single key value pair")
    for search_key, search_value in search_pair.items():
        target_dict = next(i for i in source_list if i[search_key] == search_value)
        return {k: v for k, v in target_dict.items() if k in target_keys}


def flatten_record(row: dict) -> list:
    """Flatten a nested dictionary."""
    entries = row.get("entries", [])
    fields = row.get("fields", [])
    time_frames = row.get("timeFrames", [])
    time_periods = row.get("timePeriods", [])
    users = row.get("users", [])

    new_entries = []
    for entry in entries:
        field = get_list_item_values(
            fields, ["fieldName"], {"fieldId": entry["fieldId"]}
        )
        time_frame = get_list_item_values(
            time_frames, ["startDate", "endDate"], {"timeFrameId": entry["timeFrameId"]}
        )
        time_period = get_list_item_values(
            time_periods,
            ["type", "label", "year", "startDate", "endDate", "crmId"],
            {"timePeriodId": entry["timePeriodId"]},
        )
        user = get_list_item_values(
            users,
            [
                "name",
                "email",
                "scopeId",
                "crmId",
                "hierarchyId",
                "hierarchyName",
                "parentHierarchyId",
                "parentHierarchyName",
            ],
            {"userId": entry["userId"]},
        )

        # prevent key clashes
        time_period["timePeriodStartDate"] = time_period.pop("startDate")
        time_period["timePeriodEndDate"] = time_period.pop("endDate")
        time_period["timePeriodCrmId"] = time_period.pop("crmId")
        time_period["timePeriodType"] = time_period.pop("type")
        time_period["timePeriodLabel"] = time_period.pop("label")
        time_frame["timeFrameStartDate"] = time_frame.pop("startDate")
        time_frame["timeFrameEndDate"] = time_frame.pop("endDate")
        user["userCrmId"] = user.pop("crmId")
        user["userName"] = user.pop("name")
        user["userEmail"] = user.pop("email")

        # merge dictionaries
        new_entries.append({**entry, **field, **time_frame, **time_period, **user})

    return new_entries
