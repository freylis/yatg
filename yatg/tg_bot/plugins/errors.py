

class PluginError(Exception):
    pass


class PluginImportError(PluginError):
    pass


class PluginCommandError(PluginError):
    pass
