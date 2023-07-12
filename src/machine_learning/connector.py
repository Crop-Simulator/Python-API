import base64

import api


def generate_image(api_client: api.StableDiffusionAPI, text_prompt: str):
    txt2img_config = {
        "enable_hr": False,
        "denoising_strength": 0,
        "firstphase_width": 0,
        "firstphase_height": 0,
        "hr_scale": 2,
        "hr_upscaler": "string",
        "hr_second_pass_steps": 0,
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_sampler_name": "string",
        "hr_prompt": "",
        "hr_negative_prompt": "",
        "prompt": text_prompt,
        "styles": ["string"],
        "seed": -1,
        "subseed": -1,
        "subseed_strength": 0,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "sampler_name": "Euler",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 25,
        "cfg_scale": 7,
        "width": 400,
        "height": 400,
        "restore_faces": False,
        "tiling": False,
        "do_not_save_samples": False,
        "do_not_save_grid": False,
        "negative_prompt": "",
        "eta": 0,
        "s_min_uncond": 0,
        "s_churn": 0,
        "s_tmax": 0,
        "s_tmin": 0,
        "s_noise": 1,
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "script_args": [],
        "sampler_index": "Euler",
        "script_name": "",
        "send_images": True,
        "save_images": False,
        "alwayson_scripts": {},
    }

    response = api_client.txt2img(txt2img_config)

    # save the images to disk
    for idx, img in enumerate(response["images"]):
        with open(f"img_{idx}.png", "wb") as f:
            f.write(base64.decodebytes(bytes(img, "utf-8")))
        print(f"Image {idx} saved to img_{idx}.png")


url = "http://localhost:7860"
text_prompt = "best quality, 4k, 8k, ultra highres, raw photo in hdr,\
sharp focus, intricate texture, skin imperfections, photograph of wheat,\
crop field, soil, sunlight, photo, photorealistic, spring, sprouting"

sd_api_client = api.StableDiffusionAPI(url)
generate_image(text_prompt)
