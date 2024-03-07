"""Stream type classes for tap-clari."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

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

    primary_keys: t.ClassVar[list[str]] = ["timeFrames", "timePeriods"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("entries", th.ArrayType(th.ObjectType(
            th.Property("fieldId", th.StringType),
            th.Property("quotaValue", th.NumberType),
            th.Property("timeFrameId", th.StringType),
            th.Property("timePeriodId", th.StringType),
            th.Property("userId", th.StringType),
        ))),
        th.Property("fields", th.ArrayType(th.ObjectType(
            th.Property("fieldId", th.StringType),
            th.Property("fieldName", th.StringType),
            th.Property("fieldType", th.StringType),
        ))),
        th.Property("timeFrames", th.ArrayType(th.ObjectType(
            th.Property("endDate", th.DateType),
            th.Property("startDate", th.DateType),
            th.Property("timeFrameId", th.StringType),
        ))),
        th.Property("timePeriods", th.ArrayType(th.ObjectType(
            th.Property("crmId", th.StringType),
            th.Property("endDate", th.DateType),
            th.Property("label", th.StringType),
            th.Property("startDate", th.DateType),
            th.Property("timePeriodId", th.StringType),
            th.Property("type", th.StringType),
            th.Property("year", th.StringType),
        ))),
        th.Property("users", th.ArrayType(th.ObjectType(
            th.Property("crmId", th.StringType),
            th.Property("email", th.EmailType),
            th.Property("hierarchyId", th.StringType),
            th.Property("hierarchyName", th.StringType),
            th.Property("name", th.StringType),
            th.Property("parentHierarchyId", th.StringType),
            th.Property("parentHierarchyName", th.StringType),
            th.Property("scopeId", th.StringType),
            th.Property("userId", th.StringType),
        ))),
    ).to_dict()
