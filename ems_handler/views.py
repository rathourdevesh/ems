"""Default views file for ems handler."""
import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from ems_handler.decorators.ems_decorators import http_allowed_method
from ems_handler.logic.constants import elevatorAction
from ems_handler.logic.elevator_handler import elevatorInstance
from ems_handler.logic.scheduler import schedule_elevator_data_update_cron


@http_allowed_method(method='POST')
def create_elevators(request: HttpRequest) -> HttpResponse:
    """Initialize an Elevator object.
    
    args: request
            - floor: no of floors of the building
            - elevators: no of elevators present in the building
            - floor_time: time in seconds to assend one floor."""
    data = json.loads(request.body)
    floors = data.get("floors")
    elevators = data.get("elevators")
    floor_time = data.get("floor_time")
    ems_obj = elevatorInstance()
    if ems_obj.elevators is None:
        ems_obj.initialize_elevator_data(floors, elevators, floor_time)
        schedule_elevator_data_update_cron(floor_time)
        return JsonResponse({'success':True, 'message':'elevator object initialized'})
    return JsonResponse({'success':False, 'message':'elevator object already initialized'})


@http_allowed_method(method='GET')
def get_elevators(request: HttpRequest) -> HttpResponse:
    """Get the states of elevator at any point of time."""
    ems_obj = elevatorInstance()
    return JsonResponse(ems_obj.get_current_data())


@http_allowed_method(method='POST')
def assign_elevator(request: HttpRequest) -> HttpResponse:
    """Get the elevator no to be assigned to a user."""
    data = json.loads(request.body)
    ems_obj = elevatorInstance()
    success: bool = True
    msg: str = "Elevator assigned."
    elevator_no: int = 0
    requested_floor: int = data.get("requested_floor")
    if ems_obj.validate_floor(requested_floor):
        requested_action: int = elevatorAction(data.get("requested_action"))
        elevator_no: int = ems_obj.assign_elevator_no(requested_floor, requested_action)
    else:
        success = False
        msg = f"Invalid request -floor should be below {ems_obj.floors} and action {elevatorAction.down}/{elevatorAction.up}"
    return JsonResponse({
        "success": success,
        "message": msg,
        "elevator_no": elevator_no
    })

@http_allowed_method(method='POST')
def update_user_request(request: HttpRequest) -> HttpResponse:
    """Update the user input."""
    data = json.loads(request.body)
    ems_obj = elevatorInstance()
    elevator_no: int = data.get("elevator_no")
    destination_floor: int = data.get("destination_floor")
    ems_obj.update_user_floor(elevator_no, destination_floor)
    return JsonResponse({
        "success": True,
        "message": "stops updated"
    })

@http_allowed_method(method='PUT')
def mark_maintaince(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.body)
    ems_obj = elevatorInstance()
    elevator_no: int = data.get("elevator_no")
    mark_maintainence: int = data.get("mark_maintainence")
    ems_obj.update_maintaince(elevator_no, mark_maintainence)
    return JsonResponse({
        "success": True,
        "message": f"data updated for {elevator_no}"
    })