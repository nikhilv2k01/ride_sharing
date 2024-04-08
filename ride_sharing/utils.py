# utils.py
from .tasks import update_ride_location
from ride_sharing_project.celery import app, get_ride_update_schedule

def start_ride_tracking(ride_id):
    
    update_ride_location.delay(ride_id)
    get_ride_update_schedule(ride_id)
    return


def stop_ride_tracking(ride_id):
    update_ride_location.revoke(ride_id, terminate=True)

    return