from modules.parser.binary import extract_apk_binary
from modules.parser.metadata import extract_apk_metadata
from modules.dump.Il2CppDumper import run_il2cpp_dumper
import os

def run(package_name):
    try:
        print("""
██████╗ ██╗     ██╗                   ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔══██╗██║     ██║                   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║  ██║██║     ██║         █████╗       ██║   ██║   ██║██║   ██║██║     ███████╗
██║  ██║██║     ██║         ╚════╝       ██║   ██║   ██║██║   ██║██║     ╚════██║
██████╔╝███████╗███████╗                 ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═════╝ ╚══════╝╚══════╝                 ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                                                                                                                                                                    
        """)
        
        print("Checking APK files...")
        print(f"Processing '{package_name}'...\n")

        print("[+] Parsing metadata...")
        metadata = extract_apk_metadata('./input/' + package_name, package_name)
        if metadata:
            print("Metadata parsed and saved successfully.\n")
        else:
            print("No metadata found or error in parsing.\n")

        print("[+] Parsing binary...")
        binary = extract_apk_binary('./input/' + package_name, package_name)
        if binary:
            print("Binary parsed and saved successfully.\n")
        else:
            print("No binary found or error in parsing.\n")

        print("[+] Dumping data...")
        run_il2cpp_dumper(f"output/{package_name}/libil2cpp.so", f"output/{package_name}/global-metadata.dat", package_name)


    except:
        print(f"Error: {package_name}")
        pass


def multiRun(package_list):
    for package_name in package_list:
        run(package_name)
