import os

def read_file(path):
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def modify_line(path, line_num, new_content):
    """Replaces a specific line in a file (1-indexed)."""
    with open(path, 'r') as f:
        lines = f.readlines()
    
    if 0 < line_num <= len(lines):
        lines[line_num - 1] = new_content + '\n'
        
        with open(path, 'w') as f:
            f.writelines(lines)
        return True
    return False
