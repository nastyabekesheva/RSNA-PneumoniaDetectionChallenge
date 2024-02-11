from time import perf_counter

zero = perf_counter()

from os.path import splitext, basename

from pathlib import Path
from glob import glob
from shutil import rmtree

from PIL import Image
import pydicom

from tqdm import tqdm

from ultralytics import YOLO

from utils.coordinates import center_to_left_corner

one = perf_counter()
print(f'imported modules in {one - zero:.1f}s')

MODEL_PATH = './weights/best.pt'


def main():
    mount_path = Path('/mount_dir')  # specify this when starting the container !

    original_dataset_path = mount_path / 'dataset/'
    jpg_dataset_path = Path(mount_path / 'dataset_jpg/')

    if not mount_path.exists():
        print(f'Error: {mount_path} does not exist. Please mount the folder to this location.')
        return
    if not original_dataset_path.exists():
        print(
            f'Mounted folder should contain /dataset folder with .dcm files. \n({original_dataset_path} does not exist.)')
        return

    jpg_dataset_path.mkdir(exist_ok=False)  # for submission

    glob_str = str(original_dataset_path) + '/*.dcm'

    glob_ = glob(glob_str)
    n_images = len(glob_)
    print(f'Found {n_images} .dcm images')

    for img_path in tqdm(glob_, desc='.dcm to .jpg', unit=' images'):  # TODO .jpg?
        dcm_data = pydicom.dcmread(img_path)
        image_array = dcm_data.pixel_array
        image = Image.fromarray(image_array)
        image.save(jpg_dataset_path / Path(img_path).with_suffix('.jpg').name)

    print('Loading model...')
    model = YOLO(MODEL_PATH)

    results = model(jpg_dataset_path, verbose=False, stream=True, coef=0.26)

    def get_id_from_path(path):
        return splitext(basename(path))[0]

    submission_path = mount_path / 'submission.csv'
    with open(submission_path, 'w') as file:
        file.write("patientId,PredictionString\n")
        for result in tqdm(results, total=n_images, desc='Inference', unit=' images'):
            line = get_id_from_path(result.path) + ','

            for conf, xywh in zip(result.boxes.conf, result.boxes.xywh):
                x, y, w, h = center_to_left_corner(xywh)
                line += f"{conf:.2f} {x:.2f} {y:.2f} {w:.2f} {h:.2f} "

            line = line.strip()
            file.write(line + "\n")

    # TODO fix overlapping boxes

    print(f'Inference finished. \n{n_images} predictions saved to {submission_path}')

    rmtree(jpg_dataset_path, ignore_errors=True)

    print(f'total time {perf_counter() - zero:.1f}s')


if __name__ == "__main__":
    main()
