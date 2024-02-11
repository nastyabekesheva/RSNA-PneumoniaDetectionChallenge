import numpy as np
import pandas as pd
import os
import shutil

import pydicom
from PIL import Image

from tqdm import tqdm

np.random.seed(42)

from sklearn.model_selection import train_test_split

from pathlib import Path
from RSNA_PneumoniaDetectionChallenge.utils.coordinates import translate_bbox

IMG_SIZE = 1024
TRANSFORMED_DATASET_DIR = './transformed_dataset/'

def save_label(label_dir, patient_id, bbox):
    label_fp = os.path.join(label_dir, patient_id + '.txt')

    f = open(label_fp, "a")
    if (bbox == 'nan').all():
        f.close()
        return

    x, y, w, h = translate_bbox(bbox)

    line = f"0 {x} {y} {w} {h}\n"

    f.write(line)
    f.close()


def dilute_annotations(annotations: pd.DataFrame, dilution_n: int = 600):
    positive_annotations = annotations[annotations.Target == 1]
    negative_annotations = annotations[annotations.Target == 0]
    negative_sample = negative_annotations.sample(dilution_n)

    annotations = pd.concat([positive_annotations, negative_sample])

    return annotations


def make_transformed_dataset_dirs():
    Path(TRANSFORMED_DATASET_DIR + 'labels/train/').mkdir(parents=True, exist_ok=True)
    Path(TRANSFORMED_DATASET_DIR + 'labels/val/').mkdir(parents=True, exist_ok=True)
    Path(TRANSFORMED_DATASET_DIR + 'images/train/').mkdir(parents=True, exist_ok=True)
    Path(TRANSFORMED_DATASET_DIR + 'images/val/').mkdir(parents=True, exist_ok=True)


def convert_save_images(patient_id_series, src_dir, dest_dir, label: str):  # convert .dcm to .jpg and save to dest_dir
    for patient_id in tqdm(patient_id_series, desc=f'Converting {label} images', unit=' images'):
        src_path = src_dir + patient_id + '.dcm'
        dcm_data = pydicom.dcmread(src_path)
        image_array = dcm_data.pixel_array
        image = Image.fromarray(image_array)
        image.save(dest_dir + patient_id + '.jpg')

    print(f'Images moved to {label} folder:', len(os.listdir(dest_dir)))


def convert_save_labels(patient_id_series, LABELS_DIR, dest_dir):
    for patient_id in patient_id_series:
        if os.path.isfile(LABELS_DIR + patient_id + '.txt'):
            shutil.copy(LABELS_DIR + patient_id + '.txt', dest_dir)


def preprocess(dataset_path: str) -> str:
    dataset_path = Path(dataset_path)

    CSV_FILE = str(dataset_path / 'stage_2_train_labels.csv')
    TRAIN_SRC_DIR = str(dataset_path / 'stage_2_train_images/') + '/'

    make_transformed_dataset_dirs()

    annotations = dilute_annotations(pd.read_csv(CSV_FILE))

    patient_id_series = annotations.patientId.drop_duplicates()
    print('Dataset size after dilution (background):', patient_id_series.size)

    train_series, val_series = train_test_split(patient_id_series, test_size=0.1, random_state=42)
    print('Train set size:', len(train_series))
    print('Validation set size:', len(val_series))

    convert_save_images(train_series, TRAIN_SRC_DIR, TRANSFORMED_DATASET_DIR + 'images/train/', label='train')
    convert_save_images(val_series, TRAIN_SRC_DIR, TRANSFORMED_DATASET_DIR + 'images/val/', label='validation')

    LABELS_DIR = "./labels_temp/"
    os.mkdir(LABELS_DIR)

    for row in annotations.values:
        if pd.notna(row[1:5]).all():
            save_label(LABELS_DIR, row[0], row[1:5])

    print('Converting labels...')
    convert_save_labels(train_series, LABELS_DIR, TRANSFORMED_DATASET_DIR + 'labels/train/')
    convert_save_labels(val_series, LABELS_DIR, TRANSFORMED_DATASET_DIR + 'labels/val/')

    shutil.rmtree(LABELS_DIR)

    return TRANSFORMED_DATASET_DIR


if __name__ == "__main__":
    import sys

    preprocess(sys.argv[1])
