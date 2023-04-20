from __future__ import annotations

import os.path
import shutil
from pathlib import Path
from shutil import copy

from nicegui import app, ui
from nicegui.events import MouseEventArguments
from pynput import mouse

from local_file_picker import local_file_picker


class Container_1:
    def __init__(self, mouse_handler):
        self.image_1 = ui.interactive_image(f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True).style(f'width: 0%')
        self.image_2 = ui.interactive_image(f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True).style(f'width: 0%')
        self.image_3 = ui.interactive_image(f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True).style(f'width: 0%')


class Container_2:
    def __init__(self, mouse_handler):
        self.image_4 = ui.interactive_image(f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True).style(f'width: 0%')
        self.image_5 = ui.interactive_image(f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True).style(f'width: 0%')
        self.image_6 = ui.interactive_image(f'static/1x1.png', on_mouse=mouse_handler, events=['mouseover', 'mouseout', 'mousedown'], cross=True).style(f'width: 0%')


class SegBox:

    def __init__(self):
        self.radius = 15
        self.color = "SkyBlue"
        self.scroll_index = 0
        self.on_image = False
        self.image_index = 0

        self.last_visited_folder = '~'
        self.data_folder = Path(__file__).resolve().parent / 'data'  # image source: https://pixabay.com/
        self.static_folder = Path(__file__).resolve().parent / 'static'  # image source: https://pixabay.com/
        self.files = None
        self.images = None
        self.count_images = None

        app.add_static_files('/data', self.data_folder)  # serve all files in this folder
        app.add_static_files('/static', self.static_folder)  # serve all files in this folder

        with ui.row().style('width: 100%'):
            self.container_1 = Container_1(self.mouse_handler)
        with ui.row().style('width: 100%'):
            self.container_2 = Container_2(self.mouse_handler)

        listener = mouse.Listener(on_scroll=self.on_scroll)
        listener.start()

    def update(self):
        self.data_folder = Path(__file__).resolve().parent / 'data'  # image source: https://pixabay.com/
        self.static_folder = Path(__file__).resolve().parent / 'static'  # image source: https://pixabay.com/
        self.files = sorted(f.name for f in self.data_folder.glob('*'))
        self.images = os.listdir(self.data_folder)
        self.count_images = len(self.images)
        app.add_static_files('/data', self.data_folder)  # serve all files in this folder
        app.add_static_files('/static', self.static_folder)  # serve all files in this folder

    def __call__(self):
        with ui.header(elevated=False).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')
            ui.label('SegBox').style('color: white; font-size: 20px; font-weight: bold')
            ui.label('v0.1').style('color: white; font-weight: bold')

        with ui.left_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
            with ui.card().style('margin-top: 15px'):
                ui.button('Choose files', on_click=self.pick_file).props('icon=folder').props('floating')

            with ui.card().style('margin-top: 15px'):
                self.slider = ui.slider(min=0, max=100, value=15).bind_value(self, 'radius')
                self.color_input = ui.color_input(label='Color', value='#000000').bind_value(self, 'color')

            with ui.card().style('margin-top: 15px'):
                ui.label('Files').style('font-weight: bold')
                ui.button('Show Images', on_click=self.show_image).props('icon=camera')
                # ui.button('Choose files', on_click=self.pick_file).props('icon=folder')
                # ui.button('Choose files', on_click=self.pick_file).props('icon=folder')
                # for file in self.files:
                #     ui.label(file).style('margin-top: 5px')

            with ui.card().style('margin-top: 15px'):
                with ui.row():
                    ui.spinner(size='lg')
                    ui.spinner('audio', size='lg', color='green')
                    ui.spinner('dots', size='lg', color='red')

            with ui.card().style('margin-top: 15px'):
                ui.label('Process').style('font-weight: bold')
                slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
                ui.linear_progress().bind_value_from(slider, 'value')

        with ui.footer().style('background-color: #3874c8'):
            ui.label('MIA Lab - ARTORG - University of Bern')

        ui.run(reload=False)

    def on_scroll(self, x, y, dx, dy):
        if self.on_image:
            self.scroll_index += dy
            print(self.scroll_index)

    def image_viewers(self):
        self.files = sorted(f.name for f in self.data_folder.glob('*'))
        if self.count_images:
            if self.count_images > 3:
                width = int(95 / 3)
            else:
                width = int(95 / self.count_images)

            with ui.row().style('width: 100%'):
                if self.count_images >= 1:
                    self.container_1.image_1.set_source(f'data/{self.images[0]}')
                    self.container_1.image_1.style(f'width: {width}%')
                if self.count_images >= 2:
                    self.container_1.image_2.set_source(f'data/{self.images[1]}')
                    self.container_1.image_2.style(f'width: {width}%')
                if self.count_images >= 3:
                    self.container_1.image_3.set_source(f'data/{self.images[2]}')
                    self.container_1.image_3.style(f'width: {width}%')

            with ui.row().style('width: 100%'):
                if self.count_images >= 4:
                    self.container_2.image_4.set_source(f'data/{self.images[3]}')
                    self.container_2.image_4.style(f'width: {width}%')
                if self.count_images >= 5:
                    self.container_2.image_5.set_source(f'data/{self.images[4]}')
                    self.container_2.image_5.style(f'width: {width}%')
                if self.count_images >= 6:
                    self.container_2.image_6.set_source(f'data/{self.images[5]}')
                    self.container_2.image_6.style(f'width: {width}%')

    def mouse_handler(self, event: MouseEventArguments) -> None:
        if event.type == 'mousedown':
            if self.container_1.image_1:
                self.container_1.image_1.content += f'<circle cx="{event.image_x}" cy="{event.image_y}" fill="{self.color}" r="{self.radius}"/>'
            if self.container_1.image_2:
                self.container_1.image_2.content += f'<circle cx="{event.image_x}" cy="{event.image_y} fill="{self.color}" r="{self.radius}"/>'
            if self.container_1.image_3:
                self.container_1.image_3.content += f'<circle cx="{event.image_x}" cy="{event.image_y} fill="{self.color}" r="{self.radius}"/>'
            if self.container_2.image_4:
                self.container_2.image_4.content += f'<circle cx="{event.image_x}" cy="{event.image_y} fill="{self.color}" r="{self.radius}"/>'
            if self.container_2.image_5:
                self.container_2.image_5.content += f'<circle cx="{event.image_x}" cy="{event.image_y} fill="{self.color}" r="{self.radius}"/>'
            if self.container_2.image_6:
                self.container_2.image_6.content += f'<circle cx="{event.image_x}" cy="{event.image_y} fill="{self.color}" r="{self.radius}"/>'
        if event.type == 'mouseover':
            self.on_image = True
        if event.type == 'mouseout':
            self.on_image = False

    def image_overlay(self, image):
        mask_src = f'data/{self.images[self.scroll_index]}'
        image.content = f'''
             <image xlink:href="{mask_src}" width="100%" height="100%" x="0" y="0" filter="url(#mask)" />
             <filter id="mask">
                 <feComponentTransfer>
                     <feFuncR type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                     <feFuncG type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                     <feFuncB type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                     <feFuncR type="linear" slope="1000"/>
                 </feComponentTransfer>
                 <feColorMatrix type="matrix" values="1 0 0 0 0   0 1 0 0 0   0 0 1 0 0  3 -1 -1 0 0" />
             </filter>
         '''

    def check_files(self):
        if self.count_images > 6:
            ui.notify('Currently only 6 files are supported, choose again')
            shutil.rmtree(self.data_folder)
            os.makedirs(self.data_folder, exist_ok=True)

    async def pick_file(self) -> None:
        results = await local_file_picker(
            directory=self.last_visited_folder,
            upper_limit=os.path.expanduser('~'),
            multiple=True,
            show_hidden_files=False,
        )
        if results:
            for result in results:
                ui.notify(result)
                file_name = os.path.basename(result)
                new_path = f'{self.data_folder}{os.sep}{file_name}'
                self.last_visited_folder = os.path.dirname(result)
                copy(result, new_path)
                self.update()
                # check_files()
                self.image_viewers()

    def show_image(self):
        self.update()
        self.image_viewers()


sb = SegBox()
sb()