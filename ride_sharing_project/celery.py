from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ride_sharing_project.settings")
app = Celery("ride_sharing_project")
app.conf.enable_utc = False
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()


def get_ride_update_schedule(ride_id):
    print("get ride update scheduler working")
    return {
        'update_ride_location_task': {
            'task': 'ride_sharing.tasks.update_ride_location',
            'schedule': timedelta(seconds=5),
            'args': (ride_id,),
        }
    }