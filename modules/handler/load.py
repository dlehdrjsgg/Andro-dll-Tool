import os

def listApkFiles(input_dir="./input"):
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")

    apk_files = [
        file for file in os.listdir(input_dir) 
        if file.endswith(".apk") and os.path.isfile(os.path.join(input_dir, file))
    ]
    if not apk_files:
        print(f"No '.apk' files found in the input directory: {input_dir}")

    return apk_files