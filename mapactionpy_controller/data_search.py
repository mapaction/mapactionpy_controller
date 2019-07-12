import pickle 

class DataSearch():
    def __init__(self, cmf):
        self.cmf = cmf

    def update_search_with_event_details(self, recipe, event):
        for lyr in recipe.layers:
            output_str = lyr.search_definition.format(e=event)
            lyr.search_definition = output_str

        return recipe
