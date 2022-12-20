"""Scheduler."""
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging

from ems_handler.logic.elevator_handler import elevatorInstance

logger = logging.getLogger(__name__)

def update_elevator_floors():
    """This function is responsible to update floors of an elevator."""
    ems_obj = elevatorInstance()
    for ele in range(ems_obj.elevators):
        ems_obj.update_floor_data(ele)
    logger.debug("schedule_elevator_data_update_cron task completed")


def schedule_elevator_data_update_cron(floor_time: int) -> None:
    """This function starts a scheduler triggered at fixed interval
    (as per the floor time). and updates each lift data so that lift
    which is in moving state. Its data are constatly updated."""
    
    logger.debug("schedule_elevator_data_update_cron initialized")
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_elevator_floors, 'interval', seconds=floor_time)
    scheduler.start()
