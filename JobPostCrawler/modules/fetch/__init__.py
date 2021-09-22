import importlib


def get(site):

    moduleName = importlib.import_module(f"modules.fetch.{site}", "fetch")
    main = getattr(moduleName, "main")

    return main