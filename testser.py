#!/usr/bin/env python3
from nicegui import ui, app
from pathlib import Path

img_src = 'https://i.stack.imgur.com/PpIqU.png'
mask_src = 'https://i.stack.imgur.com/OfwWp.png'


folder = Path(__file__).resolve().parent / 'segbox' / 'static'
app.add_static_files('/static', folder)  # serve all files in this folder


with ui.row().classes('w-full flex items-center'):
    img_src = 'static/data/img_0_sl_0.png'
    mask_src_1 = 'static/mask/mask_0_it_1_sl_0.png'
    mask_src_2 = 'static/mask/mask_0_it_2_sl_0.png'


    image = ui.interactive_image(img_src).style('width: 25%')

    image.content = f'''
          <image xlink:href="{mask_src_1}" width="100%" height="100%" x="0" y="0" opacity="100%" filter="url(#mask)" />
          <filter id="mask">
              <feComponentTransfer>
                  <feFuncR type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                  <feFuncG type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                  <feFuncB type="linear" slope="40" intercept="-(0.5 * 40) + 0.5"/>
                  <feFuncR type="linear" slope="1000"/>
              </feComponentTransfer>
              
             <feMorphology in="SourceAlpha" operator="dilate" radius="1" result="dilated"/>
               <feComposite in="dilated" in2="SourceAlpha" operator="out" result="out"/>
               <feFlood flood-color="black" flood-opacity="1" result="border-color"/>
               <feComposite in="border-color" in2="out" operator="in" result="border"/>
               # <feComposite in="border" in2="SourceGraphic" operator="over" result="final"/>
         
         
               
              <feColorMatrix type="matrix" values="0 0 0 0 0   0 1 0 0 0   0 0 1 0 0  3 -1 -1 0 0" />
                    <rect width="100%" height="100%" stroke="#000000" stroke-width="10" fill="none" />
          </filter>
         
      '''



ui.run()
