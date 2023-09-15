import gradio as gr
import numpy as np
import json

with gr.Blocks() as demo:
    logo=gr.Image(r".\images\NoHungry.svg", height=40, width=100, )
    introPic=gr.Image(r".\images\intro-page.jpg")
    gr.Dropdown(choices=[])

    with gr.Tab("English"):
        with open('.\labels-en.json', 'r') as labels:
            data = json.load(labels)

        gr.Markdown("# <p style='text-align: center;'>{}</p>".format(data['intro-title']))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format(data['intro-desc-1']))
        gr.Markdown("<p style='text-align: center;weight:400;font-size:14px;font:Gotham;'>{}</p>".format(data['intro-desc-2']))
        getStarted = gr.Button(data['get-started'], variant="primary")
        gr.Markdown("<a style='text-align: center;font-weight:400' href='foodfinder.us'>{}</a>".format(data['intro-footer-title']+ data['intro-footer-content']))
    with gr.Tab("Spanish"):
        with open('.\labels-sp.json', 'r') as labelsSpanish:
            data = json.load(labelsSpanish)

        gr.Markdown("# <p style='text-align: center;'>{}</p>".format(data['intro-title']))
        gr.Markdown("<p style='text-align: center;'>{}</p>".format(data['intro-desc-1']))
        gr.Markdown("<p style='text-align: center;weight:400;font-size:14px;font:Gotham;'>{}</p>".format(data['intro-desc-2']))
        getStarted = gr.Button(data['get-started'], variant="primary")
        gr.Markdown("<a style='text-align: center;font-weight:400' href='foodfinder.us'>{}</a>".format(data['intro-footer-title']+ data['intro-footer-content']))

demo.launch()
