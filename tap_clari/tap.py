"""Clari tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_clari import streams


class TapClari(Tap):
    """Clari tap class."""

    name = "tap-clari"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the Clari API",
        ),
        th.Property(
            "time_period",
            th.StringType,
            required=False,
            description="Fiscal Quarter for when you'd like to run your export. Must "
                        "be passed in as a string (e.g. 'YYYY_QQ'). Defaults to the "
                        "current quarter.",
        ),
        th.Property(
            "forecast_ids",
            th.ArrayType(th.StringType),
            required=True,
            description="An array of IDs of the Forecast Tabs you would like to "
                        "export data from.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.ClariStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        stream_list: list[streams.ClariStream] = []
        for forecast_id in self.config.get("forecast_ids"):
            stream_list.append(streams.ForecastStream(self, forecast_id=forecast_id))
        return stream_list


if __name__ == "__main__":
    TapClari.cli()
