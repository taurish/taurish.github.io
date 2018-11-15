import schedule
import time

def job():
    print("I'm working...")

schedule.every(0.5).minutes.do(job)
#schedule.every().hour.do(job)
schedule.every().day.at("12:40").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
