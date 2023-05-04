from __future__ import annotations
import os

from nicegui import ui


class TopContainer:
    """TopContainer, which contains the top 3 images."""""

    def __init__(self, mouse_event):
        self.viewer_1 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_event,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.viewer_2 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_event,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.viewer_3 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_event,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')


class BottomContainer:
    """BottomContainer, which contains the bottom 3 images."""""

    def __init__(self, mouse_event):
        self.viewer_4 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_event,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.viewer_5 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_event,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.viewer_6 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_event,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')


class Events:
    """Events class for handling events"""

    def __init__(self):
        self.on_image = False
        self.mouse_down = False
        self.key_shift = False
        self.key_ctrl = False
        self.scroll_index = 0
        self.image_index = 0
        self.mask_index = {
            'mask_0': 100,
            'mask_1': 100,
            'mask_2': 100,
            'mask_3': 100,
        }


class Folders:
    """Folders class for handling folders"""

    def __init__(self, source):
        static_folder = os.path.join(source, 'static')
        self.last_visited = '~'
        self.static = static_folder
        self.ui = os.path.join(static_folder, 'ui')
        self.data = os.path.join(static_folder, 'data')
        self.mask = os.path.join(static_folder, 'mask')

        for folder in [self.static, self.ui, self.data, self.mask]:
            os.makedirs(folder, exist_ok=True)


class Colors:

    def __init__(self):
        self.red = '0.87 0 0 0 0   0 0.20 0 0 0   0 0 0.30 0 0'
        self.orange = '0.96 0 0 0 0   0 0.54 0 0 0   0 0 0.37 0 0'
        self.yellow = '0.97 0 0 0 0   0 0.88 0 0 0   0 0 0.44 0 0'
        self.green = '0.58 0 0 0 0   0 0.81 0 0 0   0 0 0.57 0 0'
        self.blue = '0.21 0 0 0 0   0 0.60 0 0 0   0 0 0.80 0 0'
        self.purple = '0.59 0 0 0 0   0 0.34 0 0 0   0 0 0.64 0 0'
