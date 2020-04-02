import importlib
import distutils.version as version

_base_version = '0.10'


def get_gis_environment():
    gis_dependancies = []

    v = version.StrictVersion(_base_version)
    next_minor_version = '{}.{}'.format(v.version[0], v.version[1]+1)

    possible_envs = {'arcpy': 'mapactionpy_arcmap',
                     'qgis.core': 'mapactionpy_qgis'}

    for env_mod, target_mod in possible_envs.items():
        print(env_mod, target_mod)
        try:
            importlib.import_module(env_mod)
            gis_dependancies.append('{}>={},<{}'.format(target_mod, _base_version, next_minor_version))
        except ImportError:
            pass

    return gis_dependancies


if __name__ == "__main__":
    print(get_gis_environment())
