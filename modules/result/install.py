import subprocess
import os
import re

RED = "\033[91m"
RESET = "\033[0m"
GREEN = "\033[92m"
BLUE = "\033[94m"

def get_apk_metadata(apk_path):
    try:
        apktool_cmd = ['apktool', 'd', '-f', apk_path, '-o', 'apk_output']
        subprocess.run(apktool_cmd, check=True)

        with open('apk_output/AndroidManifest.xml', 'r') as file:
            manifest_content = file.read()

        package_name_match = re.search(r'package="([^"]+)"', manifest_content)
        package_name = package_name_match.group(1) if package_name_match else None

        main_activity_match = re.search(r'<activity[^>]+android:name="([^"]+)"[^>]*>', manifest_content)
        main_activity = main_activity_match.group(1) if main_activity_match else None

        subprocess.run(['rm', '-rf', 'apk_output'])

        return package_name, main_activity
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} extracting metadata from APK: {e}")
        return None, None

def install_and_run_apk(apk_path):
    try:
        print(f"{BLUE}[+]{RESET} Parsing metadata from APK file: {apk_path}")
        package_name, main_activity = get_apk_metadata(apk_path)
        print(f"{GREEN}[+]{RESET} Package Name: {package_name}")
        print(f"{GREEN}[+]{RESET} Main Activity: {main_activity}")

        if not package_name or not main_activity:
            print(f"{RED}[ERROR]{RESET} Could not extract metadata from APK: {apk_path}")
            return
        
        print(f"{BLUE}[+]{RESET} Checking for connected devices...")

        devices_cmd = ['adb', 'devices']
        result = subprocess.run(devices_cmd, capture_output=True, text=True)
        if 'device' not in result.stdout.splitlines()[1]:
            print(f"{RED}[ERROR]{RESET} No adb devices found. Please connect a device and try again.")
            return
        
        print(f"{BLUE}[+]{RESET} Installing APK: {apk_path}")
        
        install_cmd = ['adb', 'install', '-r', apk_path]
        subprocess.run(install_cmd, check=True)
        print(f"{GREEN}[+]{RESET} APK successfully installed on the emulator.")

        run_cmd = ['adb', 'shell', 'am', 'start', '-n', f'{package_name}/{main_activity}']
        subprocess.run(run_cmd, check=True)
        print(f"{GREEN}[+]{RESET} APK successfully launched: {package_name}/{main_activity}")

    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR]{RESET} Error installing or running APK: {e}")