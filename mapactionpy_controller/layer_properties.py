import json
import os
from mapactionpy_controller.map_recipe import RecipeLayer
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

        if len(extension) == 0 or extension.startswith('.'):
            self.extension = extension
        else:
            self.extension = '.{}'.format(extension)

        self.properties = {}  # Dictionary
        self._parse()

        if verify_on_creation:
            msg = self.get_difference_with_other_layer_set(
                self._get_lyr_rendering_names_as_set(),
                self._get_mismatch_with_layer_rendering_message
            )
            if msg:
                raise ValueError(msg)

    def _parse(self):
        """
        Reads layer properties file
        """
        with open(self.cmf.layer_properties) as json_file:
            jsonContents = json.load(json_file)
            for layer in jsonContents['layerProperties']:
                mapLayer = RecipeLayer(layer, self)
                self.properties[mapLayer.name] = mapLayer

    def _get_lyr_rendering_names_as_set(self):
        files_unique = set()
        dir_content = os.listdir(self.cmf.layer_rendering)
        for f in dir_content:
            f_path = os.path.join(self.cmf.layer_rendering, f)
            filename, fileext = os.path.splitext(f)
            if (os.path.isfile(f_path)) and (fileext == self.extension):
                files_unique.add(filename)

        return files_unique

    def is_difference_with_layer_rendering_dir(self):
        msg = self.get_difference_with_other_layer_set(
            self._get_lyr_rendering_names_as_set(),
            self._get_mismatch_with_layer_rendering_message
        )
        return bool(msg)

    def get_difference_with_other_layer_set(self, other_lyrs, get_msg_func):
        """
        Ensures that there is a one-to-one correspondance between
        * The layers described by this LayerProperties Object
        * Another set() listing layers from any source.

        For example this method is used to verify the consistency between
        * The layer_properties.json file and the files listed in the `cmf.layer_rendering` directory
        * The layer_properties.json file and the map_cookbook.json file.

        :returns:
            * `None`: if there are no differences between the LayerProperties and the `other_lyrs` set.
            * A message describing the differences between the two. The message is constructed by
              the `get_msg_func` supplied. The supplied funtion must accept two sets `lp_only` and `others_only`.
              Each of the two sets incldue onyl those layers which occur uniquely in each. The message is
              constructed like so:
                  msg = get_msg_func(lp_only, others_only)
        """
        lp_unique_lyrs = set(self.properties)

        lp_only = lp_unique_lyrs.difference(other_lyrs)
        others_only = other_lyrs.difference(lp_unique_lyrs)

        msg = None
        if len(lp_only) or len(others_only):
            msg = get_msg_func(lp_only, others_only)

        return msg

    def _get_mismatch_with_layer_rendering_message(self, lp_only, files_only):
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

        pair = ((lp_only, "The following layers are only present in layer properties json file:"),
                (files_only, "The following files are only present in layer rendering directory:"))

        return self._msg_builder(pair, msg)

    def _msg_builder(self, pair, msg):
        for lyrs, s in pair:
            if len(lyrs):
                msg = msg + '\n{}\n\t'.format(s)
                msg = msg + '\n\t'.join(lyrs)

        return msg
