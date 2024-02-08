# RSNA-PneumoniaDetectionChallenge

## Table of contents

- [How to run with Docker](###How-to-run-with-Docker)


-----

### How to run with Docker

First of all make sure that you have installed the latest version of Docker!
If you don't have Docker [click here to download](https://www.docker.com/products/docker-desktop/).

#### Step 1: Building the Docker Container

```
docker image build -t rsna:0.0.1 /path/to/this/dir
```

![Screenshot](readme/dockerscreen1.jpeg)

#### Step 2: Verify the Image Build

```
docker images
```

![Screenshot](readme/dockerscreen2.jpeg)

#### Step 3: Running the Docker Container

```
docker run rsna:0.0.1
```


