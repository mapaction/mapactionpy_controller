import re
import os

class DataSearch():
    def __init__(self, cmf):
        self.cmf = cmf

    def update_search_with_event_details(self, recipe, event):
        for lyr in recipe.layers:
            output_str = lyr.search_definition.format(e=event)
            lyr.search_definition = output_str

        return recipe

    def update_recipe_with_datasources(self, recipe):
        for lyr in recipe.layers:
            lyr.data_source_path = self._find_datasource(lyr)

        return recipe

    def _find_datasource(self, lyr):
        found = []
        for root, dirs, files in os.walk(self.cmf.active_data):
            for f in files:
                if re.match(lyr.search_definition, f):
                    found.append(os.path.normpath(os.path.join(root, f)))

        return ';'.join(found)
