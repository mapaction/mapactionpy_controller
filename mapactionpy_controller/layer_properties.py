import json
import os
from mapactionpy_controller.map_layer import MapLayer
from mapactionpy_controller.crash_move_folder import CrashMoveFolder


class LayerProperties:
    """
    LayerProperties

    It is expected that a seperate LayerProperties object will be created for each layer_rendering
    file type.
    """

    def __init__(self, cmf, extension, verify_on_creation=True):
        """
        Positional Arguments:
            * cmf: Either a CrashMoveFolder object or a path to a cmf_description.json file. If it
                   is a CrashMoveFolder object and cmf.verify_paths() returns False then an
                   ValueError exception will be rasied.
                   TODO note the type of exception
            * extension: The file extension of the layer_rendering file type. (typically `.lyr` for
                         ESRI Layer files, `'.qml` for QGIS style)

        Optional Named Arguments
            verify_on_creation: True by default. If True then
            `verify_match_with_layer_rendering_dir()` will be called from the constructor.

        """
        # @TODO Integrate validation utility here...

        try:
            if cmf.verify_paths():
                self.cmf = cmf
            else:
                raise ValueError('The `cmf` parameter for LayerProperties.__init__() can accept'
                                 'values where the paths verify. eg `cmf.verify_paths() == True`.'
                                 'The value passed failed this test')
        except AttributeError:
            self.cmf = CrashMoveFolder(cmf, verify_on_creation=True)

        self.extension = extension
        self.properties = {}  # Dictionary
        self._parse()

        if verify_on_creation:
            self.verify_match_with_layer_rendering_dir()

    def _parse(self):
        """
        Reads layer properties file
        """
        with open(self.cmf.layer_properties) as json_file:
            jsonContents = json.load(json_file)
            for layer in jsonContents['layerProperties']:
                mapLayer = MapLayer(layer)
                self.properties[mapLayer.layerName] = mapLayer

    def verify_match_with_layer_rendering_dir(self):
        lp_unique_lyrs = set()
        files_unique = set()

        for l in self.properties:
            lp_unique_lyrs.add(l.layerName)

        dir_content = os.listdir(self.cmf.layer_rendering)
        for f in filter(os.path.isfile, dir_content):
            filename, fileext = os.path.splitext(f)
            if fileext == self.extension:
                files_unique.add(filename)

        sym_diff = lp_unique_lyrs.symmetric_difference(files_unique)

        return len(sym_diff)
