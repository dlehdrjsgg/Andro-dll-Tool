import os
import zipfile
import shutil

def replace_libil2cpp(package_name):
    input_apk_path = f'input/{package_name}.apk'
    output_dir = f'output/{package_name}'
    lib_path = os.path.join(output_dir, 'libil2cpp.so')
    new_apk_path = os.path.join(output_dir, f'{package_name}.apk')

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"{output_dir} directory does not exist.")

    shutil.copy(input_apk_path, new_apk_path)

    with zipfile.ZipFile(new_apk_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)

    libil2cpp_path = os.path.join(output_dir, 'lib', 'armeabi-v7a', 'libil2cpp.so')
    if os.path.exists(libil2cpp_path):
        os.remove(libil2cpp_path)
    shutil.copy(lib_path, libil2cpp_path)

    with zipfile.ZipFile(new_apk_path, 'w') as zip_ref:
        for foldername, subfolders, filenames in os.walk(output_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, output_dir)
                zip_ref.write(file_path, arcname)
