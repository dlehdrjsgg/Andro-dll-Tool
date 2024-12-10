RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'

def modify_binary(file_path, offset, hex_string):
    try:
        if isinstance(offset, str):
            offset = int(offset, 16)
        modified = bytes.fromhex(hex_string)
        
        with open(file_path, 'r+b') as binary:
            binary.seek(offset)
            binary.write(modified)
            print(f"{GREEN}Successfully modified offset {hex(offset)} in {file_path}{RESET}\n")
            
    except FileNotFoundError:
        print(f"{RED}[ERROR]{RESET} File not found: {file_path}\n")
    except ValueError as e:
        if "invalid literal" in str(e):
            print(f"{RED}[ERROR]{RESET} Invalid offset value. Please provide a valid hex or decimal number.\n")
        else:
            print(f"{RED}[ERROR]{RESET} Invalid hex string. Please provide a valid space-separated hex string.\n")
    except Exception as e:
        print(f"{RED}[ERROR]{RESET} An error occurred: {e}\n")
