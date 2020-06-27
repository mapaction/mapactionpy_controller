import logging
from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.steps import Step


class ConfigVerifier():
    def __init__(self, cmf_desc, lyr_file_exn_list):
        self.cmf_desc_path = cmf_desc
        self.lyr_file_exn_list = lyr_file_exn_list

    def check_cmf_description(self, **kwargs):
        self.cmf = CrashMoveFolder(self.cmf_desc_path)
        return ('The Crash Move Folder description file open correctly:\n"{}"\n'.format(
            self.cmf_desc_path
        ))

    def check_json_file_schemas(self, **kwargs):
        try:
            # JSON schema validation is implicit in the creation of these objects
            self.check_cmf_description()
            lp = LayerProperties(self.cmf, '', verify_on_creation=False)
            MapCookbook(self.cmf, lp, verify_on_creation=False)
            return('No json validation problems were detected in the parsing of these two'
                   ' files:\n"{}"\n"{}"'.format(lp.cmf.layer_properties, self.cmf.map_definitions)
                   )
        except ValueError:
            raise

    def check_lyr_props_vs_rendering_dir(self, **kwargs):
        cmf = CrashMoveFolder(self.cmf_desc_path)
        for lyr_exn in self.lyr_file_exn_list:
            try:
                LayerProperties(cmf, lyr_exn, verify_on_creation=True)
                return('No inconsistency detected between:\n'
                       ' * the contents of the layer properties json file:\n\t{props}\n'
                       ' * and layer rendering dir:\n\t{render}\n'.format(
                           props=cmf.layer_properties,
                           render=cmf.layer_rendering
                       ))
            except ValueError:
                raise

    def check_lyr_props_vs_map_cookbook(self, **kwargs):
        try:
            cmf = CrashMoveFolder(self.cmf_desc_path)
            lyrs = LayerProperties(cmf, '', verify_on_creation=False)
            MapCookbook(cmf, lyrs, verify_on_creation=True)
            return('No inconsistency detected between:\n'
                   ' * the contents of the layer properties json file:\n\t{props}\n'
                   ' * and the contents of the MapCookbook json:\n\t{cbook}\n'.format(
                       props=cmf.layer_properties,
                       cbook=cmf.map_definitions
                   ))
        except ValueError:
            raise


def get_config_verify_steps(cmf_desc_path, lyr_file_exn_list):
    cv = ConfigVerifier(cmf_desc_path, lyr_file_exn_list)

    config_verify_steps = [
        Step(
            cv.check_cmf_description,
            logging.WARNING,
            'Checking that the Crash Move Folder description file opens correctly',
            'The Crash Move Folder description file opened correctly',
            'Failed to open the Crash Move Folder description file correctly',
        ),
        Step(
            cv.check_json_file_schemas,
            logging.WARNING,
            'Checking that each of the configuration files matches their relevant schemas',
            'Each of the configuration files adheres to their relevant schemas',
            'Failed to verify one or more of the configuration files against the relevant schema',
        ),
        Step(
            cv.check_lyr_props_vs_rendering_dir,
            logging.WARNING,
            'Comparing the contents of the layer properties json file and the layer rendering directory',
            'Compared the contents of the layer properties json file and the layer rendering directory',
            'Inconsistancy found in between the contents of the layer properties json file and the layer'
            ' rendering directory'
        ),
        Step(
            cv.check_lyr_props_vs_map_cookbook,
            logging.WARNING,
            'Comparing the contents of the layer properties json file and the MapCookbook',
            'Compared the contents of the layer properties json file and the MapCookbook',
            'Inconsistancy found in between the contents of the layer properties json file and the MapCookbook'
        )
    ]

    return config_verify_steps
