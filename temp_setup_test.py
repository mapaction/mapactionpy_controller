def get_gis_environment():
    gis_dependencies = []

    try:
        import arcpy  # noqa
        gis_dependencies.append('mapactionpy_arcmap')
    except ImportError:
        pass

    try:
        import arcpy  # noqa
        gis_dependencies.append('mapactionpy_arcpro')
    except ImportError:
        pass

    try:
        import qgis.core  # noqa
        gis_dependencies.append('mapactionpy_qgis')
    except ImportError:
        pass

    return gis_dependencies


if __name__ == "__main__":
    print(get_gis_environment())
