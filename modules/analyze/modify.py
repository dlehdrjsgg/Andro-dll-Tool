def modify_binary(file_path, offset, hex_string):
    try:
        # 바이트로 변환
        modified = bytes.fromhex(hex_string)
        
        with open(file_path, 'r+b') as binary:
            # 오프셋 이동
            binary.seek(offset)
            # 값을 수정 < (그대로)
            binary.write(modified)
            print(f"Successfully modified offset {hex(offset)} in {file_path}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except ValueError:
        print("Invalid hex string. Please provide a valid space-separated hex string.")
    except Exception as e:
        print(f"An error occurred: {e}")