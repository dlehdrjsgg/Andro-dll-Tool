import subprocess
import os

RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RESET = '\033[0m'

def sign_apk(apk_path, keystore_path, keystore_password, key_alias, key_password, output_path):
    try:

        keystore_path = os.path.expanduser(keystore_path)

        # aligned_apk_path = apk_path.replace('.apk', '-aligned.apk')
        # zipalign_cmd = [
        #     'zipalign', '-v', '-p', '4', apk_path, aligned_apk_path
        # ]
        # subprocess.run(zipalign_cmd, check=True)
        # print(f"{BLUE}[+]{RESET} APK successfully aligned: {aligned_apk_path}")

        cmd = [
            'jarsigner', '-verbose', '-sigalg', 'SHA256withRSA', '-digestalg', 'SHA-256',
            '-keystore', keystore_path,
            '-storepass', keystore_password,
            '-keypass', key_password,
            '-signedjar', output_path,
            apk_path, key_alias
        ]

        subprocess.run(cmd, check=True)
        print(f"{GREEN}[+]{RESET} APK successfully signed: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"{RED}[ERROR]{RESET} Error signing APK: {e}")

# sign_apk('unsigned.apk', '~/.android/debug.keystore', 'android', 'androiddebugkey', 'android', 'signed.apk')