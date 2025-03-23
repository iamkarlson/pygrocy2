from datetime import datetime

import pytest
from unittest.mock import MagicMock

from pygrocy2.data_models.equipment import Equipment
from pygrocy2.grocy_api_client import EquipmentDetailsResponse, CurrentEquipmentResponse, EquipmentData, GrocyApiClient


def test_equipment_init_from_current_response():
    """Test Equipment initialization from CurrentEquipmentResponse."""
    response = CurrentEquipmentResponse(id=1, name="Test Equipment")
    equipment = Equipment(response)

    assert equipment.id == 1
    assert equipment.name == "Test Equipment"
    assert equipment.description is None
    assert equipment.instruction_manual_file_name is None
    assert equipment.created_timestamp is None
    assert equipment.userfields is None



def test_equipment_init_from_details_response():
    """Test Equipment initialization from EquipmentDetailsResponse."""
    equipment_data = EquipmentData(
        id=1,
        name="Test Equipment",
        description="Test Description",
        instruction_manual_file_name="manual.pdf",
        row_created_timestamp=datetime(2025, 3, 23),
        userfields={"custom_field": "custom_value"}
    )

    response = EquipmentDetailsResponse(
        equipment=equipment_data
    )

    equipment = Equipment(response)

    assert equipment.id == 1
    assert equipment.name == "Test Equipment"
    assert equipment.description == "Test Description"
    assert equipment.instruction_manual_file_name == "manual.pdf"
    assert equipment.created_timestamp == datetime(2025, 3, 23)
    assert equipment.userfields == {"custom_field": "custom_value"}


def test_equipment_as_dict():
    """Test Equipment.as_dict method."""
    equipment_data = EquipmentData(
        id=1,
        name="Test Equipment",
        description="Test Description",
        instruction_manual_file_name="manual.pdf",
        row_created_timestamp=datetime(2025, 3, 23),
        userfields={"custom_field": "custom_value"}
    )

    response = EquipmentDetailsResponse(
        equipment=equipment_data
    )

    equipment = Equipment(response)
    result = equipment.as_dict()

    expected = {
        "id": 1,
        "name": "Test Equipment",
        "description": "Test Description",
        "instruction_manual_file_name": "manual.pdf",
        "created_timestamp": datetime(2025, 3, 23),
        "userfields": {"custom_field": "custom_value"},
    }
    assert result == expected


def test_equipment_get_details():
    """Test Equipment.get_details method."""
    initial_response = CurrentEquipmentResponse(id=1, name="Initial Equipment")
    equipment = Equipment(initial_response)

    equipment_data = EquipmentData(
        id=1,
        name="Detailed Equipment",
        description="Detailed Description",
        instruction_manual_file_name="manual.pdf",
        row_created_timestamp=datetime(2025, 3, 23),
        userfields={"field": "value"}
    )

    details_response = EquipmentDetailsResponse(
        equipment=equipment_data
    )

    # Create mock API client
    mock_api = MagicMock(spec=GrocyApiClient)
    mock_api.get_equipment.return_value = details_response

    # Call get_details
    equipment.get_details(mock_api)

    # Check that the equipment was updated with the detailed information
    mock_api.get_equipment.assert_called_once_with(1)
    assert equipment.name == "Detailed Equipment"
    assert equipment.description == "Detailed Description"
    assert equipment.instruction_manual_file_name == "manual.pdf"
    assert equipment.userfields == {"field": "value"}
