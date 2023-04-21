from __future__ import annotations

import os
import shutil
from shutil import copy

import numpy as np

from nicegui import app, ui
from nicegui.events import MouseEventArguments, KeyEventArguments
from pynput import mouse

from local_file_picker import LocalFilePicker

from segbox.gui.parts import TopContainer, BottomContainer


# icons = https://fonts.google.com/icons


class SegBox:
    def __init__(self):
        self.events = None
        self.states = None

        self.mask_store = None
        self.selected_points = None

        static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        self.folders = {
            'last_visited': '~',
            'static': static_folder,
            'ui': os.path.join(static_folder, 'ui'),
            'data': os.path.join(static_folder, 'data'),
            'mask': os.path.join(static_folder, 'mask'),
        }

        with ui.row().style('width: 100%'):
            self.top_container = TopContainer(self.mouse_handler)
        with ui.row().style('width: 100%'):
            self.bottom_container = BottomContainer(self.mouse_handler)

        ui.keyboard(on_key=self.handle_key)
        listener = mouse.Listener(on_scroll=self.on_scroll)
        listener.start()

        self.init()

    def init(self):
        self.events = {
            'on_image': False,
            'mouse': {'over': False, 'down': False},
            'keys': {'shift': False, 'ctrl': False},
            'indexes': {'scroll': 0, 'image': 0, 'mask': 100},
        }

        self.states = {
            'count_images': None,
            'image_names': [],
            'radius': 0,
            'color': 'SkyBlue',
        }

        self.selected_points = {
            'mask_1': {'pos': [], 'neg': []},
            'mask_2': {'pos': [], 'neg': []},
            'mask_3': {'pos': [], 'neg': []},
            'mask_4': {'pos': [], 'neg': []},
            'mask_5': {'pos': [], 'neg': []},
            'mask_6': {'pos': [], 'neg': []},
        }

        self.mask_store = {
            'mask_1': None,
            'mask_2': None,
            'mask_3': None,
            'mask_4': None,
            'mask_5': None,
            'mask_6': None,
        }

        app.add_static_files('/static', self.folders['static'])  # serve all files in this folder

    def handle_key(self, event: KeyEventArguments) -> None:
        if event.action.keydown:
            if event.key.shift:
                self.events['keys']['shift'] = True

        if event.action.keyup:
            if event.key.shift:
                self.events['keys']['shift'] = False

    def update(self):
        static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        self.folders = {
            'last_visited': '~',
            'static': static_folder,
            'ui': os.path.join(static_folder, 'ui'),
            'data': os.path.join(static_folder, 'data'),
            'mask': os.path.join(static_folder, 'mask'),
        }

        self.states['count_images'] = len(os.listdir(self.folders['data']))
        self.states['image_names'] = os.listdir(self.folders['data'])

        app.add_static_files('/static', self.folders['data'])  # serve all files in this folder

    def __call__(self):
        with ui.header(elevated=False).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')
            ui.label('SegBox').style('color: white; font-size: 20px; font-weight: bold')
            ui.label('')

        with ui.left_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:

            with ui.card():  # Images
                ui.label('Images').style('font-weight: bold')
                ui.button('Choose files', on_click=self.pick_file).props('icon=folder').style('width: 100%')
                ui.button('Show Images', on_click=self.show_image).props('icon=camera').style('width: 100%')
                ui.button('Reset', on_click=self.reset).props('icon=restart_alt').style('width: 100%')

            with ui.card().style('margin-top: 15px'):  # Tools
                ui.label('Tools').style('font-weight: bold')
                # self.slider = ui.slider(min=0, max=100, value=15).bind_value(self.states, 'radius')
                # self.color_input = ui.color_input(label='Color', value='#000000').bind_value(self.states.get, 'color')

            with ui.card().style('margin-top: 15px'):  # Label Mask
                ui.label('Label Mask').style('font-weight: bold')
                with ui.tabs().style('width: 100%') as tabs:
                    ui.tab('1').style('width: 1%')
                    ui.tab('2').style('width: 1%')
                    ui.tab('3').style('width: 1%')
                    ui.tab('4').style('width: 1%')

                with ui.tab_panels(tabs=tabs, value='1'):
                    with ui.tab_panel('1'):
                        with ui.column():
                            ui.input(placeholder='name_1',
                                     on_change=lambda e: result.set_text('you typed: ' + e.value),
                                     validation={'Input too long': lambda value: len(value) < 20})
                            result = ui.label()

                        with ui.row().style('width: 100%'):
                            ui.label('Opacity')

                            slider = ui.slider(min=0, max=100, value=0)
                            ui.label().bind_text_from(slider, 'value')

                        with ui.row().style('margin-top: 15px'):
                            ui.button('').props('icon=delete')
                            ui.button('').props('icon=chevron_left')
                            ui.button('').props('icon=chevron_right')

                    with ui.tab_panel('2'):
                        ui.label('....')

                    with ui.tab_panel('3'):
                        ui.label('....')

                    with ui.tab_panel('4'):
                        ui.label('....')

            with ui.card().style('margin-top: 15px'):
                ui.label('Progress').style('font-weight: bold')
                slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
                ui.linear_progress().bind_value_from(slider, 'value')

        with ui.footer().style('background-color: #3874c8'):
            ui.label('MIA Lab - ARTORG - University of Bern')

        ui.run()

    def reset(self):
        """Reset the application"""
        for folder in [self.folders['data'], self.folders['mask']]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                os.mkdir(folder)
        self.init()
        self.update()
        self.reset_image_viewers()
        self.image_overlay()

    def on_scroll(self, x, y, dx, dy):
        if self.events['on_image']:
            self.events['indexes']['scroll'] += dy
            self.events['indexes']['mask'] = int(np.clip(self.events['indexes']['mask'] + dy * 5, 0, 100))
            self.events['indexes']['image'] = int(np.clip(self.events['indexes']['image'] + dy * 5, 0, 100))
            if self.events['keys']['shift'] and self.events['on_image']:
                self.image_overlay()
            # self.image_scroll()

    def update_image_viewers(self):
        if self.states['count_images']:
            if self.states['count_images'] > 3:
                width = int(95 / 3)  # 95% of the screen
            else:
                width = int(95 / self.states['count_images'])
            if self.states['count_images'] >= 1:
                self.top_container.image_1.set_source(f'static/data/{self.states["image_names"][0]}')
                self.top_container.image_1.style(f'width: {width}%')
            if self.states['count_images'] >= 2:
                self.top_container.image_2.set_source(f'static/data/{self.states["image_names"][1]}')
                self.top_container.image_2.style(f'width: {width}%')
            if self.states['count_images'] >= 3:
                self.top_container.image_3.set_source(f'static/data/{self.states["image_names"][2]}')
                self.top_container.image_3.style(f'width: {width}%')
            if self.states['count_images'] >= 4:
                self.bottom_container.image_4.set_source(f'static/data/{self.states["image_names"][3]}')
                self.bottom_container.image_4.style(f'width: {width}%')
            if self.states['count_images'] >= 5:
                self.bottom_container.image_5.set_source(f'static/data/{self.states["image_names"][4]}')
                self.bottom_container.image_5.style(f'width: {width}%')
            if self.states['count_images'] >= 6:
                self.bottom_container.image_6.set_source(f'static/data/{self.states["image_names"][5]}')
                self.bottom_container.image_6.style(f'width: {width}%')
            self.image_overlay()

    def reset_image_viewers(self):
        self.top_container.image_1.style('width: 0%').set_source('static/ui/1x1.png')
        self.top_container.image_2.style('width: 0%').set_source('static/ui/1x1.png')
        self.top_container.image_3.style('width: 0%').set_source('static/ui/1x1.png')
        self.bottom_container.image_4.style('width: 0%').set_source('static/ui/1x1.png')
        self.bottom_container.image_5.style('width: 0%').set_source('static/ui/1x1.png')
        self.bottom_container.image_6.style('width: 0%').set_source('static/ui/1x1.png')

    def mouse_handler(self, event: MouseEventArguments) -> None:
        if event.type == 'mousedown':
            if self.top_container.image_1:
                self.top_container.image_1.content += f'<circle cx="{event.image_x}" ' f'cy="{event.image_y}" '
        if event.type == 'mouseover':
            self.events['on_image'] = True
        if event.type == 'mouseout':
            self.events['on_image'] = False

    def image_overlay(self):
        mask_src = 'static/mask/mask.png'
        images = [
            self.top_container.image_1,
            self.top_container.image_2,
            self.top_container.image_3,
            self.bottom_container.image_4,
            self.bottom_container.image_5,
            self.bottom_container.image_6,
        ]
        for image in images:
            image.content = f'''
                <image xlink:href="{mask_src}" opacity="{self.events['indexes']['mask']}%" width="100%" height="100%" x="0" y="0" filter="url(#mask)" />
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
        if self.states['count_images'] > 6:
            ui.notify('Currently only 6 files are supported, choose again')
            shutil.rmtree(self.folders['data'])
            os.makedirs(self.folders['data'], exist_ok=True)

    async def pick_file(self) -> None:
        last_visited = self.folders['last_visited']
        results = await LocalFilePicker(
            directory=last_visited,
            upper_limit=os.path.expanduser('~'),
            multiple=True,
            show_hidden_files=False,
        )
        if results:
            for result in results:
                ui.notify(result)
                file_name = os.path.basename(result)
                new_path = f'{self.folders["data"]}{os.sep}{file_name}'
                self.folders['last_visited'] = os.path.dirname(result)
                print(self.folders['last_visited'])
                copy(result, new_path)
                self.update()
                # check_files()
                self.update_image_viewers()

    def show_image(self):
        self.update()
        self.update_image_viewers()
        self.image_overlay()


sb = SegBox()
sb()
