from __future__ import annotations

import time
import os
import shutil

import numpy as np

from nicegui import app, ui
from nicegui.events import MouseEventArguments, KeyEventArguments
from pynput import mouse

from segbox.core.local_file_picker import LocalFilePicker

from segbox.gui.parts import TopContainer, BottomContainer, Events, Folders, Colors
from segbox.core.states import States
from segbox.core.reader import Reader

from segbox.sam.segment_anything import SamPredictor, sam_model_registry


# icons = https://fonts.google.com/icons


class SegBox:
    def __init__(self):
        self.viewers = None

        self.state = States()
        self.data_reader = Reader()

        self.events = Events()
        self.colors = Colors()

        source = os.path.dirname(os.path.abspath(__file__))
        self.folders = Folders(source)

        ui.keyboard(on_key=self._key_event)
        listener = mouse.Listener(on_scroll=self._scroll_event)
        listener.start()

        self.model_path = os.path.join(source, 'sam', 'models', 'sam_vit_b_01ec64.pth')
        self.sam = sam_model_registry['vit_b'](checkpoint=self.model_path)
        self.sam.to(device='cuda', )

        self.predictor = SamPredictor(self.sam)

        app.add_static_files('/static', self.folders.static)  # serve all files in this folder

    def _key_event(self, event: KeyEventArguments) -> None:
        """Handle key events."""
        if event.action.keydown:
            if event.key.shift:
                self.events.key_shift = True

        if event.action.keyup:
            if event.key.shift:
                self.events.key_shift = False

    def _scroll_event(self, x: int, y: int, dx: int, dy: int) -> None:
        """Handle scroll events."""
        if self.events is not None:
            if self.events.on_image:
                self.events.scroll_index += dy

                if self.events.key_shift:
                    mask_number = self.state.get_gui('mask_number')
                    mask_index = self.events.mask_index[f'mask_{mask_number}']
                    self.events.mask_index[f'mask_{mask_number}'] = int(np.clip(mask_index + dy * 5, 0, 100))
                    self.mask_overlay()

                if not self.events.key_shift:
                    self.events.image_index = int(np.clip(self.events.image_index + dy * 5, 0, 100))

    def _mouse_event(self, event: MouseEventArguments) -> None:
        if event.type == 'mousedown':
            if self.top_container.viewer_1:
                self.state.set_gui(time_stamp=time.time())
                self.state.add_mask_iteration()

                points = self.state.get_mask('points')
                points.append([event.image_x, event.image_y])
                self.state.set_mask(points=points)

                labels = self.state.get_mask('labels')
                labels.append(self.state.get_gui('mask_mode'))
                self.state.set_mask(labels=labels)

                self.run_sam()
                self.update_viewers()
                self.mask_overlay(reload=True)

        if event.type == 'mouseover':
            self.events.on_image = True

        if event.type == 'mouseout':
            self.events.on_image = False

    def add_mask_mode(self):
        self.state.set_gui(mask_mode=1)
        ui.notify('Click on the area where you want to add mask')

    def remove_mask_mode(self):
        self.state.set_gui(mask_mode=0)
        ui.notify('Click on the area where you want to remove mask')

    def reset_masks(self):
        mask_number = self.state.get_gui('mask_number')
        ui.notify(f'Reset mask {mask_number + 1}')

        self.state.reset_mask()
        self.mask_overlay(reload=True)

        masks = os.listdir(self.folders.mask)
        for mask in masks:
            if f'mask_{mask_number}' in mask:
                os.remove(os.path.join(self.folders.mask, mask))

    def set_mask_number(self, number: int):
        zero_based_number = number - 1
        self.state.set_gui(mask_number=zero_based_number)
        self.mask_overlay(reload=True)
        self.state.set_gui(mask_mode=1)

    def increase_mask_iteration(self):
        current_iteration, max_iteration = self.state.get_mask_iteration()
        if current_iteration < max_iteration:
            self.state.set_mask_iteration(current_iteration + 1)
            self.mask_overlay(reload=True)

    def decrease_mask_iteration(self):
        current_iteration, max_iteration = self.state.get_mask_iteration()
        if current_iteration > 0:
            self.state.set_mask_iteration(current_iteration - 1)
            self.mask_overlay(reload=True)

    def set_mask_name(self, mask_number: int, name: str):
        self.state.set_mask_name(mask_number, name)

    def __call__(self) -> None:
        """Run the app."""

        with ui.row().style('width: 100%'):
            self.top_container = TopContainer(self._mouse_event)
        with ui.row().style('width: 100%'):
            self.bottom_container = BottomContainer(self._mouse_event)

        self.viewers = [
            self.top_container.viewer_1,
            self.top_container.viewer_2,
            self.top_container.viewer_3,
            self.bottom_container.viewer_4,
            self.bottom_container.viewer_5,
            self.bottom_container.viewer_6,
        ]

        self.reset()

        with ui.header(elevated=False).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')
            ui.label('SegBox').style('color: white; font-size: 20px; font-weight: bold')
            ui.label('')

        with ui.left_drawer(fixed=False).style('background-color: #ebf1fa').props('bordered') as right_drawer:
            with ui.card():  # Images
                with ui.table.row().style('width: 100%'):
                    ui.label('Images').style('font-weight: bold')
                with ui.table.row().style('width: 100%'):
                    ui.button('Choose files', on_click=self.pick_file).props('icon=folder').style('width: 100%')
                with ui.table.row().style('width: 100%'):
                    ui.button('Reset', on_click=self.reset).props('icon=restart_alt').style('width: 100%')

            with ui.card().style('margin-top: 15px'):  # Label Mask
                ui.label('Label Mask').style('font-weight: bold')
                with ui.tabs().style('width: 100%') as tabs:
                    for tab_number in [1, 2, 3, 4]:
                        tab = ui.tab(f'{tab_number}', label=f'{tab_number}').style('width: 1%')
                        tab.on(type='click', handler=lambda _, x=tab_number: self.set_mask_number(x))

                with ui.tab_panels(tabs=tabs, value='1'):
                    for tab_number in [1, 2, 3, 4]:
                        with ui.tab_panel(str(tab_number)):
                            ui.input(placeholder=self.state.get_mask_name(tab_number), on_change=lambda e, x=tab_number: self.set_mask_name(x, e.value))

                            with ui.row().style('margin-top: 15px'):
                                ui.button('', on_click=self.add_mask_mode).props('icon=add')
                                ui.button('', on_click=self.remove_mask_mode).props('icon=remove')

                            with ui.row().style('margin-top: 15px'):
                                ui.button('', on_click=self.decrease_mask_iteration).props('icon=chevron_left')
                                ui.button('', on_click=self.increase_mask_iteration).props('icon=chevron_right')

                            with ui.row().style('margin-top: 15px'):
                                ui.button('', on_click=self.reset_masks).props('icon=delete')
                                ui.button('', on_click=self.save_masks).props('icon=save')

            with ui.card().style('margin-top: 15px'):
                ui.label('Progress').style('font-weight: bold')
                # ui.button('Start', on_click=self.run_sam)
                slider = ui.slider(min=0, max=1, step=0.01, value=0.5)
                ui.linear_progress().bind_value_from(slider, 'value')

        with ui.footer().style('background-color: #3874c8'):
            ui.label('MIA Lab - ARTORG - University of Bern')

        ui.run(title='SegBox')

    def save_masks(self):
        """Save the masks"""
        mask_number = self.state.get_gui('mask_number')
        mask_name = self.state.get_gui(f'name_{mask_number}')

        for mask in self.state.get_masks():
            mask.save()

    def reset(self) -> None:
        """Reset the application"""
        for folder in [self.folders.data, self.folders.mask]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                os.mkdir(folder)
        self.state.reset_mask()
        self.reset_viewers()

    def get_index(self) -> int:
        """Get the index of the image, 0 for 2D and scroll index for 3D"""
        if self.state.get_gui('image_slices') > 1:
            return self.events.image_index
        return 0

    def update_viewers(self, reload: bool = False) -> None:
        """Update the viewers"""
        if reload:
            self.state.set_gui(time_stamp=time.time())
        viewer_width = self.state.get_gui('viewer_width')
        image_count = self.state.get_gui('image_count')
        slice_number = self.get_index()
        if image_count:
            time_stamp = self.state.get_gui('time_stamp')

            for image_number, image in enumerate(self.viewers):
                if image_number < image_count:
                    image.set_source(f'static/data/img_{image_number}_sl_{slice_number}.png?t={time_stamp}')
                    image.style(f'width: {viewer_width}%')

    def reset_viewers(self) -> None:
        """Reset the viewers"""
        for viewer in self.viewers:
            viewer.style('width: 0%').set_source('static/ui/1x1.png')

    def mask_overlay(self, reload: bool = False) -> None:
        """Update the mask overlay"""
        if reload:
            self.state.set_gui(time_stamp=time.time())

        slice_number = self.get_index()
        time_stamp = self.state.get_gui('time_stamp')

        mask_iterations = self.state.get_gui('mask_iterations')

        for viewer in self.viewers:

            viewer.content = ''''''
            for mask_number, color in zip([0, 1, 2, 3], [self.colors.red, self.colors.green, self.colors.blue, self.colors.purple]):
                if mask_iterations[f'mask_{mask_number}'] == 0:
                    continue
                if os.path.exists(f'static/mask/mask_{mask_number}_it_{mask_iterations[f"mask_{mask_number}"]}_sl_{slice_number}.png'):
                    viewer.content += f'''<g><image xlink:href="static/mask/mask_{mask_number}_it_{mask_iterations[f'mask_{mask_number}']}_sl_{slice_number}.png?t={time_stamp}" opacity="{self.events.mask_index[f'mask_{mask_number}']}%" width="100%" height="100%" x="0" y="0" filter="url(#mask_{mask_number})" />
                          <filter id="mask_{mask_number}">
                            <feComponentTransfer>
                               <feFuncR type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                               <feFuncG type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                               <feFuncB type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                               <feFuncR type="linear" slope="1000"/>
                            </feComponentTransfer>
                          <feColorMatrix type="matrix" values="{color}  3 -1 -1 0 0" />
                          </filter></g>'''



    async def pick_file(self) -> None:
        paths = await LocalFilePicker(
            directory=self.folders.last_visited,
            upper_limit=os.path.expanduser('~'),
            multiple=True,
            show_hidden_files=False,
        )

        if paths:
            self.folders.last_visited = os.path.dirname(paths[0])

            for index, path in enumerate(sorted(paths)):
                if index >= 6:
                    break
                self.data_reader.add_image(index, path)

            error = self.data_reader(self.folders.data)

            if error:
                self.dialog(error)
                self.reset_viewers()
            else:
                self.update_viewers()
                self.predictor.set_image(self.state.get_img(0, 'array'))

    @staticmethod
    def dialog(message: str, dialog_type: str = 'Info') -> None:
        with ui.dialog() as dialog, ui.card():
            ui.label(dialog_type)
            ui.label(message)
            ui.label(message)
            ui.button('Close', on_click=dialog.close)
        dialog.open()

    def run_sam(self) -> None:
        """Run SAM on the current image"""
        input_points = np.asarray(self.state.get_mask('points'))
        input_labels = np.asarray(self.state.get_mask('labels'))
        mask_input = self.state.get_mask('logits')

        if mask_input is None:  # If no mask is selected, use the highest scoring mask
            masks, scores, logits = self.predictor.predict(
                point_coords=input_points,
                point_labels=input_labels,
                multimask_output=True,
            )
            mask_input = logits[np.argmax(scores), :, :]
            self.state.set_mask(logits=mask_input)
            mask = masks[np.argmax(scores), :, :]

        else:  # If a mask is selected, use it single mask prediction
            mask, _, _ = self.predictor.predict(
                point_coords=input_points,
                point_labels=input_labels,
                mask_input=mask_input[None, :, :],
                multimask_output=False,
            )
            mask = mask[0, :, :]

        self.state.set_mask(mask=mask)
        self.state.save_tmp_mask(self.folders.mask)


sb = SegBox()
sb()
