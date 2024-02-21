import os
import zipfile
import sys
from pathlib import Path


def download_competition_dataset(destination='./'):
    """Download and extract the RSNA Pneumonia Detection Challenge dataset from Kaggle."""
    if not os.path.exists(destination):
        os.mkdir(destination)
    os.chdir(destination)

    if os.path.exists(Path(destination) / 'dataset/'):
        print(f'Dataset already exists in {(Path(destination) / "dataset/").absolute()}')
        return False

    if not os.path.exists('./rsna-pneumonia-detection-challenge.zip'):
        os.system('pip install kaggle')
        exit_code = os.system('kaggle competitions download -c rsna-pneumonia-detection-challenge')
        if exit_code != 0:
            print(
                'Failed to download dataset. Check if you have kaggle.json as described in https://www.kaggle.com/docs/api')
            return False
        else:
            print('Dataset downloaded')
            return True
    else:
        print('Dataset already downloaded')
        return False


def extract_competition_dataset(source='./', destination='./'):
    with zipfile.ZipFile(Path(source) / 'rsna-pneumonia-detection-challenge.zip', 'r') as zip_ref:
        zip_ref.extractall(Path(destination) / 'dataset/')


def remove_archive(destination='./'):
    try:
        os.remove(Path(destination) / 'rsna-pneumonia-detection-challenge.zip')
        print('Archive removed')
        return True
    except FileNotFoundError:
        print('Archive not found (shouldn\'t happen)')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False


def main(destination: str = './'):
    if download_competition_dataset(destination):
        extract_competition_dataset(destination=destination)
        remove_archive()


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        destination = args[1]
        main(destination)
    else:
        main()
