import mapactionpy_controller.steps as steps
import os
import re

# abstract class
# Done using the "old-school" method described here, without using the abs module
# https://stackoverflow.com/a/25300153


class BaseRunnerPlugin(object):
    def __init__(self, **kwargs):
        if self.__class__ is BasePluginRunner:
            raise NotImplementedError(
                'BasePluginRunner is an abstract class and cannot be instantiated directly')

    def get_projectfile_extension(self, **kwargs):
        raise NotImplementedError(
            'BasePluginRunner is an abstract class and the `get_projectfile_extension` method cannot be called directly')

    def get_templates(self, **kwargs):
        raise NotImplementedError(
            'BasePluginRunner is an abstract class and the `get_templates` method cannot be called directly')

    def export_maps(self, **kwargs):
        raise NotImplementedError(
            'BasePluginRunner is an abstract class and the `export_maps` method cannot be called directly')

    def build_project_files(self, **kwargs):
        raise NotImplementedError(
            'BasePluginRunner is an abstract class and the `build_project_files` method cannot be called directly')

    def create_ouput_map_project(self, **kwargs):
        raise NotImplementedError(
            'BasePluginRunner is an abstract class and the `create_ouput_map_project` method cannot be called directly')


class DummyRunner(BaseRunnerPlugin):
    def __init__(self, **kwargs):
        pass

    def get_templates(self, **kwargs):
        if 'recipe' in kwargs:
            print(kwargs['recipe'])
            return 'doghnuts'

    def export_maps(self, **kwargs):
        if 'recipe' in kwargs:
            print(kwargs['recipe'])
            return 'kwargs[stuff]'

    def build_project_files(self, **kwargs):
        if 'recipe' in kwargs:
            print(kwargs['recipe'])
            return 'sausages'


def get_plugin():
    try:
        from mapactionpy_arcmap.arcmap_runner import ArcMapRunner
        runner = ArcMapRunner()
    except ImportError:
        from mapactionpy_qgis.qgis_runner import QGisRunner
        runner = QGisRunner()

    # return runner
    return DummyRunner()


def get_steps_delegated_to_plugin():
    my_runner = get_plugin()

# Get Template

        # try:
        #     self.recipe = self.cookbook.products[productName]
        # except KeyError:
        #     raise Exception("Error: Could not find recipe for product: \"" + productName + "\" in " + self.cookbookFile)

# Get Oritenation
# 'cook()'
# - set zoom
# alignLegend
# Export
#  - Create export dir
#  - do_export jpeg, pdf, thumbnail
#  - export_atlas (if required)
#  - create zip file

    # steps.Step(
    #     my_runner.update_marginalia,
    #     'Updating the marginalia on the map',
    #     'SUccessfully updated the marginalia on the map',
    #     'Failed to update the marginalia on the map'
    # ),

    plugin_steps = [
        steps.Step(
            my_runner.get_templates,
            'Identifying suitable map template',
            'Successfully indentifed suitable map template',
            'Failed to identify suitable map template',
        ),
        steps.Step(
            my_runner.create_ouput_map_project,
            "Creating new '{}' file.".format(my_runner.get_projectfile_extension()),
            "Successfully created new '{}' file.".format(my_runner.get_projectfile_extension()),
            "Failed to create new '{}' file.".format(my_runner.get_projectfile_extension())
        ),
        steps.Step(
            my_runner.build_project_files,
            'Adding layers to the map and applying styling',
            'Successfully added layers to the map and applying styling',
            'Failed to uddede theyers to the map and applying styling',
        ),
        steps.Step(
            my_runner.export_maps,
            'Exporting Maps and creating zipfile',
            'Successfully exported Maps and creating zipfile',
            'Failed to export the maps and create zipfile'
        )
    ]

    return plugin_steps


if __name__ == "__main__":
    cmf = CrashMoveFolder(self.cmf_desc_path)
    lyrs = LayerProperties(cmf, '', verify_on_creation=False)
    cookbook = MapCookbook(cmf, lyrs, verify_on_creation=True)
    recipe = cookbook.products[productName]

    my_steps = get_steps_delegated_to_plugin()
    print(steps.process_steps(my_steps, recipe))

    # try:
    #     self.recipe = self.cookbook.products[productName]
    # except KeyError:
    #     raise Exception("Error: Could not find recipe for product: \"" + productName + "\" in " + self.cookbookFile)
