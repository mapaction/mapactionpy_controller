from mapactionpy_controller.plugin_base import BaseRunnerPlugin


class DummyRunner(BaseRunnerPlugin):
    def __init__(self, **kwargs):
        pass

    def get_templates(self, **kwargs):
        return kwargs['state']

    def export_maps(self, **kwargs):
        return kwargs['state']

    def build_project_files(self, **kwargs):
        return kwargs['state']

    def get_projectfile_extension(self):
        return '.dummy'

    def create_ouput_map_project(self, **kwargs):
        return kwargs['state']
