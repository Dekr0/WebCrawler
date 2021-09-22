import importlib


def get(site):
    moduleName = importlib.import_module(f"modules.extract.{site}", "extract")
    main = getattr(moduleName, "main")

    return main