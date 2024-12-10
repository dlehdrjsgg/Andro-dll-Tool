from modules.parser.binary import extract_apk_binary
from modules.parser.csharp import extract_methods_name, search_methods_by_name, get_offset_by_method_name
from modules.parser.metadata import extract_apk_metadata
from modules.dump.Il2CppDumper import run_il2cpp_dumper
from modules.analyze.modify import modify_binary
from modules.result.apk import replace_libil2cpp
import os

BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'


def search_and_select_method(dump_content):
    results = []
    while True:
        print("\n1. Search method")
        print("2. Select method")
        choice = input("Choose an option (1-2): ")

        if choice == "2":
            method_number = input("Enter the method number to select (or 'q' to exit): ")
            if method_number.lower() == 'q':
                break
            try:
                method_idx = int(method_number) - 1
                if 0 <= method_idx < len(results):
                    selected_method = results[method_idx]
                    print(f"\nSelected method: {selected_method}")
                    offset = get_offset_by_method_name(dump_content, selected_method)
                    if offset:
                        print(f"Offset: 0x{offset}")
                    user_confirm = input("Is this the method you want? (y/n): ")
                    if user_confirm.lower() == 'y':
                        return selected_method.name, offset, selected_method.classname
                else:
                    print("Invalid method number. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "1":
            user_method_name = input("Enter the method name to search (or 'q' to exit): ")
            if user_method_name.lower() == 'q':
                break

            results = search_methods_by_name(user_method_name)
            if results:
                print("\nFound methods:")
                print("---------------")
                for idx, method in enumerate(results, 1):
                    print(f"{idx}. {method}")  # Will print as "ClassName.MethodName"
                print("---------------")
            else:
                print("\nNo methods found matching your search.")
        else:
            print("Invalid option. Please try again.")

def print_ascii_art():
    print("""
██████╗ ██╗     ██╗                   ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔══██╗██║     ██║                   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██║  ██║██║     ██║         █████╗       ██║   ██║   ██║██║   ██║██║     ███████╗
██║  ██║██║     ██║         ╚════╝       ██║   ██║   ██║██║   ██║██║     ╚════██║
██████╔╝███████╗███████╗                 ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═════╝ ╚══════╝╚══════╝                 ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                                                                                                                                                                    
            """)

def run(package_name):
    try:
        print_ascii_art()
        print(f"{BLUE}[+]{RESET} checking apk file...")
        print(f"{BLUE}[+]{RESET} Processing '{package_name}'...\n")

        print(f"{BLUE}[+]{RESET} Parsing metadata...")
        metadata = extract_apk_metadata('./input/' + package_name, package_name)
        if metadata:
            print(f"Metadata parsed and saved successfully.\n")
        else:
            print(f"{RED}[ERROR]{RESET} No metadata found or error in parsing.\n")

        print(f"{BLUE}[+]{RESET} Parsing binary...")
        binary = extract_apk_binary('./input/' + package_name, package_name)
        if binary:
            print(f"Binary parsed and saved successfully.\n")
        else:
            print(f"{RED}[ERROR]{RESET} No binary found or error in parsing.\n")

        print(f"{BLUE}[+]{RESET} Dumping data...")
        run_il2cpp_dumper(f"output/{package_name}/libil2cpp.so", f"output/{package_name}/global-metadata.dat",
                          package_name)

        print(f"{BLUE}[+]{RESET} Done. Starting method search...\n")

        with open(f"output/{package_name}/dump.cs", "r") as f:
            dump_content = f.read()
            extract_methods_name(dump_content)

        while True:
            selected_method, offset, classname = search_and_select_method(dump_content)
            if not selected_method:  # If user quit from search_and_select_method
                break
            os.system('clear')
            print_ascii_art()
            print(f"\n{RED}Final selection:{RESET}")
            print("--------------------")
            print(f"Method: {RED}{selected_method}{RESET}")
            print(f"Class: {RED}{classname}{RESET}")
            print(f"Offset: {RED}0x{offset}{RESET}")
            print("--------------------")

            print(f"{BLUE}[+]{RESET} modifying binary...\n")
            hex_string = input("Enter the new value (space-separated hex, e.g., '01 00 A0 E3 1E FF 2F E1'): ").strip()
            modify_binary(f"output/{package_name}/libil2cpp.so", offset, hex_string)

            continue_choice = input("\nDo you want to modify another method? (y/n): ")
            if continue_choice.lower() != 'y':
                break

        print(f"{BLUE}[+]{RESET} Replacing libil2cpp.so in APK...")
        replace_libil2cpp(package_name)
        print(f"{BLUE}[+]{RESET} Done.")

    except Exception as e:
        print(f"{RED}[ERROR]{RESET} Error processing {package_name}: {str(e)}")

def multiRun(package_list):
    for package_name in package_list:
        run(package_name)
