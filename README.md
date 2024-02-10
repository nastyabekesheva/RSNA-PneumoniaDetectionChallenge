# RSNA-PneumoniaDetectionChallenge

## Table of contents

- [Preprocessing](###Preprocessing)
- [Training](###Training)
- [How to run with Docker](###How-to-run-with-Docker)


-----

### Preprocessing

For better performance of any model we need to preprocess the data. So here is what we did: 

1. Creating dataset of images classified as 'pneumonia positive' and background images. Background images are images with no objects that are added to a dataset to reduce False Positives.
2. Splitting dataset into training and validation.
3. Converted images from *.dcm to *.jpg (model requirement).
4. Prepared labels with coordinates for a center of bbox (model requirement). 

-----

### Training

Training consisted of two stages:

1. Choosing the model:

We decided to explore versions of YOLO model, here is what we noted about the performance of different models:

\begin{table}[]
\begin{tabular}{|c|c|c|}
\hline
\textbf{Model} & \textbf{Minutes/epoche} & \textbf{Score} \\ \hline
yolov8n.pt     & 1                       & 0.11549        \\ \hline
yolov8n.yaml   & 1                       & 0.11745        \\ \hline
yolov8s.pt     & 1.5                     & 0.12608        \\ \hline
yolov8m.pt     & 3                       & 0.12076        \\ \hline
yolov8l.pt     & 6                       & 0.13297        \\ \hline
\end{tabular}
\end{table}

2. 

### How to run with Docker

First of all make sure that you have installed the latest version of Docker!
If you don't have Docker [click here to download](https://www.docker.com/products/docker-desktop/).

#### Step 1: Building the Docker Container

```
docker image build -t rsna:0.0.1 /path/to/this/dir
```

![Screenshot](images/dockerscreen1.jpeg)

#### Step 2: Verify the Image Build

```
docker images
```

![Screenshot](images/dockerscreen2.jpeg)

#### Step 3: Running the Docker Container

```
docker run rsna:0.0.1
```


