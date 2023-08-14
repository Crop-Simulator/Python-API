import base64

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


def generate_image(api_client: StableDiffusionAPI, config: dict, controlnet_config: dict = None):
    """
    Generates an image from a given text prompt using the Stable Diffusion API.

    Args:
        api_client (api.StableDiffusionAPI): The Stable Diffusion API client.
        config (dict): A dictionary containing the configuration for generating the image.
        controlnet_settings (dict): A dictionary containing the controlnet settings.

    Returns:
        None
    """
    # Create a Txt2ImgConfig object with the given text prompt and negative prompt
    txt2img_config = Txt2ImgConfig(**config)

    # Add a controlnet segmentation to the Txt2ImgConfig object
    if controlnet_config and not controlnet_config.get("disable_controlnet", False):
        txt2img_config.add_controlnet_segmentation("control_v11p_sd15_seg [e1f51eb9]",
                                                    controlnet_config.get("segmentation_mask"),
                                                    controlnet_config.get("depth_mask"))

    # Generate the image using the Stable Diffusion API client
    response = api_client.txt2img(txt2img_config.to_dict())
    for k, v in response.items():
        if k != "images":
            print(f"{k}: {v}")

    return response["images"]
