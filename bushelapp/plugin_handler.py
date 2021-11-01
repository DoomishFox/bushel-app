import importlib
import inspect
from pathlib import Path
from .plugins.plugins import Plugin

def get_dirs(rootdir):
    dirs = []
    for path in Path(rootdir).iterdir():
        if path.is_dir() and path.stem != "__pycache__":
            dirs.append(path)
    return dirs

def get_py_files(rootdir):
    files = []
    for file in Path(rootdir).iterdir():
        if file.is_file() and file.name.endswith(".py"):
            files.append(file.name)
    return files

class PluginCollection(object):
    
    def __init__(self, plugin_collection) -> None:
        self.plugin_collection = plugin_collection
        self.name = plugin_collection.stem
        self.reload_plugins()
    
    def reload_plugins(self):
        self.plugins = []
        print(f"    Looking for plugins under collection '{self.plugin_collection}'")
        self.import_collection(self.plugin_collection)

    def import_collection(self, plugin_collection):
        plugin_list = get_py_files(plugin_collection)
        print(f"        Available plugins: {plugin_list}")
        for item in plugin_list:
            module_name = item[:-3]
            print(f"        Importing {item} (plugins.{self.name}.{module_name}):")
            plugin_module = importlib.import_module(f".{module_name}", f"bushelapp.plugins.{self.name}")
            clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
            for (_, c) in clsmembers:
                # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                if issubclass(c, Plugin) & (c is not Plugin):
                    print(f'            Found plugin class: {c.__module__}.{c.__name__}')
                    self.plugins.append(c())
    
    def apply_plugin(self, plugin_func, plugin_arg, text):
        plugin = next(filter(lambda plugin: plugin.func == plugin_func, self.plugins), None)
        if plugin is not None:
            print(f"Applying plugin {plugin.name}...")
            return plugin.parse(text)
        print(f"Plugin {plugin_func} not found!")
        return None

class PluginHandler(object):

    def __init__(self, collection_dir):
        self.plugin_folder = collection_dir
        self.reload_collections()
    
    def reload_collections(self):
        self.plugin_collections = []
        collections = get_dirs(f"bushelapp/{self.plugin_folder}")
        print(f"Loading plugin collections...")
        for collection in collections:
            self.plugin_collections.append(PluginCollection(collection))
    
    def get_collection(self, collection_name) -> PluginCollection:
        return next(filter(lambda collection: collection.name == collection_name, self.plugin_collections), None)
    

plugins = PluginHandler("plugins")