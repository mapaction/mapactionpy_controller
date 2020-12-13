import glob
import itertools
import logging
import os

from mapactionpy_controller.recipe_layer import RecipeLayer
from mapactionpy_controller.steps import Step


def get_recipe_event_updater(hum_event):
    """
    Creates a function which will update a recipe with situation specific information about the
    Humanitarian Event. Certain strings within a recipe can be can include "replacement fields"
    using Python's String format Syntax
    (https://docs.python.org/3.3/library/string.html#formatstrings)

    This method replaces those strings with runtime values. Replacement fields referencing the humanitarian
    event object should use the name `e`. For example, the value of `recipe.summary` could be set in
    the recipe files to:
    ```
    recipe.summary = "Overview map of {e.country_name}"
    ```
    This method will update that string with the country name from `self.event`:
    ```
    recipe.summary = "Overview map of Atlantis"
    ```

    The following fields within a recipe are updated:

    * `product`
    * `summary`
    * `lyr.reg_exp` for every layer
    * `lyr.definition_query`
    * `lbl_class.expression`
    * `lbl_class.sql_query`

    If the input strings do not include any replacement fields the recipe is returned unaltered.

    @kwargs state: The recipe to be updated.
    @returns The same recipe object with the relevant strings updated as appropriate.
    """
    def update_recipe_item(item):
        try:
            return item.format(e=hum_event)
        except IndexError:
            return item

    def update_recipe_with_event_details(**kwargs):
        recipe = kwargs['state']
        return _update_items_in_recipe(recipe, update_recipe_item)

    return update_recipe_with_event_details


def _update_items_in_recipe(recipe, update_recipe_item):
    for lyr in itertools.chain(*[mf.layers for mf in recipe.map_frames]):
        lyr.reg_exp = update_recipe_item(lyr.reg_exp)
        lyr.definition_query = update_recipe_item(lyr.definition_query)

        for lbl_class in lyr.label_classes:
            lbl_class.expression = update_recipe_item(lbl_class.expression)
            lbl_class.sql_query = update_recipe_item(lbl_class.sql_query)

    # Update the recipe level members
    recipe.product = update_recipe_item(recipe.product)
    recipe.summary = update_recipe_item(recipe.summary)

    return recipe


def _check_layer(recipe_lyr):
    """
    Checks that the recipe is a MapRecipe object.

    @param recipe_lyr: The object to be checked.
    @raises ValueError: If recipe_lyr is not an instance of MapRecipe.
    """
    if not isinstance(recipe_lyr, RecipeLayer):
        error_msg = (
            'Unable to `get_lyr_data_finder` when MapRecipe is not validated against LayerProerties.'
            ' This method needs a RecipeLayer object not just a string placeholder.'
            ' layer_name = "{}"'.format(recipe_lyr)
        )
        logging.error(error_msg)
        raise ValueError(error_msg)


def get_all_gisfiles(cmf):
    gisfiles_with_paths = set()

    for extn in ['.shp', '.img', '.tif']:
        for f_path in glob.glob('{}/*/*{}'.format(cmf.active_data, extn)):
            gisfiles_with_paths.add(f_path)

    return gisfiles_with_paths


def get_per_product_data_search_steps(runner, recipe):
    """

    1) Find all possible datasources for a layer
            JIRA if there are multiple datasources per layer

    2) Check that all datasources match the required schema
            JIRA if there is a schema mismatch.

    3) Calculate checksum

    4) Calculate extent

    """
    # ds = DataSearch(hum_event)
    all_gis_files = [(f_path, os.path.basename(f_path)) for f_path in get_all_gisfiles(runner.cmf)]

    step_list = [
        Step(
            get_recipe_event_updater(runner.hum_event),
            logging.ERROR,
            'Updating recipe with event specific details',
            'Updated recipe with event specific details',
            'Failed to update recipe with event specific details'
        )]

    for map_frame in recipe.map_frames:
        for recipe_lyr in map_frame.layers:
            # This is just being paraniod. This can only occur if somewhere up the chain a MapCookbook was created
            # with the param verify_on_creation=False. That should not occur in production code and only in
            # some test cases.
            _check_layer(recipe_lyr)
            step_list.extend([
                Step(
                    recipe_lyr.get_data_finder(runner.cmf, all_gis_files),
                    logging.WARNING,
                    '"Searching for data suitable for layer "{}"'.format(recipe_lyr.name),
                    'Found data for layer "{}"'.format(recipe_lyr.name),
                    'Failed to find data suitable for layer "{}"'.format(recipe_lyr.name)
                ),
                Step(
                    recipe_lyr.calc_extent,
                    logging.WARNING,
                    'Calculating extent for the data for layer "{}"'.format(recipe_lyr.name),
                    'Calculated extent for the data for layer "{}"'.format(recipe_lyr.name),
                    'Error whilst calculating extent for the data for layer "{}"'.format(recipe_lyr.name)
                ),
                Step(
                    recipe_lyr.check_data_against_schema,
                    logging.WARNING,
                    'Checking the schema for the data available for layer "{}"'.format(recipe_lyr.name),
                    'Verified schema the data available for layer "{}"'.format(recipe_lyr.name),
                    'The data available for layer "{}" failed schema check'.format(recipe_lyr.name)
                )
            ])

        step_list.extend([
            Step(
                map_frame.calc_extent,
                logging.WARNING,
                'Calculating extent for the map frame "{}"'.format(map_frame.name),
                'Calculated extent for the map frame "{}"'.format(map_frame.name),
                'Error whilst extent for the map frame "{}"'.format(map_frame.name)
            )
        ])

    return step_list
