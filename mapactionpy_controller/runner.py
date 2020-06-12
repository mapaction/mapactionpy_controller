import mapactionpy_controller.steps as steps
import os
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.event import Event

# abstract class
# Done using the "old-school" method described here, without using the abs module
# https://stackoverflow.com/a/25300153


class BaseRunnerPlugin(object):
    def __init__(self, **kwargs):
        if self.__class__ is BaseRunnerPlugin:
            raise NotImplementedError(
                'BaseRunnerPlugin is an abstract class and cannot be instantiated directly')

    def get_projectfile_extension(self, **kwargs):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `get_projectfile_extension`'
            ' method cannot be called directly')

    def get_lyr_render_extension(self, **kwargs):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `get_lyr_render_extension`'
            ' method cannot be called directly')

    def get_templates(self, **kwargs):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `get_templates`'
            ' method cannot be called directly')

    def export_maps(self, **kwargs):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `export_maps`'
            ' method cannot be called directly')

    def build_project_files(self, **kwargs):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `build_project_files`'
            ' method cannot be called directly')

    def create_ouput_map_project(self, **kwargs):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `create_ouput_map_project`'
            ' method cannot be called directly')


class DummyRunner(BaseRunnerPlugin):
    def __init__(self, **kwargs):
        pass

    def get_templates(self, **kwargs):
        if 'recipe' in kwargs:
            print(kwargs['recipe'])
            return kwargs['recipe']

    def export_maps(self, **kwargs):
        if 'recipe' in kwargs:
            print(kwargs['recipe'])
            return kwargs['recipe']

    def build_project_files(self, **kwargs):
        if 'recipe' in kwargs:
            print(kwargs['recipe'])
            return kwargs['recipe']

    def get_projectfile_extension(self):
        return '.dummy'

    def create_ouput_map_project(self, **kwargs):
        return kwargs['recipe']


def get_plugin(hum_event, product_name):
    try:
        from mapactionpy_arcmap.arcmap_runner import ArcMapRunner
        runner = ArcMapRunner('mytemplate', myevent, product_name)
    except ImportError:
        from mapactionpy_qgis.qgis_runner import QGisRunner
        runner = QGisRunner()

    return runner
    # return DummyRunner()


def get_steps_delegated_to_plugin(my_runner):
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
            'Failed to add the layers to the map and applying styling',
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
    # print_kwargs(product_name="Country Overview with Admin 1 Boundaries and Topography", recipe='hello')

    product_name = "Country Overview with Admin 1 Boundaries and Topography"
    this_dir = os.path.dirname(os.path.realpath(__file__))
    # myevent = Event(os.path.join(this_dir, 'example', 'event_description.json'))
    # myevent = Event(r"D:\code\github\default-crash-move-folder\20YYiso3nn\event_description.json")
    myevent = Event(r"D:\MapAction\hotel\20200601-kenya-oxfam\event_description.json")
    cmf = CrashMoveFolder(myevent.cmf_descriptor_path)
    my_runner = get_plugin(myevent, product_name)
    lyrs = LayerProperties(cmf, my_runner.get_lyr_render_extension(), verify_on_creation=False)
    cookbook = MapCookbook(cmf, lyrs, verify_on_creation=False)
    recipe = cookbook.products[product_name]
    print('initial recipe', recipe)
    my_steps = get_steps_delegated_to_plugin(my_runner)
    end_result = steps.process_steps(my_steps, recipe)
    print('end_result', end_result)
