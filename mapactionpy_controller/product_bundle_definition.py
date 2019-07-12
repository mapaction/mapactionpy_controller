import json


class MapRecipe:
    '''
        Opens the recipe file specificed by recipe_json_path and creates a MapRecipe object accordingly.
        If str_def is not None then this is treated as a string representation of the json recipe. `recipeJsonFile` is ignored is str_def is not None. This is primarily used for testing.
    '''
    def __init__(self, recipe_json_path, str_def = None):
        self.recipe_json_path = recipe_json_path
        self.title = ""
        self.layers = []

        if str_def is not None:
            json_contents = json.loads(str_def)
        else:
            with open(self.recipe_json_path) as json_file:
                json_contents = json.load(json_file)

        self.title = json_contents['title']
        for layer in json_contents['layers']:
            self.layers.append(LayerSpec(layer))


class LayerSpec:
    def __init__(self, spec):
        self.map_frame = spec['map_frame']
        self.layer_group = spec['layer_group']
        self.layer_display_name = spec['layer_display_name']
        self.search_definition = spec['search_definition']
        self.data_source_path = spec['data_source_path']
        self.rendering = spec['rendering']
        self.definition_query = spec['definition_query']
        self.visable = spec['visable']
