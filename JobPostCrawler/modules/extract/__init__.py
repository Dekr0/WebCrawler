import importlib


def get(site):
    module_name = importlib.import_module(f"modules.extract.{site}", "extract")
    main = getattr(module_name, "main")

    return main