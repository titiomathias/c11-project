import kagglehub
import shutil
import os

def download_dataset():
    path = kagglehub.dataset_download("atharvasoundankar/global-cybersecurity-threats-2015-2024")

    project_root = os.getcwd()
    dataset_dir = os.path.join(project_root, "dataset")
    os.makedirs(dataset_dir, exist_ok=True)

    for filename in os.listdir(path):
        src = os.path.join(path, filename)
        dst = os.path.join(dataset_dir, filename)

        if os.path.isfile(src):
            shutil.copy2(src, dst)

    return dataset_dir
