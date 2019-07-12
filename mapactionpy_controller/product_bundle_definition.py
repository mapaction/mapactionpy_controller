import json


class MapRecipe:
    def __init__(self, recipeJsonFile):
        self.recipeJsonFile = recipeJsonFile
        self.title = ""
        self.layers = set()

        with open(self.recipeJsonFile) as json_file:
            jsonContents = json.load(json_file)
            self.title = jsonContents['title']
            for layer in jsonContents['layers']:
                self.layers.add(LayerSpec(layer))
            


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


if __name__ == '__main__':
    recipe = MapRecipe(
        r"D:\code\github\mapactionpy_controller\mapactionpy_controller\example\product_bundle_example.json")
            
    for lyr in recipe.layers:
        print('{l.map_frame}\t{l.layer_display_name}'.format(l=lyr))
