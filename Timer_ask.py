import time
import threading
import os
from Text_to_speech import text_to_speech
class Timer:

    def __init__(self):
        self.info = {}
        self.time_in_seconds = 0
        self.timer_thread = None
        self.is_running = False
        self._stop_event = threading.Event()

    def set_timer(self,input_timer : list):
        self.info={}
        for x in input_timer:
            if x.isdigit() :
                self.info['time']=int(x)
            if x in ['min','seconds','hour','minutes','minute']:
              self.info['measure']=x
        try:
            return self.info['time'],self.info['measure']
        except:
            print('nothing')

    def translate_time(self):
        try:
            measure_condition=self.info['measure']
            time_numbers=self.info['time']
            if measure_condition == 'minutes'or measure_condition == 'minute':
                self.time_in_seconds=time_numbers * 60
            elif measure_condition == 'seconds':
                self.time_in_seconds=time_numbers
            elif measure_condition == 'hour':
                self.time_in_seconds=time_numbers * 3600
            else:
                return 'nothing'
            return self.time_in_seconds
        except:
            return None
    def return_start_time(self):
        try:
            return f"timer set for {self.info['time']} {self.info['measure']}"
        except:
            print('error')



    def timer_and_sound(self):
            try:
                self.is_running = True
                for _ in range(self.time_in_seconds):
                    if self._stop_event.is_set():
                        print("Timer was stopped.")
                        self.is_running = False
                        return
                    time.sleep(1)
                self.is_running = False
                os.system("osascript -e 'set volume input volume 0'")
                print(f"Timer for {self.info['time']} {self.info['measure']} ended")
                text_to_speech(f"Beep Beep Beep Beep Timer for {self.info['time']} {self.info['measure']} ended", 'en')
                os.system("osascript -e 'set volume input volume 100'")
            except Exception as e:
                print(f'There was an error: {e}')

    def start_timer(self):
        self._stop_event.clear()
        self.timer_thread = threading.Thread(target=self.timer_and_sound)
        self.timer_thread.start()
        return self.timer_thread

    def stop_timer(self):
        if self.is_running:
            self._stop_event.set()
            self.timer_thread.join()




















