# Docker Guide

## Nvidia GPU support for Stable Diffusion

The Dockerfile in this directory can be used to build a Docker image with GPU support for Stable Diffusion.

To install the Nvidia driver:

```sh
sudo apt-get update \
    && sudo apt-get install -y nvidia-container-toolkit-base
```

If `nvdia-container-toolkit-base` is not found, add the Nvidia repository to your system:

```sh
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```

Restart docker after installing the toolkit.

More detailed guide can be found in the [Nvidia documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Running the Stable Diffusion Docker image

The first step is to download all the dependencies and models. We developed a dedicated image for this purpose.

```sh
docker compose --profile download up --build
```

After the download is complete, you can run the Stable Diffusion image.

```sh
docker compose --profile auto up --build
# Or, if you want to run the image with only CPU
docker compose --profile auto-cpu up --build
```
