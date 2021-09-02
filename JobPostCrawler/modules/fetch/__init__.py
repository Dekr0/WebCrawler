import importlib


def get(site):

    module_name = importlib.import_module(f"modules.fetch.{site}", "fetch")
    main = getattr(module_name, "main")

    return main