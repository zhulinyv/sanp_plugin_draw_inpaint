from pathlib import Path

import gradio as gr

from plugins.inpaint.sanp_plugin_draw_inpaint.utils import for_webui as draw_inpaint
from utils.env import env
from utils.utils import (
    NOISE_SCHEDULE,
    RESOLUTION,
    SAMPLER,
    open_folder,
    read_json,
    return_random,
)

webui_language = read_json(f"./files/languages/{env.webui_lang}/webui.json")


def plugin():
    with gr.Tab("涂鸦重绘"):

        def open_output_folder_block(output_folder):
            open_output_folder_folder = gr.Button(
                webui_language["t2i"]["open_folder"], scale=1
            )
            open_output_folder_folder.click(
                open_folder,
                inputs=gr.Textbox(Path(f"./output/{output_folder}"), visible=False),
            )

        with gr.Row():
            with gr.Column(scale=8):
                gr.Markdown(
                    "> 对涂鸦的部分进行局部重绘(先点击重绘图片组件下方的图片按钮上传图片, 在点击绘画按钮进行局部涂抹)"
                )
            open_output_folder_block("inpaint")
        with gr.Column():
            with gr.Column():
                draw_inpaint_positive_input = gr.Textbox(
                    value=webui_language["example"]["positive"],
                    lines=2,
                    label=webui_language["t2i"]["positive"],
                )
                with gr.Row():
                    draw_inpaint_negative_input = gr.Textbox(
                        value=webui_language["example"]["negative"],
                        lines=3,
                        label=webui_language["t2i"]["negative"],
                        scale=3,
                    )
                    draw_inpaint_generate_button = gr.Button(
                        value=webui_language["t2i"]["generate_button"], scale=1
                    )
            with gr.Row():
                draw_inpaint_input_path = gr.Textbox(
                    value="", label=webui_language["inpaint"]["input_path"], scale=5
                )
                draw_inpaint_mask_path = gr.Textbox(
                    value="", label=webui_language["inpaint"]["mask_path"], scale=5
                )
                draw_inpaint_batch_switch = gr.Radio(
                    [True, False],
                    value=False,
                    label=webui_language["i2i"]["open_button"],
                    scale=1,
                )
            with gr.Row():
                draw_inpaint_input_image = gr.ImageEditor(
                    sources=["upload", "clipboard", "webcam"],
                    type="pil",
                    label=webui_language["inpaint"]["inpaint_img"],
                )
                with gr.Column():
                    draw_inpaint_output_information = gr.Textbox(
                        label=webui_language["i2i"]["output_info"]
                    )
                    draw_inpaint_output_image = gr.Image()
            with gr.Column():
                with gr.Row():
                    draw_inpaint_resolution = gr.Dropdown(
                        RESOLUTION,
                        value="832x1216",
                        label=webui_language["t2i"]["resolution"],
                    )
                    draw_inpaint_sampler = gr.Dropdown(
                        SAMPLER,
                        value="k_euler",
                        label=webui_language["t2i"]["sampler"],
                    )
                    draw_inpaint_noise_schedule = gr.Dropdown(
                        NOISE_SCHEDULE,
                        value="native",
                        label=webui_language["t2i"]["noise_schedule"],
                    )
                with gr.Row():
                    draw_inpaint_strength = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0.5,
                        step=0.1,
                        label=webui_language["i2i"]["strength"],
                    )
                    draw_inpaint_noise = gr.Slider(
                        minimum=0,
                        maximum=1,
                        value=0,
                        step=0.1,
                        label=webui_language["i2i"]["noise"],
                    )
                    draw_inpaint_scale = gr.Slider(
                        minimum=0,
                        maximum=10,
                        value=5,
                        step=0.1,
                        label=webui_language["t2i"]["scale"],
                    )
                    draw_inpaint_steps = gr.Slider(
                        minimum=0,
                        maximum=50,
                        value=28,
                        step=1,
                        label=webui_language["t2i"]["steps"],
                    )
                with gr.Row():
                    draw_inpaint_sm = gr.Radio(
                        [True, False], value=False, label="sm", scale=2
                    )
                    draw_inpaint_sm_dyn = gr.Radio(
                        [True, False],
                        value=False,
                        label=webui_language["t2i"]["smdyn"],
                        scale=2,
                    )
                    with gr.Column(scale=1):
                        draw_inpaint_seed = gr.Textbox(
                            value="-1", label=webui_language["t2i"]["seed"], scale=7
                        )
                        draw_inpaint_random_button = gr.Button(
                            value="♻️", size="sm", scale=1
                        )
                        draw_inpaint_random_button.click(
                            return_random, inputs=None, outputs=draw_inpaint_seed
                        )
        draw_inpaint_generate_button.click(
            fn=draw_inpaint,
            inputs=[
                draw_inpaint_input_path,
                draw_inpaint_mask_path,
                draw_inpaint_input_image,
                draw_inpaint_batch_switch,
                draw_inpaint_positive_input,
                draw_inpaint_negative_input,
                draw_inpaint_resolution,
                draw_inpaint_sampler,
                draw_inpaint_noise_schedule,
                draw_inpaint_strength,
                draw_inpaint_noise,
                draw_inpaint_scale,
                draw_inpaint_steps,
                draw_inpaint_sm,
                draw_inpaint_sm_dyn,
                draw_inpaint_seed,
            ],
            outputs=[draw_inpaint_output_image, draw_inpaint_output_information],
        )
