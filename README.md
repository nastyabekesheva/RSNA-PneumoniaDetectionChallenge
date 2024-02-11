# RSNA-PneumoniaDetectionChallenge x team shiba rinu

## Table of contents
- [Problem description](#Problem-description)
- [Summary](#Summary)
- [Project structure](#Project-structure)
- [Requirements](#Requirements)
- [Running a model (Docker)](#Running-a-model)
- [Running a model (locally)](#Running-a-model-(locally))
- [Preprocessing](#Preprocessing)
- [Training](#Training)

-----

## Problem description

RSNA Pneumonia Detection Challenge is a problem of object detection with one class: the task is to predict coordinates of bounding boxes for all pneumonia areas on x-ray images. The training dataset contains ~6k images with pneumonia with total of ~10k instanses, and ~20k images without pneumonia (backgrounds). The test dataset contains 3k images. All the images are 1024x1024 px and in `dcm` format. CSV file with labels is provided containing information about both positive and negative examples, where each line represents patient ID and coordinates of one bounding box. The challenge provides and accepts coordinates in format `[top-left-x, top-left-y, width, height]` in pixels.

## Summary

The solution proposed, implements transfer learning with YOLOv8l model (large distribution), which was originally pretrained on COCO dataset. This model features advance technics of augmentation and optimization providing high level of abstarction on them. Solution includes dataset preparation, model finetuning, inference and visualization. In process of development thorough hyperparameter tuning was performed including augmentation, training and inference parameters.

The special feature of our solution is post-inference processing which allows to collapse overlapping boxes thus mitigating the habit of the model to predict 2 boxes one inside the other for one particular pneumonia unit. It is tuned to a certain IoU threshold and if the threshold is exceeded, all the participant boxes are averaged into one boxes. This approach prooved to be more effective that inference parameter tuning and it actually works great with default YOLOv8 parameters. Although, the `conf` inference parameter is adjusted anyway, to provide for the best result on a test set.

![Collapsed boxes](assets/overlap.png?raw=true)

In the end the whole pipeline gives following results on a kaggle test set: `private score: 0.13777`, `public score: 0.05802`.

## Project structure

- [`submission.csv`](submission.csv) - Model predictions for test dataset.
- [`inference.py`](inference.py) - Model inference. Run to generate submission.csv.
- [`weights`](outputs) - Folder containing trained model weights.
- [`train.py`](training.py) - Preprocessing and model training.
- [`utils`](utils) - Folder with utility scripts used in training and inference.
- `yolo8l.pt`, `config.yaml` - Pretrained model and configuration, essensial for training.
- [`Dockerfile`](Dockerfile) - Docker configuration file.

## Requirements

*In order to run the project you will need Python >= 3.10*

## Running a model (Docker)

#### Step 0: Make sure that you have the latest version of [Docker](https://www.docker.com/products/docker-desktop/) installed.

#### Step 1: Pull the Docker Container

```
docker pull varcodex/shibarinu_pneumonia_inference:final
```

#### Step 2: Running the Docker Container

In order for Docker to be able to access the dataset (which resides on your local machine),
you need to mount the directory containing the files to the Docker container. This is done using the `--mount` flag and
by providing Docker with `/your_home_dir`.

`/your_home_dir` should contain a directory called `dataset` with *.dcm files inside it.

Everything else, including the `target=/mount_dir` **should remain the same**.

```
docker run --mount type=bind,source=/your_home_dir,target=/mount_dir varcodex/shibarinu_pneumonia_inference:final
```

#### Step 3: submissions.csv

The generated `submissions.csv` file will be saved in the local `/your_home_dir` directory you provided when starting
the container.


## Running a model (locally)

#### Step 0: Clone the repository

```
git clone https://github.com/nastyabekesheva/RSNA-PneumoniaDetectionChallenge.git
```

#### Step 1: Install requirements

```
cd RSNA-PneumoniaDetectionChallenge
python -m venv .env
.env/Scripts/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 2: Run inference.py

Before running the script, navigate to the directory you wish submissions.csv to be saved in.

If you leave the repository directory, remember you need to provide the full path to `inference.py`.

`your/path/to/dataset/folder_with_dcm` should point to the directory containing *.dcm images.


```
python inference.py your/path/to/dataset/folder_with_dcm
```

-----

## Preprocessing

1. Creating a dataset of images classified as 'pneumonia positive' and background images.
   Background images are images with no labelled pneumonia that are added to a dataset to reduce False Positives.
2. Splitting dataset into training and validation (90/10).
3. Converted images from *.dcm to *.jpg (as our model trains on *.jpg).
4. Switched from left-bottom corner to relative center coordinates (again, model requirement).



## Training

#### Run train.py

```
python train.py path/to/dataset/
```

note: `path/to/dataset/` must contain `stage_2_train_labels.csv` and `stage_2_train_images/`

If you manage to successfully run train.py (it takes like 6+ hours), the model `best.pt` should be available in the directory you ran the previous command from

#### Why this specific model?

1. Choosing the model:

We decided to explore versions of YOLO model, and here is what we noted about the performance of its different models:

|  **Model**   | **Minutes per epoch** | **Score** |
|:------------:|:---------------------:|:---------:|
|  yolov8n.pt  |          ~1           |  0.11549  |
| yolov8n.yaml |          ~1           |  0.11745  |
|  yolov8s.pt  |         ~1.5          |  0.12608  |
|  yolov8m.pt  |          ~3           |  0.12076  |
|  yolov8l.pt  |          ~6           |  0.13297  |
| yolov8l.yaml |          ~6           |  0.12437  |

2. Decided to finally train 'yolov8l.pt' model. The trained model is saved at
   `weights/best.pt`

