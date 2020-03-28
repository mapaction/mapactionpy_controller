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
            * extension: The file extension of the layer_rendering file type. (typically `.lyr` for
                         ESRI Layer files, `'.qml` for QGIS style)

        Optional Named Arguments
            verify_on_creation: True by default. If True then
            `verify_match_with_layer_rendering_dir()` will be called from the constructor.

        """
        try:
            if cmf.verify_paths():
                self.cmf = cmf
            else:
                raise ValueError('The `cmf` parameter for LayerProperties.__init__() can only accept'
                                 'values where the paths verify. eg `cmf.verify_paths() == True`.'
                                 'The value passed in this case failed this test')
        except AttributeError:
            self.cmf = CrashMoveFolder(cmf, verify_on_creation=True)

        self.extension = extension
        self.properties = {}  # Dictionary
        self._parse()

        if verify_on_creation:
            lp_only, files_only = self.get_difference_with_layer_rendering_dir()
            if len(lp_only) or len(files_only):
                msg = self._get_verify_failure_message(lp_only, files_only)
                raise ValueError(msg)

    def _get_verify_failure_message(self, lp_only, files_only):
        msg = ('There is a mismatch between:\n'
               ' (a) The layers described in the layer_properties.json file "{}"\n'
               ' and (b) The layers files, with file extension "{}", listed in the'
               ' `cmf.layer_rendering` directory "{}".\n'
               ' Either ensure that these files match, or create the LayerProperties object using the'
               ' parameter `verify_on_creation=False`\n'.format(
                   self.cmf.layer_properties,
                   self.extension,
                   self.cmf.layer_rendering
               ))

        if len(lp_only):
            msg = msg + "\nThe following layers are only in layer properties json file:\n\t"
            msg = msg + "\n\t".join(lp_only)
        if len(files_only):
            msg = msg + "\nThe following files are only in layer rendering directory:\n\t"
            msg = msg + "\n\t".join(files_only)

        return msg

    def _parse(self):
        """
        Reads layer properties file
        """
        with open(self.cmf.layer_properties) as json_file:
            jsonContents = json.load(json_file)
            for layer in jsonContents['layerProperties']:
                mapLayer = MapLayer(layer)
                self.properties[mapLayer.layerName] = mapLayer

    def get_difference_with_layer_rendering_dir(self):
        """
        Ensures that there is a one-to-one correspondance between
        * The layers described in the layer_properties.json file
        * The layers files, with the relevant file extension, listed in the `cmf.layer_rendering` directory
        By default this method is called from the constructor. It can also be called at any later time, in case the
        contents of the `cmf.layer_rendering` directory has changes on disk.
        NB: Changes to the `layer_properties.json` on disk are NOT accomadated but repeated calling of this method.

        :returns: A tuple of sets:
            * The first set is the set of layers which are in Layer Properties json file, but are in the Layer
              Rendering Directory.
            * The secound set is the set of layers which are in the Layer Rendering Directory, but not in the in Layer
              Properties json file.
        In the "ideal" senario, both sets both be empty.
        """
        lp_unique_lyrs = set()
        files_unique = set()

        for layer_name in self.properties:
            lp_unique_lyrs.add(layer_name)

        dir_content = os.listdir(self.cmf.layer_rendering)
        for f in dir_content:
            f_path = os.path.join(self.cmf.layer_rendering, f)
            filename, fileext = os.path.splitext(f)
            if (os.path.isfile(f_path)) and (fileext == self.extension):
                files_unique.add(filename)

        # sym_diff = lp_unique_lyrs.symmetric_difference(files_unique)
        lp_only = lp_unique_lyrs.difference(files_unique)
        files_only = files_unique.difference(lp_unique_lyrs)

        return lp_only, files_only
