import mapactionpy_controller.steps as steps
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.event import Event
import logging

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_plugin_step():
    def get_plugin(**kwargs):
        hum_event = kwargs['state']
        try:
            logger.debug('Attempting to load the ArcMapRunner')
            from mapactionpy_arcmap.arcmap_runner import ArcMapRunner
            runner = ArcMapRunner(hum_event)
            logger.info('Successfully loaded the ArcMapRunner')
        except ImportError:
            logger.debug('Failed to load the ArcMapRunner')
            logger.debug('Attempting to load the QGisRunner')
            from mapactionpy_qgis.qgis_runner import QGisRunner
            runner = QGisRunner()
            logger.info('Failed to load the ArcMapRunner')

        return runner

    def new_event(**kwargs):
        return Event(kwargs['state'])

    plugin_step = [
        steps.Step(
            new_event,
            logging.ERROR,
            'Loading the Humanitarian Event description file',
            'Successfully loaded the Humanitarian Event description file',
            'Failed to load the Humanitarian Event description file',
        ),
        steps.Step(
            get_plugin,
            logging.ERROR,
            'Identifying available plugins (ArcMapRunner/QGisRunner)',
            'Successfully loaded an available plugin',
            'Failed to load a suitable any plugin',
        ),
    ]

    return plugin_step


def _get_per_product_steps(_runner, recipe):
    # In due course there should be greater granularity for some of these steps
    logger.debug('Building steps for recipe {}'.format(recipe.mapnumber))

    def just_return_recipe(**kwargs):
        return recipe

    def pass_through_step(**kwargs):
        pass

    product_steps = [
        steps.Step(
            just_return_recipe,
            logging.ERROR,
            'Starting to create map "{}" - "{}"'.format(recipe.mapnumber, recipe.product),
            'Starting to create map "{}" - "{}"'.format(recipe.mapnumber, recipe.product),
            'Failed to create map "{}" - "{}"'.format(recipe.mapnumber, recipe.product),
        ),
        steps.Step(
            _runner.get_templates,
            logging.ERROR,
            'Identifying suitable map template',
            'Successfully indentifed suitable map template',
            'Failed to identify suitable map template',
        ),
        steps.Step(
            _runner.create_ouput_map_project,
            logging.ERROR,
            "Creating new '{}' file.".format(_runner.get_projectfile_extension()),
            "Successfully created new '{}' file.".format(_runner.get_projectfile_extension()),
            "Failed to create new '{}' file.".format(_runner.get_projectfile_extension())
        ),
        steps.Step(
            _runner.build_project_files,
            logging.ERROR,
            'Adding layers to the map and applying styling',
            'Successfully added layers to the map and applying styling',
            'Failed to add the layers to the map and applied styling',
        ),
        steps.Step(
            _runner.export_maps,
            logging.WARNING,
            'Exporting Maps and creating zipfile',
            'Successfully exported Maps and creating zipfile',
            'Failed to export the maps and create zipfile'
        ),
        steps.Step(
            pass_through_step,
            logging.ERROR,
            'Completed the creation of map "{}" - "{}"'.format(recipe.mapnumber, recipe.product),
            'Completed the creation of map "{}" - "{}"'.format(recipe.mapnumber, recipe.product),
            'Failed to create map "{}" - "{}"'.format(recipe.mapnumber, recipe.product),
        ),
    ]

    temp_msg = product_steps[0].running_msg
    logger.debug('Built steps for recipe {} with running_msg = {}'.format(recipe.mapnumber, temp_msg))

    return product_steps


def get_cookbook_steps(my_runner, map_number):
    def get_cookbook(**kwargs):
        lyrs = LayerProperties(my_runner.cmf, my_runner.get_lyr_render_extension(), verify_on_creation=False)
        my_cookbook = MapCookbook(my_runner.cmf, lyrs, verify_on_creation=False)

        selected_product_steps = []
        for recipe in select_recipes(my_cookbook, map_number):
            logger.debug('About to create steps for recipe {}'.format(recipe.mapnumber))
            selected_product_steps.extend(_get_per_product_steps(my_runner, recipe))

        return selected_product_steps

    cookbook_steps = [
        steps.Step(
            get_cookbook,
            logging.ERROR,
            'Openning the MapCookbook files',
            'Successfully opened the MapCookbook files',
            'Failed to open the MapCookbook files'
        )
    ]

    return cookbook_steps


def select_recipes(cookbook, map_nums=None):
    all_recipes = cookbook.products.values()

    if map_nums:
        try:
            cleaned_nums = [map_nums.upper()]
        except AttributeError:
            cleaned_nums = [mn.upper() for mn in map_nums]

        # selected_recipes = []
        # for r in all_recipes:
        #     if r.mapnumber.upper() in cleaned_nums:
        #         selected_recipes.append(r)

        selected_recipes = [r for r in all_recipes if r.mapnumber.upper() in cleaned_nums]

        logger.debug('MapIDs "{}" have been selected'.format([r.mapnumber for r in selected_recipes]))
        return selected_recipes
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
