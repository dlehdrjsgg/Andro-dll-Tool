def modify_binary(file_path, offset, hex_string):
    try:
        if isinstance(offset, str):
            offset = int(offset, 16)
        modified = bytes.fromhex(hex_string)
        
        with open(file_path, 'r+b') as binary:
            binary.seek(offset)
            binary.write(modified)
            print(f"Successfully modified offset {hex(offset)} in {file_path}\n")
            
    except FileNotFoundError:
        print(f"File not found: {file_path}\n")
    except ValueError as e:
        if "invalid literal" in str(e):
            print(f"Invalid offset value. Please provide a valid hex or decimal number.\n")
        else:
            print("Invalid hex string. Please provide a valid space-separated hex string.\n")
    except Exception as e:
        print(f"An error occurred: {e}\n")
