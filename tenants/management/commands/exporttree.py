import os
from pathlib import Path
from subprocess import check_output, CalledProcessError
from django.core.management.base import BaseCommand

IMPORTANT_EXTENSIONS = {'.py', '.html', '.js', '.css', '.json', '.txt', '.env', '.md', '.yml'}
INCLUDE_FILES = {
    'manage.py', 'requirements.txt', '.env', '.env.example',
    'docker-compose.yml', 'readme.md', 'exporttree.py'
}
EXCLUDE_FOLDERS = {'venv', '__pycache__', '.git','node_modules', 'migrations', 'staticfiles', 'media','chunks'}

ICONS = {
    '.py': '⚙️', '.html': '🖼️', '.css': '🎨', '.js': '📜',
    '.json': '🧾', '.env': '🌍', '.md': '📝', '.yml': '📦', 'default': '📄', 'dir': '📁'
}


def is_git_modified(project_root, rel_path):
    try:
        output = check_output(['git', 'status', '--porcelain'], cwd=project_root).decode()
        changed_files = [line[3:].strip() for line in output.splitlines()]
        return str(rel_path).replace("\\", "/") in [x.replace("\\", "/") for x in changed_files]
    except CalledProcessError:
        return False


def tree_to_markdown(base_path, current_path='', prefix=''):
    lines = []
    entries = sorted(Path(base_path, current_path).iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

    for entry in entries:
        rel_path = os.path.relpath(entry, base_path)
        if entry.name in EXCLUDE_FOLDERS:
            continue

        if entry.is_dir():
            lines.append(f"{prefix}📁 **{entry.name}**")
            lines += tree_to_markdown(base_path, rel_path, prefix + "  ")
        else:
            if entry.suffix in IMPORTANT_EXTENSIONS or entry.name.lower() in INCLUDE_FILES:
                icon = ICONS.get(entry.suffix, ICONS['default'])
                modified = '🟡' if is_git_modified(base_path, rel_path) else ''
                lines.append(f"{prefix}{icon} {entry.name} {modified}")
    return lines


class Command(BaseCommand):
    help = "Εξάγει δενδροειδή λίστα σημαντικών αρχείων Django σε Markdown"

    def add_arguments(self, parser):
        parser.add_argument('--output', type=str, default='django_tree.md', help='Αρχείο εξόδου')

    def handle(self, *args, **kwargs):
        base_path = Path('.').resolve()
        output_file = Path(kwargs['output']).resolve()

        self.stdout.write(f"🔍 Εξαγωγή από: {base_path}")
        lines = ["# 📁 Django Development Tree", ""]
        lines += tree_to_markdown(base_path)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        self.stdout.write(self.style.SUCCESS(f"✅ Αποθηκεύτηκε στο {output_file}"))
