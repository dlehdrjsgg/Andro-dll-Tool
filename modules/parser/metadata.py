import os
import zipfile

def extract_apk_metadata(apk_path, package_name):
    try:
        if not zipfile.is_zipfile(apk_path):
            print(f"{apk_path} is not a valid APK file.")
            return None

        with zipfile.ZipFile(apk_path, 'r') as apk:
            metadata_path = "assets/bin/Data/Managed/Metadata/global-metadata.dat"

            extracted_files = {}

            if metadata_path in apk.namelist():
                metadata_output_path = f"output/{package_name}/global-metadata.dat"
                os.makedirs(os.path.dirname(metadata_output_path), exist_ok=True)
                with open(metadata_output_path, 'wb') as f:
                    f.write(apk.read(metadata_path))
                extracted_files["metadata"] = metadata_output_path
                print(f"Extracted metadata to: {metadata_output_path}")
            else:
                print(f"Metadata file {metadata_path} not found in {apk_path}.")

            return extracted_files
    except Exception as e:
        print(f"Error extracting APK data: {e}")
        return None