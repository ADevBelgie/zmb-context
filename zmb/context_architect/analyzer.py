import os
import ast
import re

class DependencyAnalyzer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.file_map = self._build_file_map()

    def _build_file_map(self):
        """Builds a map of filename (without extension) to full path."""
        file_map = {}
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                # Store both full name and name without extension
                abs_path = os.path.join(root, file)
                name_no_ext = os.path.splitext(file)[0]
                file_map[file] = abs_path
                file_map[name_no_ext] = abs_path
        return file_map

    def get_dependencies(self, file_path):
        """Returns a list of file paths that the given file imports."""
        ext = os.path.splitext(file_path)[1]
        if ext == '.py':
            return self._analyze_python(file_path)
        elif ext in ['.js', '.jsx', '.ts', '.tsx']:
            return self._analyze_js(file_path)
        return []

    def _analyze_python(self, file_path):
        dependencies = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self._resolve_import(alias.name, dependencies)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self._resolve_import(node.module, dependencies)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return list(dependencies)

    def _analyze_js(self, file_path):
        dependencies = set()
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Regex for ES6 imports: import ... from '...'
            # and CommonJS: require('...')
            # Very basic regex, can be improved
            
            # Match: from '...' or from "..."
            matches = re.findall(r'from\s+[\'"](.+?)[\'"]', content)
            matches.extend(re.findall(r'require\s*\(\s*[\'"](.+?)[\'"]\s*\)', content))
            
            for match in matches:
                # Handle relative imports
                if match.startswith('.'):
                    # Resolve relative path
                    dir_path = os.path.dirname(file_path)
                    resolved_path = os.path.normpath(os.path.join(dir_path, match))
                    # Try to find this file with extensions
                    self._resolve_path_with_extensions(resolved_path, dependencies)
                else:
                    # Non-relative import (package or absolute), skip for now unless it matches a file in project
                    pass

        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            
        return list(dependencies)

    def _resolve_import(self, module_name, dependencies):
        """Resolves a Python module name to a file path."""
        # Split module by dots to find file
        # e.g. zmb.context_architect.scanner -> zmb/context_architect/scanner.py
        
        parts = module_name.split('.')
        
        # Try to match the last part to a filename
        # This is heuristic and imperfect but good for MVP
        
        # 1. Check if the full module path corresponds to a file
        potential_path = os.path.join(self.root_dir, *parts) + '.py'
        if os.path.exists(potential_path):
            dependencies.add(os.path.normpath(os.path.abspath(potential_path)))
            return

        # 2. Check if it's a package (dir with __init__.py)
        potential_pkg = os.path.join(self.root_dir, *parts, '__init__.py')
        if os.path.exists(potential_pkg):
            dependencies.add(os.path.normpath(os.path.abspath(potential_pkg)))
            return
            
        # 3. Search in file map by the last component
        last_part = parts[-1]
        if last_part in self.file_map:
             # Verify it's somewhat related (e.g. path contains some of the module parts)
             # For now, just add it if it's unique enough
             dependencies.add(os.path.normpath(os.path.abspath(self.file_map[last_part])))

    def _resolve_path_with_extensions(self, base_path, dependencies):
        extensions = ['.js', '.jsx', '.ts', '.tsx', '.json', '']
        for ext in extensions:
            path = base_path + ext
            if os.path.exists(path):
                dependencies.add(os.path.normpath(os.path.abspath(path)))
                return
