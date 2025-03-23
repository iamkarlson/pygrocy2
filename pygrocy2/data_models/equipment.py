from datetime import datetime

from pygrocy2.base import DataModel
from pygrocy2.grocy_api_client import (
    EquipmentDetailsResponse,
    EquipmentData,
    GrocyApiClient,
)


class Equipment(DataModel):
    """Class to represent a Grocy equipment item."""

    def __init__(self, response):
        self._init_empty()

        if isinstance(response, EquipmentData):
            self._init_from_EquipmentData(response)
        elif isinstance(response, EquipmentDetailsResponse):
            self._init_from_EquipmentDetailsResponse(response)
        elif isinstance(response, dict):
            # Initialize from a plain dictionary response from the API
            self._init_from_dict(response)

    def _init_from_EquipmentData(self, response: EquipmentData):
        self._id = response.id
        self._name = response.name
        self._description = response.description
        self._instruction_manual_file_name = response.instruction_manual_file_name
        self._created_timestamp = response.created_timestamp
        self._userfields = response.userfields

    def _init_from_EquipmentDetailsResponse(self, response: EquipmentDetailsResponse):
        self._id = response.equipment.id
        self._name = response.equipment.name
        self._description = response.equipment.description
        self._instruction_manual_file_name = response.equipment.instruction_manual_file_name
        self._created_timestamp = response.equipment.created_timestamp
        self._userfields = response.equipment.userfields

    def _init_from_dict(self, response: dict):
        self._id = response.get("id")
        self._name = response.get("name")
        self._description = response.get("description")
        self._instruction_manual_file_name = response.get("instruction_manual_file_name")
        self._created_timestamp = response.get("row_created_timestamp") or response.get("created_timestamp")
        self._userfields = response.get("userfields")

    def _init_empty(self):
        self._id = None
        self._name = None
        self._description = None
        self._instruction_manual_file_name = None
        self._created_timestamp = None
        self._userfields = None

    def get_details(self, api_client: GrocyApiClient):
        details = api_client.get_equipment(self._id)
        self._init_from_EquipmentDetailsResponse(details)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def instruction_manual_file_name(self) -> str:
        return self._instruction_manual_file_name

    @property
    def created_timestamp(self) -> datetime:
        return self._created_timestamp

    @property
    def userfields(self):
        return self._userfields

    def as_dict(self):
        """Return a dict representation of the equipment."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instruction_manual_file_name": self.instruction_manual_file_name,
            "created_timestamp": self.created_timestamp,
            "userfields": self.userfields,
        }
