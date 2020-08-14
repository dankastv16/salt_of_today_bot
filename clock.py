import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=29)
def timed_job():
    print('This job is run every 29 minutes.')

sched.start()
