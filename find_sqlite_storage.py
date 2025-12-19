import os
import pkgutil
import importlib
import agno

def find_class(package, class_name):
    path = package.__path__
    prefix = package.__name__ + "."

    for _, name, is_pkg in pkgutil.walk_packages(path, prefix):
        try:
            module = importlib.import_module(name)
            for attr in dir(module):
                if attr.endswith("Storage"):
                    print(f"Found {attr} in {name}")
print("Searching for *Storage...")
find_class(agno, "Storage")
