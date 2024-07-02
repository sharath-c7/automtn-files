import cardinalityCounts
import policy_condition_channels_metric
import schedule
import time

def main():
    print("This job is scheduled to run for every hour")
    # print("This job is scheduled to run for every min")
    policy_condition_channels_metric.job_schedule()
    cardinalityCounts.cardinality()

# schedule.every().hour.do(main)
schedule.every(10).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
