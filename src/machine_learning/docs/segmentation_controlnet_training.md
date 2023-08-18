# Finetuning ControlNet for Segmentation

## Prerequisites

ControlNet's training framework leverages two foundational models:

- The StableDiffusion Model: Serves as the primary model we aim to control.
- A Pre-trained ControlNet Model: This model acts as our starting point, which we then refine or finetune for our specific use-case.

The dataset comprises three core elements:

- An Input Text Prompt: This offers a detailed descriptor for our target image.
- A Control Image: Provides a segmented reference of the target image.
- The Target Image: The actual image that we aim for the ControlNet to predict or replicate, given the text prompt and control image.

The core of the training revolves around training the ControlNet to generate the target image by interpreting the input text prompt and cross-referencing it with the control image.

## Model Recommendations

For those aiming to generate lifelike, photorealistic images, we recommend integrating the following models:

- [dreamlike-photoreal](https://huggingface.co/dreamlike-art/dreamlike-photoreal-2.0)
- [Deliberate](https://civitai.com/models/4823/deliberate)

Additionally, the pre-trained ControlNet segmentation model can be accessed [here](https://huggingface.co/lllyasviel/ControlNet-v1-1/blob/main/control_v11p_sd15_seg.pth)

## Building Your Dataset

Commence by gathering your target images. Authentic photos can serve this purpose effectively.

For each target image, formulate a text prompt. It's essential for this prompt to capture intricate details of the target image, ensuring the ControlNet model comprehends the desired outcome.

Subsequently, craft a control image for each target. This image should provide a detailed segmentation map of the target image. One crucial aspect to consider during this stage is the color palette for segmentation. Ensure that the colors chosen don't overlap or conflict with the pre-defined colors for segmentation.

Refer to the color palette of the segmentation [here](https://docs.google.com/spreadsheets/d/1se8YEtb2detS7OuPE86fXGyD269pMycAWe2mtKUj2W8/edit#gid=0).

## Training

Here's a sample code snippet for training the ControlNet model:

```python
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from tutorial_dataset import MyDataset
from cldm.logger import ImageLogger
from cldm.model import create_model, load_state_dict


# Configs
resume_path = './models/control_sd15_ini.ckpt'
batch_size = 4
logger_freq = 300
learning_rate = 1e-5
sd_locked = True
only_mid_control = False


# First use cpu to load models. Pytorch Lightning will automatically move it to GPUs.
model = create_model('./models/cldm_v15.yaml').cpu()
model.load_state_dict(load_state_dict(resume_path, location='cpu'))
model.learning_rate = learning_rate
model.sd_locked = sd_locked
model.only_mid_control = only_mid_control


# Misc
dataset = MyDataset()
dataloader = DataLoader(dataset, num_workers=0, batch_size=batch_size, shuffle=True)
logger = ImageLogger(batch_frequency=logger_freq)
trainer = pl.Trainer(gpus=1, precision=32, callbacks=[logger])


# Train!
trainer.fit(model, dataloader)
```

## Reference

- [Train a ControlNet to Control SD](https://github.com/lllyasviel/ControlNet/blob/main/docs/train.md)
