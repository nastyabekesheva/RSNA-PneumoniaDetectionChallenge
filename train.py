import sys
from RSNA_PneumoniaDetectionChallenge.utils.preprocessing import preprocess
from ultralytics import YOLO
from pathlib import Path

import wandb


def write_config_yaml(transformed_dataset_path: str):
    with open('config.yaml', 'w') as f:
        config = \
            f"""path: '{transformed_dataset_path}' # dataset root dir
train: images/train  # train images (relative to 'path')
val: images/val  # val images (relative to 'path')

# Classes
names:
  0: pneumonia"""

        f.write(config)


def train(transformed_dataset_path: str):
    wandb.login(key='f69ae6e7564feaf1e47f90164e1b2f9598492168')

    write_config_yaml(transformed_dataset_path)

    model = YOLO('yolov8l.pt')

    print('Training model...\n')
    results = model.train(data='config.yaml', project='weights', epochs=100)


def main():
    if len(sys.argv) < 2:
        print("Usage: python train.py <path_to_dataset>")
        print("Usage: python train.py x <path_to_preprocessed_dataset>")
        return

    if sys.argv[1] == 'x':
        if len(sys.argv) < 3:
            print("Usage: python train.py x <path_to_preprocessed_dataset>")
            return
        transformed_dataset_path = sys.argv[2]
    else:
        dataset_path = sys.argv[1]

        print("Preprocessing dataset...")
        transformed_dataset_path = preprocess(dataset_path)

    transformed_dataset_path = str(Path(transformed_dataset_path).resolve())

    train(transformed_dataset_path)


if __name__ == "__main__":
    main()
