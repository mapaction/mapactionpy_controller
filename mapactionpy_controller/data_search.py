from crash_move_folder import CrashMoveFolder
from event import Event
from product_bundle_definition import MapRecipe

class DataSearch():
    def __init__(self, cmf):
        self.cmf = cmf

    def update_search_with_event_details(self, recipe, event):
        for lyr in recipe.layers:
            output_str = lyr.search_definition.format(e=event)
            print('{}\t{}'.format(lyr.search_definition, output_str))
