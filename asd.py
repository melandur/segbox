import os
import time
from nicegui import ui, app

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path


class MyHandler(FileSystemEventHandler):
    def __init__(self, gui):
        self.gui = gui

    def on_any_event(self, event):
        self.gui.reload()

class MyApp:


    def __init__(self):
        self.name = 'logo.png'
        data_folder = Path(__file__).resolve().parent / 'data'
        app.add_static_files('/data', data_folder)
        ui.button('fresh', on_click=self.do)
        self.image = ui.image(f"data/{self.name}")
        # ui.add(self.image)

        # create watchdog observer to monitor folder
        # event_handler = MyHandler(self.image)
        # self.observer = Observer()
        # self.observer.schedule(event_handler, self.static_folder, recursive=True)
        # self.observer.start()

        # s.show(block=True)
    async def do(self):
        await ui.run_javascript('location.reload();', respond=False)

    def __call__(self, *args, **kwargs):
        ui.run(reload=True)

    def reload(self):
        # reload static folder and update GUI
        self.image.set_source(f'data/{self.name}')

app1 = MyApp()
app1()

# files = sorted(f.name for f in data_fold1er.glob('*.jpeg'))

# x = ui.image(f'data/cat.jpeg').style('width: 100%')
#
# ui.run()
