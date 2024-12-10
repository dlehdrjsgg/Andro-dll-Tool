import os
import platform
import subprocess
import shutil
from dotenv import load_dotenv

load_dotenv()

def run_il2cpp_dumper(lib_path, metadata_path, package_name):
    il2cpp_dumper_dll = os.getenv("IL2CPP_DUMPER_DLL_PATH")
    if not il2cpp_dumper_dll:
        print("Error: IL2CppDumper.dll path not found in .env file.")
        return
    system = platform.system()
    output_path = os.path.join("output", package_name)

    if system == "Darwin":
        try:
            il2cpp_dumper_dll = os.path.join(il2cpp_dumper_dll, "Il2CppDumper.dll")
            command = ["dotnet", il2cpp_dumper_dll, lib_path, metadata_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input="\n")  
            # if stderr:
            #     print(f"Error: {stderr.strip()}")
            dump_cs_file = os.path.join(os.path.dirname(il2cpp_dumper_dll), "dump.cs")
            destination_file = os.path.join(output_path, "dump.cs")
            if os.path.exists(dump_cs_file):
                shutil.copy(dump_cs_file, destination_file)
                print(f"dump.cs file copied to: {destination_file}\n")
            else:
                print(f"Error: dump.cs file not found at {dump_cs_file}\n")
        except Exception as e:
            print(f"Error running Il2CppDumper: {e}\n")

    elif system == "Windows":
        try:
            command = ["Il2CppDumper.exe", lib_path, metadata_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input="\n")  
            dump_cs_file = "dump.cs" # 실제 Windows에서 dump.cs 파일명으로 수정 필요
            destination_file = os.path.join(output_path, "dump.cs")
            
            if os.path.exists(dump_cs_file):
                shutil.copy(dump_cs_file, destination_file)
                print(f"dump.cs file copied to: {destination_file}\n")
            else:
                print(f"Error: dump.cs file not found at {dump_cs_file}\n")
        except Exception as e:
            print(f"Error running Il2CppDumper: {e}\n")
    
    else:
        print(f"[ERROR] Unsupported operating system: {system}. Only macOS and Windows are supported.\n")
