import mapactionpy_controller.steps as steps
import logging
import os
import re
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.event import Event

# abstract class
# Done using the "old-school" method described here, without using the abs module
# https://stackoverflow.com/a/25300153


class BaseRunnerPlugin(object):
    def __init__(self, cmf_descriptor_path, ** kwargs):
        self.cmf = CrashMoveFolder(cmf_descriptor_path)

        if not self.cmf.verify_paths():
            raise ValueError("Cannot find paths and directories referenced by cmf {}".format(self.cmf.path))

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

    def _get_all_templates_by_regex(self, recipe):
        """
        Returns:
            - A list of all of the templates, stored in `cmf.map_templates` whose
              filename matches the regex `recipe.template` and that have the extention
              `self.get_projectfile_extension()`
        """
        def _is_relevant_file(f):
            extension = os.path.splitext(f)[1]
            logging.debug('checking file "{}", with extension "{}", against pattern "{}" and "{}"'.format(
                f, extension, recipe.template, self.get_projectfile_extension()
            ))
            if re.search(recipe.template, f):
                logging.debug('file {} matched regex'.format(f))
                f_path = os.path.join(self.cmf.map_templates, f)
                return (os.path.isfile(f_path)) and (extension == self.get_projectfile_extension())
            else:
                return False

        # TODO: This results in calling `os.path.join` twice for certain files
        logging.debug('searching for map templates in; {}'.format(self.cmf.map_templates))
        filenames = os.listdir(self.cmf.map_templates)
        logging.debug('all available template files:\n\t{}'.format('\n\t'.join(filenames)))
        filenames = filter(_is_relevant_file, filenames)
        logging.debug('possible template files:\n\t{}'.format('\n\t'.join(filenames)))
        return [os.path.join(self.cmf.map_templates, fi) for fi in filenames]

    def get_aspect_ratios_of_templates(self, possible_templates):
        raise NotImplementedError(
            'BaseRunnerPlugin is an abstract class and the `_get_aspect_ratios_of_templates`'
            ' method cannot be called directly')

    def get_templates(self, **kwargs):
        recipe = kwargs['state']
        # If there already already is a valid `recipe.map_project_path` just skip with method
        if recipe.map_project_path:
            if os.path.exists(recipe.map_project_path):
                return recipe
            else:
                raise ValueError('Unable to locate map project file: {}'.format(recipe.map_project_path))

        # use `recipe.template` as regex to locate one or more templates
        possible_templates = self._get_all_templates_by_regex(recipe)

        # Select the template with the most appropriate asspect ratio
        recipe.template_path = self.get_aspect_ratios_of_templates(possible_templates)
        # use logic to workout which template has best aspect ratio

        # TODO re-enable "Have the input files changed?"
        # Have the input shapefiles changed?
        return recipe

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


def get_plugin_step():
    def get_plugin(**kwargs):
        hum_event = kwargs['state']
        try:
            from mapactionpy_arcmap.arcmap_runner import ArcMapRunner
            runner = ArcMapRunner(hum_event)
        except ImportError:
            from mapactionpy_qgis.qgis_runner import QGisRunner
            runner = QGisRunner()

        return runner

    def new_event(**kwargs):
        return Event(kwargs['state'])

    plugin_step = [
        steps.Step(
            new_event,
            'Loading the Humanitarian Event description file',
            'Successfully loaded the Humanitarian Event description file',
            'Failed to load the Humanitarian Event description file',
        ),
        steps.Step(
            get_plugin,
            'Identifying available plugins (ArcMapRunner/QGisRunner)',
            'Successfully loaded an available plugin',
            'Failed to load a suitable any plugin',
        ),
    ]

    return plugin_step


def get_per_product_steps(_runner, map_num, map_name):
    # In due course there should be greater granularity for some of these steps

    def just_return_recipe(**kwargs):
        return kwargs['state']

    def pass_through_step(**kwargs):
        pass

    product_steps = [
        steps.Step(
            just_return_recipe,
            'Starting to create map "{}" - "{}"'.format(map_num, map_name),
            'Starting to create map "{}" - "{}"'.format(map_num, map_name),
            'Failed to create map "{}" - "{}"'.format(map_num, map_name),
        ),
        steps.Step(
            _runner.get_templates,
            'Identifying suitable map template',
            'Successfully indentifed suitable map template',
            'Failed to identify suitable map template',
        ),
        steps.Step(
            _runner.create_ouput_map_project,
            "Creating new '{}' file.".format(_runner.get_projectfile_extension()),
            "Successfully created new '{}' file.".format(_runner.get_projectfile_extension()),
            "Failed to create new '{}' file.".format(_runner.get_projectfile_extension())
        ),
        steps.Step(
            _runner.build_project_files,
            'Adding layers to the map and applying styling',
            'Successfully added layers to the map and applying styling',
            'Failed to add the layers to the map and applied styling',
        ),
        steps.Step(
            _runner.export_maps,
            'Exporting Maps and creating zipfile',
            'Successfully exported Maps and creating zipfile',
            'Failed to export the maps and create zipfile'
        ),
        steps.Step(
            pass_through_step,
            'Completed the creation of map "{}" - "{}"'.format(map_num, map_name),
            'Completed the creation of map "{}" - "{}"'.format(map_num, map_name),
            'Failed to create map "{}" - "{}"'.format(map_num, map_name),
        ),

    ]

    return product_steps


def get_cookbook_steps(my_runner):
    def get_cookbook():
        lyrs = LayerProperties(my_runner.cmf, my_runner.get_lyr_render_extension(), verify_on_creation=False)
        return MapCookbook(my_runner.cmf, lyrs, verify_on_creation=False)

    cookbook_steps = [
        steps.Step(
            get_cookbook,
            'Openning the MapCookbook files',
            'Successfully opened the MapCookbook files',
            'Failed to open the MapCookbook files'
        )
    ]

    return cookbook_steps


def select_recipes(cookbook, map_nums=None):
    all_recipes = cookbook.products.values()
    if map_nums:
        return [r for r in all_recipes if r.mapnumber in map_nums]
    else:
        return all_recipes


# if __name__ == "__main__":
#     my_event_path = r"D:\MapAction\hotel\20200601-kenya-oxfam\event_description.json"
#     my_runner = steps.process_steps(get_plugin_step(), my_event_path)
#     my_cookbook = steps.process_steps(get_cookbook_steps(my_runner), None)

#     # print_kwargs(product_name="Country Overview with Admin 1 Boundaries and Topography", recipe='hello')

#     # product_name = "Country Overview with Admin 1 Boundaries and Topography"
#     map_nums = ['MA001']

#     for recipe in select_recipes(my_cookbook, map_nums):
#         product_steps = get_per_product_steps(my_runner, recipe.mapnumber, recipe.product)
#         end_result = steps.process_steps(product_steps, recipe)
