import os
import zipfile
import shutil

RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"

def replace_libil2cpp(package_name):
    input_apk_path = f'input/{package_name}'
    output_dir = f'output/{package_name}'
    temp_dir = f'temp_{package_name}'
    lib_path = os.path.join(output_dir, 'libil2cpp.so')
    new_apk_path = os.path.join(output_dir, f'{package_name}')

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"{RED}[ERROR]{RESET} Directory not found: {output_dir}\n")
    shutil.copy(input_apk_path, new_apk_path)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with zipfile.ZipFile(new_apk_path, 'r') as zip_ref:
        print(f"{BLUE}[+]{RESET} Extracting APK: {new_apk_path}")
        zip_ref.extractall(temp_dir)
    libil2cpp_path = os.path.join(temp_dir, 'lib', 'armeabi-v7a', 'libil2cpp.so')
    if os.path.exists(libil2cpp_path):
        os.remove(libil2cpp_path)
    shutil.copy(lib_path, libil2cpp_path)
    
    with zipfile.ZipFile(new_apk_path, 'w') as zip_ref:
        print(f"{BLUE}[+]{RESET} Replacing libil2cpp.so in APK")
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, temp_dir)
                zip_ref.write(file_path, arcname)

    print(f"{GREEN}APK successfully created: {new_apk_path}{RESET}\n")

    shutil.rmtree(temp_dir)
