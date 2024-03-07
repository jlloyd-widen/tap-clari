"""REST client handling, including ClariStream base class."""

from __future__ import annotations

from typing import Any, Callable

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
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
