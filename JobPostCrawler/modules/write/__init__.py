import importlib


def get(site):
    moduleName = importlib.import_module(f"modules.write.{site}", "write")
    main = getattr(moduleName, "main")

    return main