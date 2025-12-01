import os
import pathspec

def get_project_files(root_dir):
    """
    Scans the project directory and returns a list of files,
    respecting .gitignore if present.
    """
    files_to_include = []
    gitignore_path = os.path.join(root_dir, '.gitignore')
    
    spec = None
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            spec = pathspec.PathSpec.from_lines('gitwildmatch', f)

    # Always ignore .git directory and venv
    default_ignore = pathspec.PathSpec.from_lines('gitwildmatch', ['.git/', 'venv/', '__pycache__/', '*.pyc'])

    for root, dirs, files in os.walk(root_dir):
        # Filter directories in-place to prevent walking into ignored dirs
        dirs[:] = [d for d in dirs if not default_ignore.match_file(os.path.join(os.path.relpath(os.path.join(root, d), root_dir)) + '/')]
        
        if spec:
             dirs[:] = [d for d in dirs if not spec.match_file(os.path.join(os.path.relpath(os.path.join(root, d), root_dir)) + '/')]

        for file in files:
            abs_path = os.path.join(root, file)
            rel_path = os.path.relpath(abs_path, root_dir)
            
            if default_ignore.match_file(rel_path):
                continue

            if spec and spec.match_file(rel_path):
                continue
                
            files_to_include.append(abs_path)
            
    return sorted(files_to_include)

def generate_tree(root_dir, files):
    """Generates a string representation of the file tree."""
    # Simple list for MVP
    tree_lines = []
    for f in files:
        rel_path = os.path.relpath(f, root_dir)
        tree_lines.append(f"- {rel_path}")
    return "\n".join(tree_lines)
