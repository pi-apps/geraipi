import time

from celery import shared_task


@shared_task(name="api_check_availability")
def check_availability():
    time.sleep(20)
    print("hello")
