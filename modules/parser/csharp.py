import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Method:
    name: str
    classname: str
    
    def __str__(self):
        return f"{self.classname}.{self.name}"

# Global variable to store methods
methods_store: List[Method] = []

def extract_methods_name(cs_code: str) -> List[Method]:
    global methods_store
    methods = []
    class_pattern = r'public class (\w+)\s*:'
    method_pattern = r'(?:public|private|protected)\s+(?:virtual\s+|override\s+|static\s+)?(?:[\w<>[\],\s]+\s+)?(\w+)\s*\([^)]*\)\s*{'
    
    # Split code into class blocks
    class_blocks = re.split(class_pattern, cs_code)
    
    for i in range(1, len(class_blocks), 2):
        classname = class_blocks[i]
        class_content = class_blocks[i + 1]
        
        # Find all methods in this class
        method_matches = re.finditer(method_pattern, class_content)
        for match in method_matches:
            method_name = match.group(1)
            if method_name != 'ctor':  # Exclude constructors
                methods.append(Method(method_name, classname))
    
    # Store methods in memory instead of file
    methods_store = methods
    return methods

def get_offset_by_method_name(cs_code: str, method: Method) -> Optional[str]:
    # Find method with any return type, not just void
    class_method_pattern = (
        rf'public class {method.classname}\s*:.*?'  # Class definition
        rf'// RVA: 0x([0-9A-F]+) Offset: 0x([0-9A-F]+) VA: 0x([0-9A-F]+)\n\s+'  # Method offset info
        rf'(?:public|private|protected)\s+(?:virtual\s+|override\s+|static\s+)?'  # Method modifiers
        rf'(?:[\w<>[\],\s]+\s+)?'  # Return type (optional)
        rf'{method.name}\s*\('  # Method name
    )
    
    match = re.search(class_method_pattern, cs_code, re.DOTALL)
    if not match:
        # Try alternative pattern without class context for better matching
        method_pattern = (
            rf'// RVA: 0x[0-9A-F]+ Offset: 0x([0-9A-F]+) VA: 0x[0-9A-F]+\n\s+'
            rf'(?:public|private|protected)\s+(?:virtual\s+|override\s+|static\s+)?'
            rf'(?:[\w<>[\],\s]+\s+)?{method.name}\s*\('
        )
        match = re.search(method_pattern, cs_code)
        return match.group(1) if match else None
        
    return match.group(2)

def search_methods_by_name(name: str) -> List[Method]:
    return [method for method in methods_store if name.lower() in method.name.lower()]