# Python-API
![CI](https://github.com/Crop-Simulator/Python-API/actions/workflows/release-build.yml/badge.svg)

## Install
### Python Version
The build is tested on [Python 3.10.2](https://www.python.org/downloads/release/python-3102/) and is our recommended Python version.
We use [pyenv](https://github.com/pyenv/pyenv) to manage our Python versions and [Poetry](https://python-poetry.org/) to manage our packages and dependencies.  

### Pyenv Setup
- For UNIX/macOS, follow [these instructions](https://github.com/pyenv/pyenv#installation) to set up pyenv locally.
- For Windows, we recommend using the officially endorsed [pyenv fork](https://github.com/pyenv-win/pyenv-win#installation). 

Once installed, use the following command in commandline to install the supported Python version.
```commandline
pyenv install 3.10.2
```
After the Python version has been installed, type `pyenv local` and ensure the output is 3.10.2

### Poetry Setup
After installing the pyenv, install 
poetry using the [official instructions](https://python-poetry.org/docs/#installation).

#### Activating the virtual environment
Once poetry is installed, type the following to activate the virtual environment:
```commandline
poetry shell
```
To deactivate the venv and exit this new shell type `exit`

### Dependency Installation
While in the active venv, use the following command to install the dependencies.
```commandline
poetry install
```
#### Managing Dependencies
To add a new dependency use `poetry add <dependency name>`
- For more guidance on dependency management refer to poetry's [official website](https://python-poetry.org/docs/managing-dependencies/).

### Launch API
While in the active venv, use the following command to run the code
```commandline
poetry run python .\src\launch.py .\data.yml
```

### Installing Blender
To install Blender following [these instructions](https://docs.blender.org/manual/en/latest/getting_started/installing/index.html). 
The build is tested on Blender 3.5 and is our recommended version.

## Linting
To lint the code we use [ruff](https://github.com/astral-sh/ruff). 
Use the following command to run Ruff over the project
```commandline
ruff check .
```
If Ruff considers an error "fixable" it can be resolved by running the following
```commandline
ruff check --fix .
```

## Testing
While in the active venv, to run the all the unit tests use the following command from the root directory of your checkout
```commandline
poetry run pytest 
```

To run a single unit test file use 
```commandline
poetry run pytest tests/test_launch.py
```

## Interactive Annotator

A semi-automation tool for conducting pixel-level segmentation annotation. Currently, supports "ground", "crop", and "weed" types.

### Start Annotator

```commandline
poetry run python .\src\machine_learning\utilities\interactive_annotator.py
```

### Initialisation and Configuration
Upon first execution, it will generate a `interactive_annotator_config.ini` file besides it and quit.
Open the `ini` file, change the "source image folder" and "output image folder" to your desired paths.

### Usage
The annotator automatically extracts ground pixels, and then you need to manually mark weed pixels out of crop pixels using various tools provided.

Keyboard operations (this guideline also appears in the title of window)
- `b`: switch to brush
- `e`: switch to eraser
- `r`: switch to rectangle fill
- `g`: switch to rectangle erase
- `x`: clear all annotation
- `space`: save current annotation and proceed to next
- `esc/q`: quit

### Settings

The annotator has a dedicated `Tools Window` for change various settings:
- `Disp Width`: zoom in or out of the image
- `Disp Mode`: switch between different display modes:
  - `0`: overlay mode: ground pixels darken, weed pixels in red
  - `1`: original image
  - `2`: ground in grey, weed in red
  - `3`: high contrast: ground in red, weed in black
- `Lower/Upper HSV`: adjust the parameters for extracting ground pixels
- `Smoothing`: 0 means no smoothing
- `Brush Size`: in pixels

The settings and your progress will be memorised when you press `space` to save and continue, so that you can enjoy your favourite settings and continue your work upon next run.


## LoRA

### Usage

Put the LoRA model to the `<stable_diffusion_webui_path>/models/Lora` folder. When generating images, put `&lt;lora:[model_name]:[weight]&gt;`, e.g., `&lt;lora:cropsim:0.5&gt;`, into positive prompt, where `model_name` is the filename of LoRA model without extension name, and `weight` is a number within 0 to 1, where 0 means the LoRA won't have any effect. 

### Training

LoRA model can be trained with [Kohya's GUI](https://github.com/bmaltais/kohya_ss). This is currently the most popular solution for LoRA training in the StableDiffusion community. There are many training guidelines available on web, such as:
- [The Ultimate Stable Diffusion LoRA Guide (Downloading, Usage, Training)](https://aituts.com/stable-diffusion-lora/)
- [How To Train Own Stable Diffusion LoRA Models – Full Tutorial!](https://techtactician.com/how-to-train-stable-diffusion-lora-models/)

According to our experiments, training on 100 images for 5 epochs can achieve a reasonable photorealistic result. Note that more epochs are not always better, where over-trained LoRA may output blurry images that contain no recognisable objects.