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
        # Copy from params
        exportPropertiesDict["versionNumber"] = params["versionNumber"]
        exportPropertiesDict["mapNumber"] = params["mapNumber"]
        exportPropertiesDict["themes"] = params["themes"]
        exportPropertiesDict["pdffilename"] = params["pdfFileName"]
        exportPropertiesDict["jpgfilename"] = params["jpgFileName"]
        exportPropertiesDict["pdffilesize"] = params["pdfFileSize"]
        exportPropertiesDict["jpgfilesize"] = params["jpgFileSize"]
        exportPropertiesDict["title"] = params["productName"]
        exportPropertiesDict["xmin"] = params["xmin"]
        exportPropertiesDict["ymin"] = params["ymin"]
        exportPropertiesDict["xmax"] = params["xmax"]
        exportPropertiesDict["ymax"] = params["ymax"]
        exportPropertiesDict["ref"] = params["coreFileName"]
        exportPropertiesDict["mxdfilename"] = params["coreFileName"]
        exportPropertiesDict["product-type"] = params["productType"]
        exportPropertiesDict["summary"] = params["summary"]
        # Fixed values
        exportPropertiesDict["imagerydate"] = params.get('imagerydate', "")
        exportPropertiesDict["papersize"] = params.get('papersize', "A3")
        exportPropertiesDict["access"] = params.get('access', "MapAction")
        exportPropertiesDict["accessnotes"] = params.get('accessnotes', "")
        exportPropertiesDict["location"] = params.get('location', "")
        exportPropertiesDict["qclevel"] = params.get('qclevel', "Automatically generated")
        exportPropertiesDict["qcname"] = params.get('qcname', "")
        exportPropertiesDict["proj"] = params.get('proj', "")
        exportPropertiesDict["datasource"] = params.get('datasource', "")
        exportPropertiesDict["kmlresolutiondpi"] = params.get('kmlresolutiondpi', "")
        exportPropertiesDict["paperxmax"] = params.get('paperxmax', "")
        exportPropertiesDict["paperxmin"] = params.get('paperxmin', "")
        exportPropertiesDict["paperymax"] = params.get('paperymax', "")
        exportPropertiesDict["paperymin"] = params.get('paperymin', "")
        exportPropertiesDict["createdate"] = params.get('createdate', "")
        exportPropertiesDict["createtime"] = params.get('createtime', "")
        exportPropertiesDict["scale"] = params.get('scale', "")
        exportPropertiesDict["datum"] = params.get('datum', "")
        exportPropertiesDict["language-iso2"] = self.event.language_iso2
        exportPropertiesDict["pdfresolutiondpi"] = self.event.default_pdf_res_dpi
        exportPropertiesDict["jpgresolutiondpi"] = self.event.default_jpeg_res_dpi
        exportPropertiesDict["countries"] = self.event.country_name
        exportPropertiesDict["glideno"] = self.event.glide_number
        exportPropertiesDict["operationID"] = self.event.operation_id
        exportPropertiesDict["sourceorg"] = self.event.default_source_organisation

        if (params["versionNumber"] == 1):
            exportPropertiesDict["status"] = "New"
        else:
            exportPropertiesDict["status"] = "Update"

        language = pycountry.languages.get(alpha_2=self.event.language_iso2)
        if (language is not None):
            exportPropertiesDict["language"] = language.name
        else:
            exportPropertiesDict["language"] = None

        if (self.chef is not None):
            exportPropertiesDict["createdate"] = self.chef.createDate
            exportPropertiesDict["createtime"] = self.chef.createTime
            exportPropertiesDict["scale"] = self.chef.scale()
            exportPropertiesDict["datum"] = self.chef.spatialReference()

        # return
        return exportPropertiesDict
