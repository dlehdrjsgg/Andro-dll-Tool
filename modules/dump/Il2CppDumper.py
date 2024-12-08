import os
import platform
import subprocess
import shutil
from dotenv import load_dotenv

load_dotenv()

def run_il2cpp_dumper(lib_path, metadata_path, package_name):
    il2cpp_dumper_dll = os.getenv("IL2CPP_DUMPER_DLL_PATH")
    if not il2cpp_dumper_dll:
        print("Error: IL2CPP_DUMPER_DLL_PATH is not set in the .env file.")
        return

    system = platform.system()
    output_path = os.path.join("output", package_name)

    if system == "Darwin":
        try:
            il2cpp_dumper_dll = os.path.join(il2cpp_dumper_dll, "Il2CppDumper.dll")
            command = ["dotnet", il2cpp_dumper_dll, lib_path, metadata_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input="\n")  # '\n'을 입력으로 제공하여 'Press any key to exit...' 메시지를 피함
            # if stderr:
            #     print(f"Error: {stderr.strip()}")
            dummy_dll_folder = os.path.join(os.path.dirname(il2cpp_dumper_dll), "DummyDll")
            destination_folder = os.path.join(output_path, "DummyDll")

            if os.path.exists(dummy_dll_folder):
                shutil.copytree(dummy_dll_folder, destination_folder)
                print(f"DummyDll folder copied to: {destination_folder}")
            else:
                print(f"Error: DummyDll folder not found at {dummy_dll_folder}")
        except Exception as e:
            print(f"Error running Il2CppDumper: {e}")

    elif system == "Windows":
        try:
            #il2cpp_dumper_dll = os.path.join(il2cpp_dumper_dll, "Il2CppDumper.dll")
            command = ["Il2CppDumper.exe", lib_path, metadata_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input="\n")  # '\n'을 입력으로 제공하여 'Press any key to exit...' 메시지를 피함
            dummy_dll_folder = "path/to/DummyDll"  # 실제 Windows에서 DummyDll 경로로 수정 필요
            destination_folder = os.path.join(output_path, "DummyDll")

            if os.path.exists(dummy_dll_folder):
                shutil.copytree(dummy_dll_folder, destination_folder)
                print(f"DummyDll folder copied to: {destination_folder}")
            else:
                print(f"Error: DummyDll folder not found at {dummy_dll_folder}")
        except Exception as e:
            print(f"Error running Il2CppDumper: {e}")
    
    else:
        print(f"Unsupported operating system: {system}. Only macOS and Windows are supported.")
