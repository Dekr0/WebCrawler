import importlib


def get(site):
    module_name = importlib.import_module(f"modules.write.{site}", "write")
    handle_func = getattr(module_name, "handle")

    return handle_func