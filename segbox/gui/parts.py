from __future__ import annotations

from nicegui import ui


class TopContainer:
    """TopContainer, which contains the top 3 images."""""

    def __init__(self, mouse_handler):
        self.image_1 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_handler,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.image_2 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_handler,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.image_3 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_handler,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')


class BottomContainer:
    """BottomContainer, which contains the bottom 3 images."""""

    def __init__(self, mouse_handler):
        self.image_4 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_handler,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.image_5 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_handler,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
        self.image_6 = ui.interactive_image(
            'static/ui/1x1.png',
            on_mouse=mouse_handler,
            events=['mouseover', 'mouseout', 'mousedown'],
        ).style('width: 0%')
