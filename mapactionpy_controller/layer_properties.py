import json
from map_layer import MapLayer


class LayerProperties:
    def __init__(self, layerPropertiesJsonFile):
        # @TODO Integrate validation utility here...
        self.layerPropertiesJsonFile = layerPropertiesJsonFile
        self.properties = {}  # Dictionary
        self._parse()

    def _parse(self):
        """
        Reads layer properties file
        """
        with open(self.layerPropertiesJsonFile) as json_file:
            jsonContents = json.load(json_file)
            for layer in jsonContents['layerProperties']:
                mapLayer = MapLayer(layer)
                self.properties[mapLayer.layerName] = mapLayer
