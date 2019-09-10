import json


class MapRecipe:
    '''
        Opens the recipe file specificed by recipe_json_path and creates a MapRecipe object accordingly.
        If str_def is not None then this is treated as a string representation of the json recipe.
        `recipeJsonFile` is ignored if str_def is not None. This is primarily used for testing.
    '''

    def __init__(self, recipe_json_path, str_def=None):
        self.recipe_json_path = recipe_json_path
        self.title = ""
        self.layers = []

        if str_def:
            json_contents = json.loads(str_def)
        else:
            with open(self.recipe_json_path) as json_file:
                json_contents = json.load(json_file)

        self.title = json_contents['title']
        for layer in json_contents['layers']:
            self.layers.append(LayerSpec(layer))

    def __eq__(self, other):
        if not self.title == other.title:
            return False

        if not len(self.layers) == len(other.layers):
            return False

        listcomp = list(map(lambda sl, ol: sl == ol, self.layers, other.layers))
        return all(listcomp)

    # See https://stackoverflow.com/a/25176504/3837936
    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)


class LayerSpec:
    def __init__(self, spec):
        self.map_frame = spec['map_frame']
        self.layer_group = spec['layer_group']
        self.layer_display_name = spec['layer_display_name']
        self.search_definition = spec['search_definition']
        self.data_source_path = spec['data_source_path']
        self.data_name = spec['data_name']
        self.rendering = spec['rendering']
        self.definition_query = spec['definition_query']
        self.visible = spec['visible']

    def __eq__(self, other):
        comp = [
            self.data_name == other.data_name,
            self.map_frame == other.map_frame,
            self.layer_group == other.layer_group,
            self.layer_display_name == other.layer_display_name,
            self.search_definition == other.search_definition,
            self.data_source_path == other.data_source_path,
            self.rendering == other.rendering,
            self.definition_query == other.definition_query,
            self.visible == other.visible
        ]

        return all(comp)

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
