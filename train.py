import sys
import os
import utils.preprocessing
from ultralytics import YOLO
import wandb

def main():
    if len(sys.argv) < 2:
        print("Usage: python train.py <path_to_file>")
        return
    dataset_path = sys.argv[1]

    print("Preprocessing dataset...")
    utils.preprocessing.main(dataset_path)
    
    model = YOLO('yolov8l.pt')
    wandb.login(key='da27b138f0f392e3f931cf71acdab08543ac649c')
    results = model.train(data='config.yaml', epochs = 1)

if __name__ == "__main__":
    main()