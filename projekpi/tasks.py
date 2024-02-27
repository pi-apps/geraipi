from celery import shared_task
import time

@shared_task(name="api_check_availability")
def check_availability():
    time.sleep(20)
    print("hello")