"""Manages the elevator instance."""
import heapq
import logging

from ems_handler.decorators.common_decorators import Singleton
from ems_handler.logic.constants import elevatorAction, elevatorState
from ems_handler.logic.constants import (
    elevator_action_indx, elevator_state_indx, elevator_current_floor_indx, elevator_stops)

logger = logging.getLogger(__name__)


@Singleton
class elevatorInstance:
    """Common class to maintain state of each elevator.
    
    This is a singleton class so in a singne session once an elevator is initialized,
    the entire operation takes place on that parameters."""
    def __init__(self) -> None:
        """init class for elevatorInstance."""
        self.floors: int = None
        self.elevators: int = None
        self.floor_time: int = None
        self.data: dict = {}

    def initialize_elevator_data(self, floors: int, elevators: int, floor_time: int) -> None:
        """Updated the elevator instance as per the values provided
        
        args:
            floors: total floors in the building
            elevators: no of elevators
            floor_time: time in seconds to assend one floor."""
        setattr(self, "floors", floors)
        setattr(self, "elevators", elevators)
        setattr(self, "floor_time", floor_time)
        # This loop updates default data for each elevator
        # {"elevator_no": [state, action, current_floor, stops[] -> heapq ]}
        for elevator in range(self.elevators):
            self.data.update({
                elevator: [elevatorState.stopped, elevatorAction.up, 0, []]
            })
        logger.debug(f"ems object initialized with parameters {self.floors} : {self.elevators} : {self.floor_time}")
        return

    def get_current_data(self) -> dict:
        """returns current attributes."""
        return {
            "floor": self.floors,
            "elevators": self.elevators,
            "floor_time": self.floor_time,
            "data": {
                        key: [
                            val[elevator_state_indx].value,
                            val[elevator_action_indx].value,
                            val[elevator_current_floor_indx]
                    ]
                for key, val in self.data.items()
            }
        }

    def assign_elevator_no(self, requested_floor: int, requested_action: int) -> int:
        """Assign the best possible elevator as per the current states.
        Algo elaborated in readme."""
        dir, dist = 0, 0
        q: list = []
        for elv_no, data in self.data.items():
            dist = abs(data[elevator_current_floor_indx] - requested_floor)
            if data[elevator_state_indx] == elevatorState.moving:
                if data[elevator_action_indx] == requested_action:
                    dir = -1
                else:
                    dir = 1
            if not dir == 1:
                heapq.heappush(q, (dist, dir, elv_no))
        
        # updating assigned elevator data.
        stops = self.data.get(q[0][2])[elevator_stops]
        heapq.heappush(stops, requested_floor)
        self.data[q[0][2]][elevator_stops] = stops
        self.data[q[0][2]][elevator_action_indx] = requested_action
        self.data[q[0][2]][elevator_state_indx] = elevatorState.moving
        logger.debug(f"elevator assigned {q[0][2]}")
        return q[0][2]

    def validate_floor(self, floor: int) -> bool:
        """validates the requested floor."""
        return floor in range(self.floors)

    def update_floor_data(self, elevator_no: int) -> None:
        """update a floor assend/decend"""
        data: dict = self.data.get(elevator_no)
        if data[elevator_state_indx] == elevatorState.moving:
            logger.debug(f"updating floor for {elevator_no}")
            stops: heapq = data[elevator_stops]
            current_floor: int = data[elevator_current_floor_indx]
            if stops and stops[0] == current_floor:
                heapq.heappop(stops)
                self.data[elevator_no][elevator_stops] = stops
            else:
                current_floor += 1
                self.data[elevator_no][elevator_current_floor_indx] = current_floor
            if not stops:
                self.data[elevator_no][elevator_state_indx] = elevatorState.stopped
        return

    def update_user_floor(self, elevator_no: int, destination_floor: int) -> None:
        """Updating users request in the stops list as a floor where list will stop."""
        data: dict = self.data.get(elevator_no)
        stops: heapq = data[elevator_stops]
        heapq.heappush(stops, destination_floor)
        self.data[elevator_no][elevator_stops] = stops
        self.data[elevator_no][elevator_state_indx] = elevatorState.moving
        return

    def update_maintaince(self, elevator_no: int, mark_maintainence: bool) -> None:
        """This can be used to mark/unmark a lift if it is under maintaince."""
        if mark_maintainence:
            self.data[elevator_no] = [elevatorState.idle, elevatorAction.up, 0, []]
        else:
            self.data[elevator_no] = [elevatorState.stopped, elevatorAction.up, 0, []]
        return


    def __repr__(self) -> str:
        return f"{self.floors} : {self.elevators} : {self.floor_time}"
