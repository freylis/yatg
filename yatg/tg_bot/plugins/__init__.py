import functools
import importlib

from yatg.utils import logger
from yatg.settings import Settings
from yatg.tg_bot.plugins.yadisk import YandexDiskPlugin
from yatg.tg_bot.plugins.notes import NotesPlugin
from yatg.tg_bot.plugins import errors


def get_plugin(command):
    """
    Get environment form command
    or from database of current user

    Args:
        command (str): command raw text

    Returns:
        (yadisk.tg_bot.plugins.base.Plugin): plugin class
    """
    plugins = initialize_plugins()

    # try to load plugin from user data

    current_plugin = None
    for plugin in plugins.values():
        if plugin.is_activate_plugin_command(command):
            current_plugin = plugin
            break

    if current_plugin:
        return current_plugin

    raise errors.PluginImportError(f'Can not find plugin for command {command!r}')


@functools.lru_cache()
def initialize_plugins():
    """
    Load all enabled plugins
    """
    plugins = {}
    settings = Settings()
    for plugin_path in settings.tgbot_plugins:
        try:
            plugin_object = import_plugin(plugin_path)
        except ImportError:
            logger.error(f'Can not import plugin {plugin_path!r}')
            continue

        plugins[plugin_object.NAME] = plugin_object

    return plugins


def import_plugin(path):
    """
    Path from root to custom PluginClass
    """
    parts = path.split('.')
    module_path = parts[:-1]
    module = importlib.import_module('.'.join(module_path))
    if not module:
        raise ImportError(f'Cat not import module {module_path!r}')
    cls = getattr(module, parts[-1])
    if not cls:
        raise ImportError(f'Cat not import class {parts[-1]!r} from {module_path!r}')
    return cls
