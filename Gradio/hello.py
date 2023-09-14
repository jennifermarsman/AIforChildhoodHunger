import gradio as gr

import numpy as np

def start():
        return {
            introQuestionnaire: gr.update(visible=True),
            introPage: gr.update(visible=False)
        }

def back():
        return {
            introQuestionnaire: gr.update(visible=False),
            introPage: gr.update(visible=True)
        }

 

with gr.Blocks() as demo:

    with gr.Group(visible=False) as introQuestionnaire:

        gr.Slider(2, 20, value=4, label="Count", info="Choose between 2 and 20")
        gr.Dropdown(
            ["cat", "dog", "bird"], label="Animal", info="Will add more animals later!"
        )
        gr.CheckboxGroup(["USA", "Japan", "Pakistan"], label="Countries", info="Where are they from?")
        gr.Radio(["park", "zoo", "road"], label="Location", info="Where did they go?")
        gr.Dropdown(
            ["ran", "swam", "ate", "slept"], value=["swam", "slept"], multiselect=True, label="Activity", info="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed auctor, nisl eget ultricies aliquam, nunc nisl aliquet nunc, eget aliquam nisl nunc vel nisl."
        )
        gr.Checkbox(label="Morning", info="Did they do it in the morning?")
        getStarted = gr.Button("Get started")

    with gr.Group(visible=True) as introPage:

        logo=gr.Image(r".\images\NoHungry.svg", height=20, width=60, )

        introPic=gr.Image(r".\images\Home.svg")

        gr.Dropdown(choices=[])

    

        with gr.Tab("English"):

            title = gr.Markdown("<b>Find food programs near you</b>" )

            gr.Markdown(

        """

        # Find food programs near you

        Free and private — find out which federal programs you’re eligible for, then apply for ongoing food benefits in your area.

        """)

            getStarted = gr.Button("Get started")
            getStarted.click(start,[],[introQuestionnaire,introPage])

        with gr.Tab("Spanish"):

            title = gr.Markdown("Find food programs near you", )

            desc1 = gr.Markdown("Free and private — find out which federal programs you’re eligible for, then apply for ongoing food benefits in your area. ")

            getStarted = gr.Button("Get started")
    
    with gr.Group(visible=True) as backButtonGroup:
         backButton = gr.Button("Back")
         backButton.click(back,[],[introQuestionnaire,introPage])


 

demo.launch()