from threading import Thread
import schedule
import time

class Scheduler(Thread):

    def __init__(self, updater, data_handler):
        super().__init__()
        self.updater = updater
        self.data_handler = data_handler
        self.daemon = True

    def run(self):
        schedule.every(1).minutes.do(self.send_daily_quiz)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def send_daily_quiz(self):
        from datetime import datetime
        now_time = datetime.now().strftime('%H:%M')
        for user_id in self.data_handler.get_all_users():
            quiz_time = self.data_handler.get_user_quiz_time(user_id)
            if quiz_time == now_time:
                chat_id = int(user_id)  
                from .bot import send_quiz
                send_quiz(self.updater.bot, chat_id)
