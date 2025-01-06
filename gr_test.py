import gradio as gr

def func(text, bool1, bool2):
	return ['latest_img_1.jpg', 'latest_img_2.jpg', 'latest_img_0.jpg', text]

outputs = [gr.Image(type="pil"),
                 gr.Image(type='pil'),
                 gr.Image(type='pil'),
                 gr.Textbox(lines=8)]
                 
inputs = [gr.Textbox(lines=2, placeholder="Change board here"),
           gr.Checkbox(label="Capture"),
           gr.Checkbox(label="Move")]

thing = gr.Interface(func, inputs, outputs)

#demo = gr.TabbedInterface([robot_control, camera_pics], ["Robot Control", "Images"])

thing.launch()
