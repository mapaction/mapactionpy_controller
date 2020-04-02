def get_gis_environment():
    gis_dependancies = []

    try:
        import arcpy  # noqa
        gis_dependancies.append('mapactionpy_arcmap')
    except ImportError:
        pass

    try:
        import qgis.core  # noqa
        gis_dependancies.append('mapactionpy_qgis')
    except ImportError:
        pass

    return gis_dependancies


if __name__ == "__main__":
    print(get_gis_environment())
