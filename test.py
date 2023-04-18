#!/usr/bin/env python3
from pathlib import Path

from nicegui import app, ui
from nicegui.events import KeyEventArguments

folder = Path(__file__).resolve().parent / 'data'  # image source: https://pixabay.com/
folder1 = Path(__file__).resolve().parent / 'static'  # image source: https://pixabay.com/
files = sorted(f.name for f in folder.glob('*'))
index = 0


def handle_key(event: KeyEventArguments) -> None:
    global index
    if event.action.keydown:
        if event.key.arrow_right:
            index += 1
        if event.key.arrow_left:
            index -= 1
        index = index % len(files)
        slide.set_source(f'data/{files[index]}')
        # slide.set_source(f'slides/{files[index]}')


app.add_static_files('/data', folder)  # serve all files in this folder
app.add_static_files('/static', folder1)  # serve all files in this folder
slide = ui.image(f'static/1x1.png')  # show the first image
# slide1 = ui.image(f'data/{files[index-1]}')  # show the first image
ui.keyboard(on_key=handle_key)  # handle keyboard events

ui.run()
