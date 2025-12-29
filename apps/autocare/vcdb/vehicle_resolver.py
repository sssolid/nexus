from __future__ import annotations

from typing import Any, Optional

from apps.autocare.api_client import AutocareAPIClient


class VehicleResolver:
    """
    Resolve Vehicles ONLY if they fully satisfy the canonical VCDB Vehicle schema.

    This resolver does NOT:
      - create stubs
      - guess missing fields
      - fabricate FK relationships
      - relax NOT NULL constraints

    If a Vehicle cannot exist canonically, it is explicitly skipped.
    """

    def __init__(self, api_client: AutocareAPIClient):
        self.client = api_client

    # ---------------------------------------------------------

    def fetch_vehicle_json(self, vehicle_id: int) -> Optional[dict[str, Any]]:
        """
        Fetch a single vehicle from the authenticated UI endpoint.

        Returns:
            dict payload if found
            None if not found
        """
        endpoint = f"/api/vcdb/vehicles/{vehicle_id}"
        params = {
            "cultureId": "en-US",
            "cultureCode": "en-US",
        }

        response = self.client.get_raw(endpoint, params=params)

        if response.status_code == 404:
            return None

        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict):
            return None

        return data

    # ---------------------------------------------------------

    def ensure_vehicle_exists(self, VehicleModel, vehicle_id: int) -> tuple[bool, str]:
        """
        Ensure a Vehicle exists IF AND ONLY IF it satisfies VCDB schema.

        Returns:
            (True, "")        -> vehicle exists or was safely created
            (False, reason)   -> vehicle is non-canonical and must be skipped
        """

        # Already present
        if VehicleModel.objects.filter(vehicle_id=vehicle_id).exists():
            return True, ""

        payload = self.fetch_vehicle_json(vehicle_id)
        if not payload:
            return False, "Vehicle not present in bulk VCDB or UI endpoint"

        # ---- HARD VCDB CONTRACT ----
        # These fields are NOT NULL in the official schema.
        required_fields = (
            "VehicleID",
            "BaseVehicleID",
            "SubModelID",
            "RegionID",
            "PublicationStageID",
            "PublicationStageDate",
        )

        for field in required_fields:
            if payload.get(field) is None:
                return False, f"UI vehicle missing required field {field}"

        # ---- SAFE INSERT (IDs only, no FK objects) ----
        VehicleModel.objects.create(
            vehicle_id=payload["VehicleID"],
            base_vehicle_id=payload["BaseVehicleID"],
            submodel_id=payload["SubModelID"],
            region_id=payload["RegionID"],
            publication_stage_id=payload["PublicationStageID"],
            publication_stage_source=payload.get("PublicationStageSource", ""),
            publication_stage_date=payload["PublicationStageDate"],
            effective_datetime=payload.get("EffectiveDateTime"),
            end_datetime=payload.get("EndDateTime"),
        )

        return True, ""
