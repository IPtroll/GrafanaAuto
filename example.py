
import json
import logging
from typing import Dict

from grafanalib._gen import DashboardEncoder
from grafanalib.core import Dashboard

from grafana_client import GrafanaApi
from grafana_client.util import setup_logging

logger = logging.getLogger(__name__)


def mkdashboard(uid: str, title: str = None, message: str = None, overwrite: bool = False) -> Dict:
    """
    Create a dashboard create/update payload using grafanalib, suitable for
    submitting to the Grafana HTTP API.
    Note: This is solely for demonstration purposes, a real-world
    implementation would stuff more details into the dashboard beforehand.
    """
    dashboard = Dashboard(uid=uid, title=title)
    data = {
        "dashboard": encode_dashboard(dashboard),
        "overwrite": overwrite,
        "message": message,
    }
    return data


def encode_dashboard(entity) -> Dict:
    """
    Encode grafanalib `Dashboard` entity to dictionary.
    TODO: Optimize without going through JSON marshalling.
    """
    return json.loads(json.dumps(entity, sort_keys=True, cls=DashboardEncoder))


def run(grafana: GrafanaApi):
    """
    The main body of the example program.
    - Create a Grafana dashboard create/update payload.
    - Submit to Grafana HTTP API.
    - Display response.
    """

    # Create dashboard payload.
    dashboard_payload = mkdashboard(
        uid="abifsd",
        title="My awesome dashboard",
        message="Updated by grafanalib",
        overwrite=True,
    )
    print(dashboard_payload)

    # Create or update dashboard at Grafana HTTP API.
    response = grafana.dashboard.update_dashboard(dashboard_payload)

    # Display the outcome in JSON format.
    print(json.dumps(response, indent=2))


if __name__ == "__main__":
    """
    Boilerplate bootloader. Create a `GrafanaApi` instance and run example.
    """

    # Setup logging.
    setup_logging(level=logging.DEBUG)

    # Create a `GrafanaApi` instance, optionally configured with environment
    # variables `GRAFANA_URL` and `GRAFANA_TOKEN`.
    grafana_client = GrafanaApi.from_url(url="http://localhost:3000/",
    credential=("admin", "Ud98%2Lm"))

    # Invoke example conversation.
    run(grafana_client)
