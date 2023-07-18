import base64
import api


def read_segmentation_mask(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_image(api_client: api.StableDiffusionAPI, text_prompt: str, negative_prompt: str = ""):
    txt2img_config = api.Txt2ImgConfig(prompt=text_prompt, negative_prompt=negative_prompt)
    txt2img_config.add_controlnet_segmentation("control_v11p_sd15_seg [e1f51eb9]", read_segmentation_mask("test_seg1.png"))
    print(txt2img_config.to_dict())
    response = api_client.txt2img(txt2img_config.to_dict())

    for k, v in response.items():
        if k != "images":
            print(f"{k}: {v}")
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
generate_image(sd_api_client, text_prompt)