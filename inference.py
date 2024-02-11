from time import perf_counter

zero = perf_counter()

import sys
from os.path import splitext, basename

from pathlib import Path
from glob import glob

from PIL import Image
import pydicom

from tqdm import tqdm

from ultralytics import YOLO

from utils.coordinates import center_to_left_corner
import os

one = perf_counter()
print(f'imported modules in {one - zero:.1f}s')

MODEL_PATH = './weights/best.pt'


def main():
    if len(sys.argv) < 2:
        print("Usage: python inference.py <path_to_file>")
        return

    original_dataset_path = sys.argv[1]
    dataset_path = Path('./test_set_jpg/')

    # dataset_path.mkdir(exist_ok=False) # for submission
    dataset_path.mkdir(exist_ok=True)  # for debugging

    two = perf_counter()
    glob_ = glob(original_dataset_path + '/*.dcm')
    n_images = len(glob_)

    for img_path in tqdm(glob_, desc='.dcm to .jpg', unit=' images'):  # TODO .jpg?
        dcm_data = pydicom.dcmread(img_path)
        image_array = dcm_data.pixel_array
        image = Image.fromarray(image_array)
        image.save(dataset_path / Path(img_path).with_suffix('.jpg').name)

    print('Loading model...')
    model = YOLO(MODEL_PATH)

    results = model(dataset_path, verbose=False, stream=True, conf=0.26)

    def get_id_from_path(path):
        return splitext(basename(path))[0]

    with open('submission.csv', 'w') as file:
        file.write("patientId,PredictionString\n")
        for result in tqdm(results, total=n_images, desc='Inference', unit=' images'):
            line = get_id_from_path(result.path) + ','

            for conf, xywh in zip(result.boxes.conf, result.boxes.xywh):
                x, y, w, h = center_to_left_corner(xywh)
                line += f"{conf:.2f} {x:.2f} {y:.2f} {w:.2f} {h:.2f} "

            line = line.strip()
            file.write(line + "\n")

    #print(f'Inference finished. {len(results)} results saved to submission.csv')
    print(f'Inference finished. Results saved to submission.csv')

    print(f'total time {perf_counter() - zero:.1f}s')


if __name__ == "__main__":
    main()
