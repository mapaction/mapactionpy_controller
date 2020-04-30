import os
import pycountry
from mapactionpy_controller.map_data import MapData
from mapactionpy_controller.map_doc import MapDoc


class XmlExporter:
    def __init__(self, event, chef):
        self.event = event
        self.chef = chef

    def write(self, params):
        # Set up dictionary for all the values required for the export XML file
        exportPropertiesDict = self.setExportParameters(params)
        exportData = MapData(exportPropertiesDict)
        mapDocument = MapDoc(exportData)

        exportXmlFileName = params["coreFileName"]+".xml"
        exportXmlFileLocation = os.path.join(params["exportDirectory"], exportXmlFileName)

        f = open(exportXmlFileLocation, "w")
        f.write(mapDocument.to_xml())
        f.close()

        return exportXmlFileLocation

    def setExportParameters(self, params):
        exportPropertiesDict = {}
        exportPropertiesDict["versionNumber"] = params["versionNumber"]
        exportPropertiesDict["mapNumber"] = params["mapNumber"]
        exportPropertiesDict["operationID"] = self.event.operation_id
        exportPropertiesDict["sourceorg"] = self.event.default_source_organisation
        exportPropertiesDict["pdffilename"] = params["pdfFileName"]
        exportPropertiesDict["jpgfilename"] = params["jpgFileName"]
        exportPropertiesDict["pdffilesize"] = params["pdfFileSize"]
        exportPropertiesDict["jpgfilesize"] = params["jpgFileSize"]
        exportPropertiesDict["glideno"] = self.event.glide_number
        exportPropertiesDict["title"] = params["productName"]
        exportPropertiesDict["countries"] = self.event.country_name
        exportPropertiesDict["xmin"] = params["xmin"]
        exportPropertiesDict["ymin"] = params["ymin"]
        exportPropertiesDict["xmax"] = params["xmax"]
        exportPropertiesDict["ymax"] = params["ymax"]
        exportPropertiesDict["ref"] = params["coreFileName"]
        exportPropertiesDict["mxdfilename"] = params["coreFileName"]
        exportPropertiesDict["paperxmax"] = ""
        exportPropertiesDict["paperxmin"] = ""
        exportPropertiesDict["paperymax"] = ""
        exportPropertiesDict["paperymin"] = ""
        exportPropertiesDict["pdfresolutiondpi"] = self.event.default_pdf_res_dpi
        exportPropertiesDict["jpgresolutiondpi"] = self.event.default_jpeg_res_dpi
        if (params["versionNumber"] == 1):
            exportPropertiesDict["status"] = "New"
        else:
            exportPropertiesDict["status"] = "Update"

        exportPropertiesDict["language-iso2"] = self.event.language_iso2
        language = pycountry.languages.get(alpha_2=self.event.language_iso2)
        if (language is not None):
            exportPropertiesDict["language"] = language.name
        else:
            exportPropertiesDict["language"] = None
        exportPropertiesDict["createdate"] = None
        exportPropertiesDict["createtime"] = None
        exportPropertiesDict["summary"] = None
        exportPropertiesDict["scale"] = None
        exportPropertiesDict["datum"] = None

        if (self.chef is not None):
            exportPropertiesDict["createdate"] = self.chef.createDate
            exportPropertiesDict["createtime"] = self.chef.createTime
            exportPropertiesDict["summary"] = self.chef.summary
            exportPropertiesDict["scale"] = self.chef.scale()
            exportPropertiesDict["datum"] = self.chef.spatialReference()
        exportPropertiesDict["imagerydate"] = ""
        exportPropertiesDict["product-type"] = params["productType"]
        exportPropertiesDict["papersize"] = "A3"
        exportPropertiesDict["access"] = "MapAction"  # Until we work out how to get the values for this
        exportPropertiesDict["accessnotes"] = ""
        exportPropertiesDict["location"] = ""
        exportPropertiesDict["qclevel"] = "Automatically generated"
        exportPropertiesDict["qcname"] = ""
        exportPropertiesDict["themes"] = {}
        exportPropertiesDict["proj"] = ""
        exportPropertiesDict["datasource"] = ""
        exportPropertiesDict["kmlresolutiondpi"] = ""
        return exportPropertiesDict
