from datetime import datetime

from pygrocy2.base import DataModel
from pygrocy2.grocy_api_client import (
    EquipmentDetailsResponse,
    CurrentEquipmentResponse,
    GrocyApiClient,
)


class Equipment(DataModel):
    """Class to represent a Grocy equipment item."""

    def __init__(self, response):
        self._init_empty()

        if isinstance(response, CurrentEquipmentResponse):
            self._init_from_CurrentEquipmentResponse(response)
        elif isinstance(response, EquipmentDetailsResponse):
            self._init_from_EquipmentDetailsResponse(response)

    def _init_from_CurrentEquipmentResponse(self, response: CurrentEquipmentResponse):
        self._id = response.id
        self._name = response.name

    def _init_from_EquipmentDetailsResponse(self, response: EquipmentDetailsResponse):
        self._id = response.equipment.id
        self._name = response.equipment.name
        self._description = response.equipment.description
        self._instruction_manual_file_name = response.equipment.instruction_manual_file_name
        self._created_timestamp = response.equipment.created_timestamp
        self._userfields = response.equipment.userfields
        self._last_maintenance = response.last_maintenance
        self._next_estimated_maintenance_time = response.next_estimated_maintenance_time

    def _init_empty(self):
        self._id = None
        self._name = None
        self._description = None
        self._instruction_manual_file_name = None
        self._created_timestamp = None
        self._userfields = None
        self._last_maintenance = None
        self._next_estimated_maintenance_time = None

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

    @property
    def last_maintenance(self) -> datetime:
        return self._last_maintenance

    @property
    def next_estimated_maintenance_time(self) -> datetime:
        return self._next_estimated_maintenance_time

    def as_dict(self):
        """Return a dict representation of the equipment."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instruction_manual_file_name": self.instruction_manual_file_name,
            "created_timestamp": self.created_timestamp,
            "userfields": self.userfields,
            "last_maintenance": self.last_maintenance,
            "next_estimated_maintenance_time": self.next_estimated_maintenance_time,
        }
