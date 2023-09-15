import gradio as gr


def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(
    fn=greet,
    inputs=[gr.Image(".\images\home.svg"), gr.Label("Find food near you"), gr.Button("Get Started")],
    outputs=None,
)
    
demo.launch(inbrowser=True)   

