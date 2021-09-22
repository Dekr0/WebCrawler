import importlib


def get(site):
    module_name = importlib.import_module(f"modules.write.{site}", "write")
    main = getattr(module_name, "main")

    return main