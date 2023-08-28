# Machine Learning Connector

## Getting Started

First, make sure that the StableDiffusion API is up and running. Checkout the [README](../../docker/README.md) for more information.

The machine learning pipeline has a filesystem watcher that watches for the output from the Blender pipeline. New outputs are automatically processed by the machine learning pipeline.
From the project root directory, run the following command to start the watcher:

```sh
poetry run python -m src.machine_learning.watcher
```

StableDiffusion image outputs are stored in the working directory.
