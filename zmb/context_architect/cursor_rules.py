import os

def detect_project_type(root_dir):
    """
    Detects the project type based on files present in the root directory.
    Returns a list of detected types (e.g., ['python', 'django']).
    """
    types = []
    files = os.listdir(root_dir)
    
    if 'requirements.txt' in files or 'pyproject.toml' in files or 'setup.py' in files:
        types.append('python')
        
    if 'manage.py' in files:
        types.append('django')
        
    if 'package.json' in files:
        types.append('node')
        # Check for react, next, etc. inside package.json if we wanted to be more granular
        # For now, simple file existence checks
        
    if 'next.config.js' in files or 'next.config.ts' in files:
        types.append('nextjs')
        
    return types

def generate_cursor_rules_content(project_types):
    """
    Generates the content for .cursorrules based on detected project types.
    """
    rules = []
    
    # Base Rules
    rules.append("""# Cursor Rules

## General Behavior
- Be concise and efficient.
- Always think step-by-step.
- If you are unsure, ask clarifying questions.
- Prefer modern best practices.
""")

    if 'python' in project_types:
        rules.append("""
## Python
- Use Python 3.x features.
- Follow PEP 8 style guide.
- Use type hinting where helpful.
- Prefer `venv` for virtual environments.
""")

    if 'django' in project_types:
        rules.append("""
## Django
- Use class-based views (CBVs) where appropriate.
- Keep business logic in `services.py` or `models.py`, not views.
- Use Django ORM efficiently (select_related, prefetch_related).
""")

    if 'node' in project_types:
        rules.append("""
## Node/JavaScript
- Use ES6+ syntax.
- Prefer `const` and `let` over `var`.
- Use async/await for asynchronous operations.
""")

    if 'nextjs' in project_types:
        rules.append("""
## Next.js
- Use App Router if available.
- Optimize images using `next/image`.
- Use Server Components by default.
""")

    return "\n".join(rules)

def create_cursor_rules(root_dir):
    """
    Orchestrates the creation of the .cursorrules file.
    """
    project_types = detect_project_type(root_dir)
    content = generate_cursor_rules_content(project_types)
    
    output_path = os.path.join(root_dir, '.cursorrules')
    
    # Don't overwrite if it exists? Or maybe just append? 
    # For now, let's overwrite but warn if we were interactive. 
    # Since this is a CLI tool, we'll just write it.
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return output_path, project_types
