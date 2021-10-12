from typing import Dict, List, Optional, cast

from globus_sdk import GCSClient, RefreshTokenAuthorizer

from globus_cli import version
from globus_cli.login_manager import internal_auth_client, token_storage_adapter

from .transfer import get_client as get_transfer_client


def get_gcs_client(
    gcs_id: str, *, gcs_address: Optional[str] = None, require_auth: bool = True
) -> GCSClient:
    adapter = token_storage_adapter()
    tokens = adapter.get_token_data(gcs_id)
    authorizer = None

    # if there are tokens, build the authorizer
    if tokens is not None:
        authorizer = RefreshTokenAuthorizer(
            tokens["refresh_token"],
            internal_auth_client(),
            access_token=tokens["access_token"],
            expires_at=tokens["expires_at_seconds"],
            on_refresh=adapter.on_refresh,
        )
    elif require_auth:
        raise ValueError(
            f"Could not get login data for GCS {gcs_id}. "
            f"Try login with '--gcs {gcs_id}' to fix."
        )

    if not gcs_address:
        tc = get_transfer_client()
        gcs_address = cast(str, tc.get_endpoint(gcs_id)["DATA"][0]["hostname"])

    return GCSClient(gcs_address, authorizer=authorizer, app_name=version.app_name)


CONNECTOR_INFO: List[Dict[str, str]] = [
    {
        "connector_id": "145812c8-decc-41f1-83cf-bb2a85a2a70b",
        "name": "POSIX",
    },
    {
        "connector_id": "7e3f3f5e-350c-4717-891a-2f451c24b0d4",
        "name": "BlackPearl",
    },
    {
        "connector_id": "7c100eae-40fe-11e9-95a3-9cb6d0d9fd63",
        "name": "Box",
    },
    {
        "connector_id": "1b6374b0-f6a4-4cf7-a26f-f262d9c6ca72",
        "name": "Ceph",
    },
    {
        "connector_id": "28ef55da-1f97-11eb-bdfd-12704e0d6a4d",
        "name": "OneDrive",
    },
    {
        "connector_id": "976cf0cf-78c3-4aab-82d2-7c16adbcc281",
        "name": "Google Drive",
    },
    {
        "connector_id": "56366b96-ac98-11e9-abac-9cb6d0d9fd63",
        "name": "Google Cloud Storage",
    },
    {
        "connector_id": "7251f6c8-93c9-11eb-95ba-12704e0d6a4d",
        "name": "ActiveScale",
    },
    {
        "connector_id": "7643e831-5f6c-4b47-a07f-8ee90f401d23",
        "name": "S3",
    },
    {
        "connector_id": "052be037-7dda-4d20-b163-3077314dc3e6",
        "name": "POSIX Staging",
    },
    {
        "connector_id": "e47b6920-ff57-11ea-8aaa-000c297ab3c2",
        "name": "iRODS",
    },
]


def connector_display_name_to_id(connector_name: str) -> Optional[str]:
    conn_id = None
    for data in CONNECTOR_INFO:
        if data["name"] == connector_name:
            conn_id = data["connector_id"]
            break
    return conn_id


def connector_id_to_display_name(connector_id: str) -> str:
    display_name = None
    for data in CONNECTOR_INFO:
        if data["connector_id"] == connector_id:
            display_name = data["name"]
            break

    if not display_name:
        display_name = f"UNKNOWN ({connector_id})"

    return display_name