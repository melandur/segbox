from __future__ import annotations

import os.path
import shutil
from pathlib import Path
from shutil import copy

from nicegui import app, ui
from nicegui.events import MouseEventArguments
from pynput import mouse

from local_file_picker import local_file_picker


class State:

    def __init__(self):
        self.radius = 15
        self.color = "SkyBlue"
        self.scroll_index = 0
        self.on_image = False
        self.image_index = 0
        self.data_folder = Path(__file__).resolve().parent / 'data'  # image source: https://pixabay.com/
        self.static_folder = Path(__file__).resolve().parent / 'static'  # image source: https://pixabay.com/
        self.files = sorted(f.name for f in self.data_folder.glob('*'))
        self.images = os.listdir(self.data_folder)
        self.count_images = len(self.images)


state = State()


app.add_static_files('/data', state.data_folder)  # serve all files in this folder
app.add_static_files('/static', state.static_folder)  # serve all files in this folder


def on_scroll(x, y, dx, dy):
    if state.on_image:
        state.scroll_index += dy
        print(state.scroll_index)


listener = mouse.Listener(on_scroll=on_scroll)
listener.start()


def check_files():
    # files = os.listdir(data_folder)
    if state.count_images > 6:
        ui.notify('Currently only 6 files are supported, choose again')
        shutil.rmtree(state.data_folder)
        os.makedirs(state.data_folder, exist_ok=True)


async def pick_file() -> None:
    results = await local_file_picker('~', multiple=True, show_hidden_files=False)
    if results:
        for result in results:
            ui.notify(result)
            file_name = os.path.basename(result)
            new_path = f'{state.data_folder}{os.sep}{file_name}'
            copy(result, new_path)
            check_files()
            image_viewers()


def mouse_handler(event: MouseEventArguments) -> None:
    if event.type == 'mousedown':
        image_1.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" r="{state.radius}" fill="{state.color}" />'
        if image_2:
            image_2.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" r="{state.radius}" fill="{state.color}" />'
        if image_3:
            image_3.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" r="{state.radius}" fill="{state.color}" />'
        if image_4:
            image_4.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" r="{state.radius}" fill="{state.color}" />'
        if image_5:
            image_5.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" r="{state.radius}" fill="{state.color}" />'
        if image_6:
            image_6.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" r="{state.radius}" fill="{state.color}" />'
    if event.type == 'mouseover':
        state.on_image = True
    if event.type == 'mouseout':
        state.on_image = False


# def handle_key(event: KeyEventArguments) -> None:
#     global index
#     if event.action.keydown:
#         if event.key.arrow_right:
#             index += 1
#         if event.key.arrow_left:
#             index -= 1
#         index = index % len(files)
#         slide.set_source(f'slides/{files[index]}')


def handle_shutdown():
    if os.path.exists(f'{state.data_folder}{os.sep}slides'):
        print('slides folder exists')


"""APP"""
ui.label('CONTENT')

container_1 = ui.row()
container_2 = ui.row()

with container_1.style('width: 100%'):
    image_1 = ui.interactive_image(
        f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True
    ).style(f'width: 30%')
    image_2 = ui.interactive_image(
        f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True
    ).style(f'width: 30%')
    image_3 = ui.interactive_image(
        f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True
    ).style(f'width: 30%')

with container_2.style('width: 100%'):
    image_4 = ui.interactive_image(
        f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True
    ).style(f'width: 30%')
    image_5 = ui.interactive_image(
        f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True
    ).style(f'width: 30%')
    image_6 = ui.interactive_image(
        f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True
    ).style(f'width: 30%')


def image_viewers():
    if state.count_images:
        if state.count_images > 3:
            width = int(95 / 3)
        else:
            width = int(95 / state.count_images)

        with container_1.style('width: 100%'):
            if state.count_images >= 1:
                image_1.set_source(f'data/{state.images[0]}')
                image_1.style(f'width: {width}%')
            if state.count_images >= 2:
                image_2.set_source(f'data/{state.images[1]}')
                image_2.style(f'width: {width}%')
            if state.count_images >= 3:
                image_3.set_source(f'data/{state.images[2]}')
                image_3.style(f'width: {width}%')

        with container_2.style('width: 100%'):
            if state.count_images >= 4:
                image_4.set_source(f'data/{state.images[3]}')
                image_4.style(f'width: {width}%')
            if state.count_images >= 5:
                image_5.set_source(f'data/{state.images[4]}')
                image_5.style(f'width: {width}%')
            if state.count_images >= 6:
                image_6.set_source(f'data/{state.images[5]}')
                image_6.style(f'width: {width}%')


with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    ui.label('SegBox')
    ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')

with ui.left_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
    slider = ui.slider(min=0, max=100, value=15).style('margin-top: 15px').bind_value(state, 'radius')
    color_input = ui.color_input(label='Color', value='#000000').bind_value(state, 'color').style('margin-top: 15px')
    ui.button('Choose files', on_click=pick_file).props('icon=folder').style('margin-top: 30px')
    ui.button('Show images', on_click=image_viewers).props('icon=camera').style('margin-top: 15px')

with ui.footer().style('background-color: #3874c8'):
    ui.label('MIA Lab - ARTORG - University of Bern')


ui.run()
