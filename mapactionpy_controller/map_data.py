# Required to generate Export XML
# Mapdata in its own class so that it's held in the inner mapdata block:
#
# <?xml version="1.0" ?>
# <mapdoc>
#    <mapdata>


class MapData:
    def __init__(self, row):
        # Constructor.  Creates an instance of MapData for the Export XML

        self.versionNumber = row["versionNumber"]
        self.mapNumber = row["mapNumber"]
        self.operationID = row["operationID"]
        self.sourceorg = row["sourceorg"]
        self.glideno = row["glideno"]

        self.jpgfilename = row["jpgfilename"]
        self.pdffilename = row["pdffilename"]
        self.jpgfilesize = row["jpgfilesize"]
        self.pdffilesize = row["pdffilesize"]

        self.title = row["title"]
        self.ref = row["ref"]
        self.language = row["language"]
        self.countries = row["countries"]
        self.createdate = row["createdate"]
        self.createtime = row["createtime"]
        self.status = row["status"]
        self.xmin = row["xmin"]
        self.ymin = row["ymin"]
        self.xmax = row["xmax"]
        self.ymax = row["ymax"]
        self.proj = row["proj"]
        self.datum = row["datum"]
        self.qclevel = row["qclevel"]
        self.qcname = row["qcname"]
        self.access = row["access"]
        self.summary = row["summary"]
        self.imagerydate = row["imagerydate"]
        self.datasource = row["datasource"]
        self.location = row["location"]
        self.themes = row["themes"]
        self.scale = row["scale"]
        self.papersize = row["papersize"]
        self.jpgresolutiondpi = row["jpgresolutiondpi"]
        self.pdfresolutiondpi = row["pdfresolutiondpi"]
        self.kmlresolutiondpi = row["kmlresolutiondpi"]
        self.mxdfilename = row["mxdfilename"]
        self.paperxmax = row["paperxmax"]
        self.paperxmin = row["paperxmin"]
        self.paperymax = row["paperymax"]
        self.paperymin = row["paperymin"]
        self.accessnotes = row["accessnotes"]
        self.product_type = row["product-type"]  # Name contains hyphen "-"
        self.language_iso2 = row["language-iso2"]  # Name contains hyphen "-"
