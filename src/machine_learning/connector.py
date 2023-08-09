import base64
import os

from .api import StableDiffusionAPI, Txt2ImgConfig

def read_segmentation_mask(path: str) -> str:
    """
    Reads a segmentation mask from a file and returns it as a base64-encoded string.

    Args:
        path (str): The path to the segmentation mask file.

    Returns:
        str: The segmentation mask as a base64-encoded string.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def encode_image(f) -> str:
    """
    Encodes an image file as a base64-encoded string.

    Args:
        f (file): The file object to encode.

    Returns:
        str: The base64-encoded image.
    """
    return base64.b64encode(f.read()).decode("utf-8")


def generate_image(api_client: StableDiffusionAPI, text_prompt: str, negative_prompt: str = "",
                   disable_controlnet: bool = False, segmentation_mask: str = None, **kwargs):
    """
    Generates an image from a given text prompt using the Stable Diffusion API.

    Args:
        api_client (api.StableDiffusionAPI): The Stable Diffusion API client.
        text_prompt (str): The text prompt to generate the image from.
        negative_prompt (str, optional): The negative text prompt to use. Defaults to "".

    Returns:
        None
    """
    # Create a Txt2ImgConfig object with the given text prompt and negative prompt
    txt2img_config = Txt2ImgConfig(prompt=text_prompt, negative_prompt=negative_prompt, **kwargs)

    # Add a controlnet segmentation to the Txt2ImgConfig object
    if not disable_controlnet:
        txt2img_config.add_controlnet_segmentation("control_v11p_sd15_seg [e1f51eb9]", segmentation_mask)

    # Generate the image using the Stable Diffusion API client
    response = api_client.txt2img(txt2img_config.to_dict())
    for k, v in response.items():
        if k != "images":
            print(f"{k}: {v}")

    return response["images"]



if __name__ == "__main__":
    url = "http://localhost:7860"
    text_prompt = "best quality, 4k, 8k, ultra highres, raw photo in hdr,\
    sharp focus, intricate texture, skin imperfections, photograph of wheat,\
    crop field, soil, sunlight, photo, photorealistic, spring, sprouting"
    disable_controlnet = os.environ.get("DISABLE_CONTROLNET", "false").lower() == "true"
    width = int(os.environ.get("WIDTH", "512"))
    height = int(os.environ.get("HEIGHT", "512"))

    sd_api_client = StableDiffusionAPI(url)
    generate_image(sd_api_client, text_prompt, disable_controlnet=disable_controlnet, width=width, height=height)

