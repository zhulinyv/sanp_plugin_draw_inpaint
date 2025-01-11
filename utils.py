import random

import ujson as json

from src.image2image import prepare_json
from utils.imgtools import (
    change_the_mask_color_to_white,
    get_img_info,
    img_to_base64,
    revert_img_info,
)
from utils.prepare import logger
from utils.utils import (
    file_namel2pathl,
    file_path2list,
    file_path2name,
    generate_image,
    return_x64,
    save_image,
)


def for_webui(
    input_path,
    mask_path,
    draw_inpaint_input_image,
    draw_inpaint_overlay,
    open_button,
    draw_inpaint_positive_input,
    draw_inpaint_negative_input,
    inpaint_width,
    inpaint_height,
    draw_inpaint_sampler,
    draw_inpaint_noise_schedule,
    draw_inpaint_strength,
    draw_inpaint_noise,
    draw_inpaint_scale,
    draw_inpaint_steps,
    draw_inpaint_sm,
    draw_inpaint_sm_dyn,
    draw_inpaint_variety,
    draw_inpaint_decrisp,
    draw_inpaint_seed,
):
    if open_button:
        main(input_path, mask_path, draw_inpaint_overlay)
        return None, "处理完成, 图片已保存到 ./output/inpaint..."
    else:
        (draw_inpaint_input_image["composite"]).save(
            "./output/temp_draw_inpaint_img.png"
        )
        (draw_inpaint_input_image["layers"][0]).save(
            "./output/temp_draw_inpaint_mask.png"
        )
        change_the_mask_color_to_white("./output/temp_draw_inpaint_mask.png")

        info = {
            "Software": "NovelAI",
            "Comment": json.dumps(
                {
                    "prompt": draw_inpaint_positive_input,
                    "steps": draw_inpaint_steps,
                    "height": return_x64(int(inpaint_height)),
                    "width": return_x64(int(inpaint_width)),
                    "scale": draw_inpaint_scale,
                    "seed": (
                        random.randint(1000000000, 9999999999)
                        if draw_inpaint_seed == "-1"
                        else int(draw_inpaint_seed)
                    ),
                    "noise_schedule": draw_inpaint_noise_schedule,
                    "sampler": draw_inpaint_sampler,
                    "sm": draw_inpaint_sm,
                    "sm_dyn": draw_inpaint_sm_dyn,
                    "skip_cfg_above_sigma": (19 if draw_inpaint_variety else None),
                    "dynamic_thresholding": draw_inpaint_decrisp,
                    "uc": draw_inpaint_negative_input,
                }
            ),
        }

        revert_img_info(None, "./output/temp_draw_inpaint_img.png", info)

        logger.info("开始重绘...")
        path = inpaint(
            "./output/temp_draw_inpaint_img.png",
            "./output/temp_draw_inpaint_mask.png",
            draw_inpaint_overlay,
            draw_inpaint_strength,
            draw_inpaint_noise,
        )
    return path, None


def inpaint(img_path, mask_path, inpaint_overlay, *args):
    imginfo = get_img_info(img_path)
    json_for_inpaint = prepare_json(imginfo, img_path)
    json_for_inpaint["parameters"]["mask"] = img_to_base64(mask_path)
    json_for_inpaint["model"] = "nai-diffusion-3-inpainting"
    json_for_inpaint["action"] = "infill"
    json_for_inpaint["add_original_image"] = inpaint_overlay
    if args:
        json_for_inpaint["strength"] = args[0]
        json_for_inpaint["noise"] = args[1]

    saved_path = save_image(
        generate_image(json_for_inpaint),
        "inpaint",
        json_for_inpaint["parameters"]["seed"],
        "None",
        "None",
    )

    return saved_path


def main(img_folder, mask_folder, inpaint_overlay):
    file_list = file_namel2pathl(file_path2list(img_folder), img_folder)

    for file in file_list:
        logger.info(f"正在处理: {file}")
        inpaint(file, f"{mask_folder}/{file_path2name(file)}", inpaint_overlay)
