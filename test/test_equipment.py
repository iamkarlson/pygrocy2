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
    assert equipment.last_maintenance is None
    assert equipment.next_estimated_maintenance_time is None


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
        equipment=equipment_data,
        last_maintenance=datetime(2025, 2, 1),
        next_estimated_maintenance_time=datetime(2025, 4, 1)
    )
    
    equipment = Equipment(response)
    
    assert equipment.id == 1
    assert equipment.name == "Test Equipment"
    assert equipment.description == "Test Description"
    assert equipment.instruction_manual_file_name == "manual.pdf"
    assert equipment.created_timestamp == datetime(2025, 3, 23)
    assert equipment.userfields == {"custom_field": "custom_value"}
    assert equipment.last_maintenance == datetime(2025, 2, 1)
    assert equipment.next_estimated_maintenance_time == datetime(2025, 4, 1)


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
        equipment=equipment_data,
        last_maintenance=datetime(2025, 2, 1),
        next_estimated_maintenance_time=datetime(2025, 4, 1)
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
        "last_maintenance": datetime(2025, 2, 1),
        "next_estimated_maintenance_time": datetime(2025, 4, 1),
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
        equipment=equipment_data,
        last_maintenance=datetime(2025, 2, 1),
        next_estimated_maintenance_time=datetime(2025, 4, 1)
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
    assert equipment.last_maintenance == datetime(2025, 2, 1)
    assert equipment.next_estimated_maintenance_time == datetime(2025, 4, 1)


# These tests need a connection to a Grocy server and VCR cassettes
# @pytest.mark.vcr
# def test_grocy_equipment_basic(grocy):
#     """Test basic equipment listing via Grocy class."""
#     equipment_items = grocy.equipment(get_details=False)
#     
#     assert len(equipment_items) > 0
#     assert equipment_items[0].id > 0
#     assert equipment_items[0].name is not None


# @pytest.mark.vcr
# def test_grocy_equipment_detailed(grocy):
#     """Test detailed equipment via Grocy class."""
#     equipment_items = grocy.equipment(get_details=True)
#     
#     assert len(equipment_items) > 0
#     assert equipment_items[0].id > 0
#     assert equipment_items[0].name is not None
#     assert hasattr(equipment_items[0], 'description')
