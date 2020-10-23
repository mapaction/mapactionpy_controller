import glob
import logging
import os
import re
from mapactionpy_controller.steps import Step
import mapactionpy_controller.task_renderer as task_renderer
from mapactionpy_controller.map_recipe import RecipeLayer


class FixMissingGISDataTask(task_renderer.TaskReferralBase):
    _task_template_filename = 'missing-gis-file'
    _primary_key_template = 'Could not find data for "{{<%layer.name%>}}"'

    def __init__(self, recipe_lyr, cmf):
        super(FixMissingGISDataTask, self).__init__()
        self.context_data.update(task_renderer.layer_adapter(recipe_lyr))
        self.context_data.update(task_renderer.cmf_description_adapter(cmf))


class FixMultipleMatchingFilesTask(task_renderer.TaskReferralBase):
    _task_template_filename = 'multiple-matching-files'
    _primary_key_template = 'More than one dataset available for "{{<%layer.name%>}}"'

    def __init__(self, recipe_lyr, cmf, datasources_list):
        super(FixMultipleMatchingFilesTask, self).__init__()
        self.context_data.update(task_renderer.layer_adapter(recipe_lyr))
        self.context_data.update(task_renderer.cmf_description_adapter(cmf))
        # Roll-our-own one-line adapter here:
        self.context_data.update({
            'datasources_list': [{'datasources': datasources} for datasources in sorted(datasources_list)]
        })


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
    # Update the reg_exg for seaching for each individual layer
    for lyr in recipe.all_layers():
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


def _check_found_files(found_files, recipe_lyr, cmf):
    """
    This method checks the list of files in `get_lyr_data_finder`. It is called within `get_lyr_data_finder`
    so there is no need to call it seperately. A 'ValueError' exception, along with a Task and task
    description will be raised if there are too few or too many files in the `found_files` list.

    @param found_files: A list of tuples. Each tuple should be represent one of the files found and the tuple
                        should be in the format `(full_path, filename_without_extension)`
    @param recipe_lyr: The recipe being processed. Used for providing contact to any error message that may
                       be created.
    @param cmf: The crash move folder being searched. Used for providing contact to any error message that
                may be created.
    @raises ValueError: If there is not exactly one file in the found_files lilst.
    """
    # If no data matching is found:
    # Test on list of paths as they are guarenteed to be unique, whereas base filenames are not
    if not found_files:
        missing_data_task = FixMissingGISDataTask(recipe_lyr, cmf)
        raise ValueError(missing_data_task)

    # If multiple matching files are found
    if len(found_files) > 1:
        found_datasources = [f_path for f_path, f_name in found_files]
        multiple_files_task = FixMultipleMatchingFilesTask(recipe_lyr, cmf, found_datasources)
        raise ValueError(multiple_files_task)


def get_lyr_data_finder(cmf, recipe_lyr):
    """
    This method returns a function which tests for the existance of data that matches
    the param `recipe_lyr.reg_exp`.

    Create a new function for each layer within a recipe.
    """
    # This is just being paraniod. This can only occur if somewhere up the chain a MapCookbook was created
    # with the param verify_on_creation=False. That should not occur in production code and only in
    # some test cases.
    _check_layer(recipe_lyr)

    # Get list of files, so that they are only queried on disk once.
    # Make this into a list of full_paths (as returned by `get_all_gisfiles(cmf)`) and
    # just the file name
    all_gis_files = [(f_path, os.path.basename(f_path)) for f_path in get_all_gisfiles(cmf)]

    def _data_finder(**kwargs):
        recipe = kwargs['state']

        # Again this is being paraniod. This can only occur if there are more than one MapRecipe objects
        # being proceed simulatiously. There is isn't currently a use case where that would occur in
        # production code. This check is present just in case.
        if recipe_lyr not in recipe.all_layers():
            error_msg = 'Attempting to update a layer ("{}") which is not part of the recipe'.format(
                recipe_lyr.name)
            logging.error(error_msg)
            raise ValueError(error_msg)

        found_files = []

        # Match filename *including extension* against regex
        # But only store the filename without extension
        found_files.extend(
            [(f_path, os.path.splitext(f_name)[0])
             for f_path, f_name in all_gis_files if re.match(recipe_lyr.reg_exp, f_name)]
        )

        # Do checks and raise exceptions if required.
        _check_found_files(found_files, recipe_lyr, cmf)

        # else assume everthing is OK:
        recipe_lyr.data_source_path, recipe_lyr.data_name = found_files.pop()

        return recipe

    return _data_finder


def get_all_gisfiles(cmf):
    gisfiles_with_paths = set()

    for extn in ['.shp', '.img', '.tif']:
        for f_path in glob.glob('{}/*/*{}'.format(cmf.active_data, extn)):
            gisfiles_with_paths.add(f_path)

    return gisfiles_with_paths


def get_per_product_data_search_steps(cmf, hum_event, recipe):
    """

    1) Find all possible datasources for a layer
            JIRA if there are multiple datasources per layer

    2) Check that all datasources match teh required schema
            JIRA if there is a schema mismatch.

    3) Calculate checksum

    """
    # ds = DataSearch(hum_event)

    step_list = [
        Step(
            get_recipe_event_updater(hum_event),
            logging.ERROR,
            'Updating recipe with event specific details',
            'Updated recipe with event specific details',
            'Failed to update recipe with event specific details'
        )]

    for recipe_lyr in recipe.all_layers():
        step_list.extend([
            Step(
                get_lyr_data_finder(cmf, recipe_lyr),
                logging.WARNING,
                '"Searching for data suitable for layer "{}"'.format(recipe_lyr.name),
                'Found data for layer "{}"'.format(recipe_lyr.name),
                'Failed to find data suitable for layer "{}"'.format(recipe_lyr.name)
            )
        ])

        # Step(
        #     ds.check schema(),
        #     logging.WARNING,
        #     'Checking the schema for the data available for layer "{}"'.format(recipe_lyr.name),
        #     'Verified schema the data available for layer "{}"'.format(recipe_lyr.name),
        #     'The data available for layer "{}" failed schema check'.format(recipe_lyr.name)
        # ),
        # Step(
        #     ds.calculate checksum(),
        #     logging.ERROR,
        #     'Calculating checksum for the data for layer "{}"'.format(recipe_lyr.name),
        #     'Calculated checksum for the data for layer "{}"'.format(recipe_lyr.name),
        #     'Error whilst calculating checksum for the data for layer "{}"'.format(recipe_lyr.name)
        # )

    return step_list
