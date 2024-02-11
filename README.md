# RSNA-PneumoniaDetectionChallenge

## Table of contents

- [Preprocessing](#Preprocessing)
- [Training](#Training)
- [Running a model (Docker)](#Running-a-model-(Docker))
- [Running a model (locally)](#Running-a-model-(locally))

-----

### Preprocessing

1. Creating a dataset of images classified as 'pneumonia positive' and background images.
   Background images are images with no labelled pneumonia that are added to a dataset to reduce False Positives.
2. Splitting dataset into training and validation (90/10).
3. Converted images from *.dcm to *.jpg (as our model trains on *.jpg).
4. Switched from left-bottom corner to relative center coordinates (again, model requirement).

-----

### Training

#### Run train.py

```
python3 train.py path/to/dataset/
```

**Important note: your dir must contain stage_2_train_labels.csv and stage_2_train_images dirs!**

#### Training consisted of two stages:

1. Choosing the model:

We decided to explore versions of YOLO model, here is what we noted about the performance of different models:

|  **Model**   | **Minutes per epoch** | **Score** |
|:------------:|:---------------------:|:---------:|
|  yolov8n.pt  |           1           |  0.11549  |
| yolov8n.yaml |           1           |  0.11745  |
|  yolov8s.pt  |          1.5          |  0.12608  |
|  yolov8m.pt  |           3           |  0.12076  |
|  yolov8.pt   |           6           |  0.13297  |
| yolov8l.yaml |           6           |  0.12437  |

2. Training the model: Based on previous analysis we decided to train 'yolov8l.pt' model. Model is saved in
   `weights/best.pt`

-----

### Running a model (Docker)

#### Step 0: Make sure that you have the latest version of [Docker](https://www.docker.com/products/docker-desktop/) installed.

#### Step 1: Pull the Docker Container

```
docker pull varcodex/shibarinu_pneumonia_inference:final
```

#### Step 2: Running the Docker Container

In order for Docker to be able to access the dataset (which resides on your local machine),
you need to mount the directory containing the files to the Docker container. This is done using the `--mount` flag and
by providing Docker with `/your_home_dir`.

Your local directory should contain a directory called `dataset` with *.dcm files inside.

Everything else, including the `target=/mount_dir` **should remain the same**.

```
docker run --mount type=bind,source=/your_home_dir,target=/mount_dir varcodex/shibarinu_pneumonia_inference:final /mount_dir
```

#### Step 3: submissions.csv

The generated `submissions.csv` file will be saved in the local `/your_home_dir` directory you provided when starting
the container.

------

### Running a model (locally)

#### Step 0: Clone the repository

```
git clone https://github.com/nastyabekesheva/RSNA-PneumoniaDetectionChallenge.git
```

#### Step 1: Install requirements

```
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 2: Run inference.py

Before running the script, navigate to the directory you wish submissions.csv to be saved in.

If you leave the repository directory, remember you need to provide the full path to `inference.py`.

`your/path/to/dataset/` should point to the directory containing *.dcm images.


```
python inference.py your/path/to/dataset/
```

[//]: # (------)
[//]: # (### Visualizing)


