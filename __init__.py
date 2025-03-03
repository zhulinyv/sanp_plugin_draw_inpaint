from pathlib import Path

import gradio as gr

from plugins.inpaint.sanp_plugin_draw_inpaint.utils import for_webui as draw_inpaint
from src.text2image_nsfw import return_resolution
from utils.env import env
from utils.utils import (
    CHARACTER_POSITION,
    FAVORTES_FILE,
    NOISE_SCHEDULE,
    RESOLUTION,
    SAMPLER,
    add_wildcard_to_textbox,
    open_folder,
    read_json,
    return_random,
    return_wildcard_tag,
    update_image_size,
    update_name_to_dropdown_list,
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
            with gr.Tab("生成参数"):
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
                    with gr.Column():
                        draw_inpaint_input_image = gr.ImageEditor(
                            sources=["upload", "clipboard", "webcam"],
                            type="pil",
                            label=webui_language["inpaint"]["inpaint_img"],
                        )
                        draw_inpaint_input_image.change(
                            update_image_size,
                            inputs=draw_inpaint_input_image,
                            outputs=draw_inpaint_input_image,
                        )
                        draw_inpaint_overlay = gr.Checkbox(
                            False, label="Overlay Original Image"
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
                            value=(
                                "832x1216"
                                if env.img_size == -1
                                else "{}x{}".format(
                                    (env.img_size)[0], (env.img_size)[1]
                                )
                            ),
                            label=webui_language["t2i"]["resolution"],
                        )
                        draw_inpaint_width = gr.Textbox(
                            value="832", label=webui_language["t2i"]["width"]
                        )
                        draw_inpaint_height = gr.Textbox(
                            value="1216", label=webui_language["t2i"]["height"]
                        )
                        draw_inpaint_resolution.change(
                            return_resolution,
                            draw_inpaint_resolution,
                            outputs=[draw_inpaint_width, draw_inpaint_height],
                            show_progress="hidden",
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
                        draw_inpaint_rescale = gr.Slider(
                            minimum=0,
                            maximum=1,
                            value=env.rescale,
                            step=0.01,
                            label="Prompt Guidance Rescale",
                        )
                        draw_inpaint_steps = gr.Slider(
                            minimum=0,
                            maximum=50,
                            value=28,
                            step=1,
                            label=webui_language["t2i"]["steps"],
                        )
                    with gr.Row():
                        with gr.Column():
                            draw_inpaint_sm = gr.Checkbox(
                                value=False,
                                label="sm",
                                scale=2,
                                visible=(
                                    False if "nai-diffusion-4" in env.model else True
                                ),
                            )
                            draw_inpaint_sm_dyn = gr.Checkbox(
                                value=False,
                                label=webui_language["t2i"]["smdyn"],
                                scale=2,
                                visible=(
                                    False if "nai-diffusion-4" in env.model else True
                                ),
                            )
                        with gr.Column():
                            draw_inpaint_variety = gr.Checkbox(
                                value=False, label="variety"
                            )
                            draw_inpaint_decrisp = gr.Checkbox(
                                value=(
                                    env.decrisp
                                    if "nai-diffusion-4" not in env.model
                                    else False
                                ),
                                label="decrisp",
                                visible=(
                                    True
                                    if "nai-diffusion-4" not in env.model
                                    else False
                                ),
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
            with gr.Tab("wildcards"):
                with gr.Row():
                    draw_inpaint_wildcard_file = gr.Dropdown(
                        choices=FAVORTES_FILE,
                        value="",
                        label="wildcard文件",
                    )
                    draw_inpaint_wildcard_name = gr.Dropdown(label="名称")
                    draw_inpaint_wildcard_file.change(
                        update_name_to_dropdown_list,
                        inputs=draw_inpaint_wildcard_file,
                        outputs=draw_inpaint_wildcard_name,
                    )
                    draw_inpaint_add_wildcard_button = gr.Button("添加到文本框")
                    draw_inpaint_add_wildcard_button.click(
                        add_wildcard_to_textbox,
                        inputs=[
                            draw_inpaint_positive_input,
                            draw_inpaint_negative_input,
                            draw_inpaint_wildcard_file,
                            draw_inpaint_wildcard_name,
                        ],
                        outputs=[
                            draw_inpaint_positive_input,
                            draw_inpaint_negative_input,
                        ],
                    )
                draw_inpaint_wildcard_tag = gr.Textbox(label="tag")
                draw_inpaint_wildcard_name.change(
                    return_wildcard_tag,
                    inputs=[draw_inpaint_wildcard_file, draw_inpaint_wildcard_name],
                    outputs=draw_inpaint_wildcard_tag,
                )
            with gr.Tab(
                "Character", visible=True if "nai-diffusion-4" in env.model else False
            ):
                draw_inpaint_ai_choice = gr.Checkbox(
                    True, label="AI 选择位置(AI's choice)"
                )
                gr.Markdown("<hr>")

                def character_compents(number):
                    with gr.Row():
                        draw_inpaint_character_position = gr.Dropdown(
                            CHARACTER_POSITION, label="位置(Position)"
                        )
                        draw_inpaint_character_switch = gr.Checkbox(
                            False, label="启用(Switch)"
                        )
                        gr.Textbox(f"角色{number}", show_label=False)
                    with gr.Row():
                        draw_inpaint_character_positive = gr.Textbox(
                            label="正面提示词(Positive)", lines=3
                        )
                        draw_inpaint_character_negative = gr.Textbox(
                            label="负面提示词(Negative)", lines=3
                        )
                    for _ in range(3):
                        gr.Markdown("<hr>")
                    return (
                        draw_inpaint_character_switch,
                        draw_inpaint_character_positive,
                        draw_inpaint_character_negative,
                        draw_inpaint_character_position,
                    )

                draw_inpaint_components_list = [
                    character_compents(num) for num in range(1, 7)
                ]
                draw_inpaint_new_components_list = [
                    component
                    for components in draw_inpaint_components_list
                    for component in components
                ]
        draw_inpaint_generate_button.click(
            fn=draw_inpaint,
            inputs=[
                draw_inpaint_input_path,
                draw_inpaint_mask_path,
                draw_inpaint_input_image,
                draw_inpaint_overlay,
                draw_inpaint_batch_switch,
                draw_inpaint_positive_input,
                draw_inpaint_negative_input,
                draw_inpaint_width,
                draw_inpaint_height,
                draw_inpaint_sampler,
                draw_inpaint_noise_schedule,
                draw_inpaint_strength,
                draw_inpaint_noise,
                draw_inpaint_scale,
                draw_inpaint_rescale,
                draw_inpaint_steps,
                draw_inpaint_sm,
                draw_inpaint_sm_dyn,
                draw_inpaint_variety,
                draw_inpaint_decrisp,
                draw_inpaint_seed,
            ]
            + [draw_inpaint_ai_choice]
            + draw_inpaint_new_components_list,
            outputs=[draw_inpaint_output_image, draw_inpaint_output_information],
        )
