"""This file contains all the constants required by ems instance."""
from enum import Enum

class elevatorState(Enum):
    """Enum class to hold states of elevator."""
    moving: str = "moving"
    stopped: str = "stopped"
    idle: str = "under maintenance"

class elevatorAction(Enum):
    """Enum class to maintain actions of elevator."""
    up: str = "moving up"
    down: str = "moving down"

elevator_state_indx: int = 0
elevator_action_indx: int = 1
elevator_current_floor_indx: int = 2
elevator_stops: int = 3
