import os
from zmb.context_architect.scanner import generate_tree

def create_context_file(files, output_path, root_dir=None):
    """Reads files and writes them to a single markdown file."""
    if root_dir is None:
        root_dir = os.getcwd()

    with open(output_path, 'w', encoding='utf-8') as out_f:
        out_f.write("# Project Context\n\n")
        
        # Add File Tree
        out_f.write("## File Tree\n")
        out_f.write("```\n")
        out_f.write(generate_tree(root_dir, files))
        out_f.write("\n```\n\n")

        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as in_f:
                    content = in_f.read()
                    
                rel_path = os.path.relpath(file_path, root_dir)
                
                ext = os.path.splitext(file_path)[1].lstrip('.')
                if not ext:
                    ext = 'text'
                
                out_f.write(f"## File: {rel_path}\n")
                out_f.write(f"```{ext}\n")
                out_f.write(content)
                out_f.write("\n```\n\n")
                
            except Exception as e:
                print(f"Skipping binary or unreadable file: {file_path} ({e})")

    return True
