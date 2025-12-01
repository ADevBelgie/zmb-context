import argparse
import os
import sys
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

# Ensure zmb package is in path
sys.path.append(os.getcwd())

from zmb.context_architect.scanner import get_project_files
from zmb.context_architect.generator import create_context_file
from zmb.context_architect.cursor_rules import create_cursor_rules
from zmb.context_architect.analyzer import DependencyAnalyzer

console = Console()

def print_tree(root_dir, files):
    """Prints a rich tree of the files."""
    tree = Tree(f":open_file_folder: [bold blue]{os.path.basename(root_dir)}[/bold blue]")
    
    # Simple tree construction for MVP
    # A better implementation would nest directories properly
    # For now, we'll just list files to show it works
    
    # Group by directory to make it look nicer
    dirs = {}
    for f in files:
        rel_path = os.path.relpath(f, root_dir)
        parts = rel_path.split(os.sep)
        
        current_level = tree
        for i, part in enumerate(parts[:-1]):
            if part not in dirs:
                # This is a simplification; in a real recursion we'd track nodes
                # For flat list, let's just add to root or a flat structure
                pass
        
        # Just adding flat for now to match previous behavior but with icons
        tree.add(f":page_facing_up: {rel_path}")

    console.print(tree)

def interactive_mode():
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]ZMB Context Architect[/bold cyan]\n[dim]Select an action below[/dim]"))
        
        action = Prompt.ask("Choose an action", choices=["scan", "generate", "rules", "exit"], default="scan")
        
        if action == "scan":
            path = Prompt.ask("Path to scan", default=os.getcwd())
            run_scan(path)
            Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
        elif action == "generate":
            path = Prompt.ask("Path to scan", default=os.getcwd())
            
            # Suggest directories for focus
            try:
                dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
                if dirs:
                    console.print(f"[dim]Available directories: {', '.join(dirs)}[/dim]")
            except Exception:
                pass

            focus = Prompt.ask("Focus keyword (optional)", default="")
            smart = Confirm.ask("Enable Smart Focus (include dependencies)?", default=True)
            output = Prompt.ask("Output filename", default="context.md")
            run_generate(path, focus if focus else None, smart, output)
            Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
        elif action == "rules":
            path = Prompt.ask("Path to scan", default=os.getcwd())
            run_rules(path)
            Prompt.ask("\n[dim]Press Enter to continue...[/dim]")
        elif action == "exit":
            console.print("[yellow]Goodbye![/yellow]")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="ZMB Context Architect")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Scan Command
    scan_parser = subparsers.add_parser('scan', help='Scan project and show file tree')
    scan_parser.add_argument('--path', default=os.getcwd(), help='Root path to scan')

    # Generate Command
    gen_parser = subparsers.add_parser('generate', help='Generate context.md')
    gen_parser.add_argument('--path', default=os.getcwd(), help='Root path to scan')
    gen_parser.add_argument('--output', default='context.md', help='Output filename')
    gen_parser.add_argument('--focus', help='Filter by keyword (e.g., "auth")')
    gen_parser.add_argument('--smart', action='store_true', help='Include dependencies of focused files')

    # Rules Command
    rules_parser = subparsers.add_parser('rules', help='Generate .cursorrules')
    rules_parser.add_argument('--path', default=os.getcwd(), help='Root path to scan')

    # Interactive Command
    subparsers.add_parser('interactive', help='Start interactive mode')

    args = parser.parse_args()

    if args.command == 'scan':
        run_scan(args.path)

    elif args.command == 'generate':
        run_generate(args.path, args.focus, args.smart, args.output)

    elif args.command == 'rules':
        run_rules(args.path)

    elif args.command == 'interactive':
        interactive_mode()

    else:
        # If no arguments, enter interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
