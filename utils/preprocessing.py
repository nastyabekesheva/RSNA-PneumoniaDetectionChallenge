import pandas as pd
import os
import opendatasets as od
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import pydicom
from PIL import Image
import shutil

'''try:
    shutil.rmtree('/kaggle/working/')
except:
    pass'''


# download dataset
dataset = 'https://www.kaggle.com/'
od.download(dataset)

IMG_SIZE = 1024

# paths
CSV_FILE = '../input/rsna-pneumonia-detection-challenge/stage_2_train_labels.csv'
TRAIN_SRC_DIR = '../input/rsna-pneumonia-detection-challenge/stage_2_train_images/'
TEST_SRC_DIR = '../input/rsna-pneumonia-detection-challenge/stage_2_test_images/'
DATASET_DIR = './dataset/'
TEST_IMG_DIR = 'test_images/'

os.mkdir(DATASET_DIR)
os.mkdir(DATASET_DIR + 'images/')
os.mkdir(DATASET_DIR + 'images/train/')
os.mkdir(DATASET_DIR + 'images/val/')
os.mkdir(DATASET_DIR + 'images/test/')
os.mkdir(DATASET_DIR + 'labels/')
os.mkdir(DATASET_DIR + 'labels/train/')
os.mkdir(DATASET_DIR + 'labels/val/')
os.mkdir(DATASET_DIR + 'labels/test/')
os.mkdir(TEST_IMG_DIR)

# read dataset
annotations = pd.read_csv(CSV_FILE)

# cleaning
positive_annotations = annotations[annotations.Target == 1]
negative_annotations = annotations[annotations.Target == 0]
negative_sample = negative_annotations.sample(600)
negative_sample['patientId'].shape[0]

annotations = pd.concat([positive_annotations, negative_sample])
patient_id_series = annotations.patientId.drop_duplicates()

# train test split
print('Number of images:', patient_id_series.size)
train_series, val_series = train_test_split(patient_id_series, test_size=0.1, random_state=42)
print('Train set number:', len(train_series))
print('Validation set number:', len(val_series))

# read images
for patient_id in tqdm(train_series):
    src_path = TRAIN_SRC_DIR + patient_id + '.dcm'
    dcm_data = pydicom.dcmread(src_path)
    image_array = dcm_data.pixel_array
    image = Image.fromarray(image_array)
    image.save(DATASET_DIR + 'images/train/' + patient_id + '.jpg')
print('Images moved to train folder:', len(os.listdir(DATASET_DIR + 'images/train/')))
    
for patient_id in tqdm(val_series):
    src_path = TRAIN_SRC_DIR + patient_id + '.dcm'
    dcm_data = pydicom.dcmread(src_path)
    image_array = dcm_data.pixel_array
    image = Image.fromarray(image_array)
    image.save(DATASET_DIR + 'images/val/' + patient_id + '.jpg')
print('Images moved to val folder:', len(os.listdir(DATASET_DIR + 'images/val/')))

# prepare coordinates for training
def translate_bbox(bbox):
    top_left_x = bbox[0]
    top_left_y = bbox[1]
    absolute_w = bbox[2]
    absolute_h = bbox[3]

    relative_w = absolute_w / IMG_SIZE
    relative_h = absolute_h / IMG_SIZE
    
    relative_x = top_left_x / IMG_SIZE + relative_w / 2
    relative_y = top_left_y / IMG_SIZE + relative_h / 2
    
    return relative_x, relative_y, relative_w, relative_h
    
def revert_bbox(rx, ry, rw, rh):
    x = (rx-rw/2)*IMG_SIZE
    y = (ry-rh/2)*IMG_SIZE
    w = rw*IMG_SIZE
    h = rh*IMG_SIZE
    
    return x, y, w, h
    
    
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

LABELS_DIR = "./labels_temp/"
os.mkdir(LABELS_DIR)

for row in annotations.values:
    if pd.notna(row[1:5]).all():
        save_label(LABELS_DIR, row[0], row[1:5])
    
for patient_id in train_series:
    if os.path.isfile(LABELS_DIR + patient_id + '.txt'):
        shutil.copy(LABELS_DIR + patient_id + '.txt', DATASET_DIR + 'labels/train/')
    
for patient_id in val_series:
    if os.path.isfile(LABELS_DIR + patient_id + '.txt'):
        shutil.copy(LABELS_DIR + patient_id + '.txt', DATASET_DIR + 'labels/val/')
    
shutil.rmtree(LABELS_DIR)