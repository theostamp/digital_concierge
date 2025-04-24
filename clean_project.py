import os
import shutil

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(PROJECT_ROOT):
    # Διαγραφή .pyc
    for file in files:
        if file.endswith('.pyc'):
            os.remove(os.path.join(root, file))
    # Διαγραφή φακέλων migrations (εκτός αν περιέχουν μόνο __init__.py)
    for dir_name in dirs:
        if dir_name == 'migrations':
            migrations_path = os.path.join(root, dir_name)
            files_in_migrations = os.listdir(migrations_path)
            if all(f == '__init__.py' or f.endswith('.pyc') for f in files_in_migrations):
                for f in files_in_migrations:
                    os.remove(os.path.join(migrations_path, f))
                print(f"Καθαρίστηκε ο φάκελος: {migrations_path}")
            elif files_in_migrations:
                # Διαγραφή όλων των αρχείων εκτός από __init__.py
                for f in files_in_migrations:
                    if f != '__init__.py':
                        os.remove(os.path.join(migrations_path, f))
                print(f"Διαγράφηκαν migration αρχεία από: {migrations_path}")