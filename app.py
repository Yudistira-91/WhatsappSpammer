import tkinter as tk
import songlyrics
import spammer
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

def run_songlyrics_script():
    trigger = DateTrigger()
    scheduler.add_job(songlyrics.run, trigger)

def run_spammer_script():
    trigger = DateTrigger()
    scheduler.add_job(lambda: spammer.run('Dor', 'zombie', '1'), trigger)

def init():
    HEIGHT = 400
    WIDTH = 500
    root = tk.Tk()
    root.resizable(0, 0)
    root.geometry(f'{WIDTH}x{HEIGHT}')

    frame = tk.Frame(root, bg='#ff9933')
    frame.place(relwidth=1, relheight=1)

    songlyrics_button = tk.Button(frame, command=run_songlyrics_script,
                            text="Run song lyrics",
                            bg='black',
                            fg='white',
                            bd=0)

    songlyrics_button.place(relx=0.325, rely=0.300, relwidth=0.35, relheight=0.1)
    spammer_button = tk.Button(frame, command=run_spammer_script,
                        text="Run Whatsapp spammer",
                        bg='white',
                        fg='black',
                        bd=0)
    spammer_button.place(relx=0.325, rely=0.500, relwidth=0.35, relheight=0.1)

    root.mainloop()

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    init()
