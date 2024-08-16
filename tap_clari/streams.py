"""Stream type classes for tap-clari."""

from __future__ import annotations

import typing as t
from typing import Any

import requests
from singer_sdk import typing as th
from singer_sdk.helpers.jsonpath import extract_jsonpath

from tap_clari.client import ClariStream


class ForecastStream(ClariStream):
    """Define forecast stream."""

    def __init__(self, tap, forecast_id: str):
        super().__init__(
            tap,
            path=f"/forecast/{forecast_id}",
            name=f"{forecast_id}_forecast",
        )
        self.forecast_id = forecast_id

    primary_keys: t.ClassVar[list[str]] = [
        "fieldId",
        "timeFrameId",
        "timePeriodId",
        "userId",
    ]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("adjustmentValue", th.NumberType),
        th.Property("adjustedBy", th.StringType),
        th.Property("adjustedOn", th.NumberType),
        th.Property("aggregationTotal", th.NumberType),
        th.Property("fieldId", th.StringType),
        th.Property(
            "currency",
            th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("symbol", th.StringType),
            ),
        ),
        th.Property("quotaValue", th.NumberType),
        th.Property("isUpdated", th.BooleanType),
        th.Property("forecastValue", th.NumberType),
        th.Property("timeFrameId", th.StringType),
        th.Property("timePeriodId", th.StringType),
        th.Property("userId", th.StringType),
        th.Property("fieldName", th.StringType),
        th.Property("timeFrameEndDate", th.DateType),
        th.Property("timeFrameStartDate", th.DateType),
        th.Property("timePeriodCrmId", th.StringType),
        th.Property("timePeriodEndDate", th.DateType),
        th.Property("timePeriodLabel", th.StringType),
        th.Property("timePeriodStartDate", th.DateType),
        th.Property("timePeriodType", th.StringType),
        th.Property("year", th.StringType),
        th.Property("userCrmId", th.StringType),
        th.Property("userEmail", th.EmailType),
        th.Property("hierarchyId", th.StringType),
        th.Property("hierarchyName", th.StringType),
        th.Property("userName", th.StringType),
        th.Property("parentHierarchyId", th.StringType),
        th.Property("parentHierarchyName", th.StringType),
        th.Property("scopeId", th.StringType),
    ).to_dict()

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: A raw :class:`requests.Response`

        Yields:
            One item for every item found in the response.
        """
        record = extract_jsonpath(self.records_jsonpath, input=response.json())
        yield from self.flatten_record(next(record))

    @staticmethod
    def get_list_item_values(
        source_list: list, target_keys: list[str], search_pair: dict
    ) -> dict:
        """Return items from dict with a specific key value pair from array of dicts."""
        if len(search_pair) > 1:
            raise ValueError("pair must be a dictionary with a single key value pair")
        for search_key, search_value in search_pair.items():
            target_dict = next(i for i in source_list if i[search_key] == search_value)
            return {k: v for k, v in target_dict.items() if k in target_keys}

    def flatten_record(self, row: dict) -> list:
        """Flatten a nested dictionary."""
        entries = row.get("entries", [])
        fields = row.get("fields", [])
        time_frames = row.get("timeFrames", [])
        time_periods = row.get("timePeriods", [])
        users = row.get("users", [])

        new_entries = []
        for entry in entries:
            field = self.get_list_item_values(
                fields, ["fieldName"], {"fieldId": entry["fieldId"]}
            )
            time_frame = self.get_list_item_values(
                time_frames,
                ["startDate", "endDate"],
                {"timeFrameId": entry["timeFrameId"]},
            )
            time_period = self.get_list_item_values(
                time_periods,
                ["type", "label", "year", "startDate", "endDate", "crmId"],
                {"timePeriodId": entry["timePeriodId"]},
            )
            user = self.get_list_item_values(
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


class OpportunityStream(ClariStream):
    """Define stream."""

    name = "opportunity"
    path = "/opportunity"
    records_jsonpath = "$.opportunities.[*]"  # Or override `parse_response`.
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property(
            "fields",
            th.ArrayType(
                th.ObjectType(
                    th.Property("alias", th.StringType),
                    th.Property("id", th.StringType),
                    th.Property("value", th.AnyType),
                )
            ),
        ),
        th.Property("id", th.StringType),
    ).to_dict()

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
        opp_ids = self.config.get("opp_ids", [])
        if len(opp_ids) == 0:
            self.logger.info("No opportunity IDs provided. Exporting 0 opportunities.")
        return {"oppId": opp_ids}
