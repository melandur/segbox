#!/usr/bin/env python3
from nicegui import ui

img_src = 'https://i.stack.imgur.com/PpIqU.png'
mask_src = 'https://i.stack.imgur.com/OfwWp.png'

with ui.row().classes('w-full flex items-center'):
    ui.image(img_src).style('width: 25%')
    ui.label('+').style('font-size: 18em')
    ui.image(mask_src).style('width: 25%')
    ui.label('=').style('font-size: 18em')
    image = ui.interactive_image(img_src).style('width: 25%')


ui.run()
