import os
import zipfile

def extract_apk_binary(apk_path, package_name):
    try:
        if not zipfile.is_zipfile(apk_path):
            print(f"{apk_path} is not a valid APK file.")
            return None

        with zipfile.ZipFile(apk_path, 'r') as apk:
            lib_path = "lib/armeabi-v7a/libil2cpp.so"

            extracted_files = {}

            if lib_path in apk.namelist():
                binary_output_path = f"output/{package_name}/libil2cpp.so"
                os.makedirs(os.path.dirname(binary_output_path), exist_ok=True)
                with open(binary_output_path, 'wb') as f:
                    f.write(apk.read(lib_path))
                extracted_files["binary"] = binary_output_path
                print(f"Extracted binary to: {binary_output_path}")
            else:
                print(f"Binary file {lib_path} not found in {apk_path}.")

            return extracted_files
    except Exception as e:
        print(f"Error extracting APK data: {e}")
        return None
