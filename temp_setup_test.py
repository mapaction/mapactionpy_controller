def get_gis_environment():
    gis_dependancies = []

    try:
        import arcpy
        gis_dependancies.append('mapactionpy_arcmap')
    except ImportError:
        pass

    try:
        import qgis.core
        gis_dependancies.append('mapactionpy_qgis')
    except ImportError:
        pass

    return gis_dependancies


if __name__ == "__main__":
    print(get_install_requires())

