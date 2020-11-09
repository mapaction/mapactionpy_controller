from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom


class MapDoc:
    # Required to generate 'mapdoc' XML document
    # Needs mapdata in its own class so that it's held in the inner mapdata block:
    #
    # <?xml version="1.0" ?>
    # <mapdoc>
    #    <mapdata>

    def __init__(self, mapdata):
        self.mapdata = mapdata

    def to_xml(self):
        mapDoc = Element('mapdoc')

        mapdata = SubElement(mapDoc, 'mapdata')

        versionNumber = SubElement(mapdata, 'versionNumber')
        versionNumber.text = str(self.mapdata.versionNumber)

        mapNumber = SubElement(mapdata, 'mapNumber')
        mapNumber.text = str(self.mapdata.mapNumber)

        operationID = SubElement(mapdata, 'operationID')
        operationID.text = str(self.mapdata.operationID)

        sourceOrg = SubElement(mapdata, 'sourceorg')
        sourceOrg.text = str(self.mapdata.sourceorg)

        title = SubElement(mapdata, 'title')
        title.text = str(self.mapdata.title)

        ref = SubElement(mapdata, 'ref')
        ref.text = str(self.mapdata.ref)

        language = SubElement(mapdata, 'language')
        language.text = str(self.mapdata.language)

        countries = SubElement(mapdata, 'countries')
        countries.text = str(self.mapdata.countries)

        createdate = SubElement(mapdata, 'createdate')
        createdate.text = str(self.mapdata.createdate)

        createtime = SubElement(mapdata, 'createtime')
        createtime.text = str(self.mapdata.createtime)

        status = SubElement(mapdata, 'status')
        status.text = str(self.mapdata.status)

        xmin = SubElement(mapdata, 'xmin')
        xmin.text = str(self.mapdata.xmin)

        ymin = SubElement(mapdata, 'ymin')
        ymin.text = str(self.mapdata.ymin)

        xmax = SubElement(mapdata, 'xmax')
        xmax.text = str(self.mapdata.xmax)

        ymax = SubElement(mapdata, 'ymax')
        ymax.text = str(self.mapdata.ymax)

        proj = SubElement(mapdata, 'proj')
        proj.text = str(self.mapdata.proj)

        datum = SubElement(mapdata, 'datum')
        datum.text = str(self.mapdata.datum)

        qclevel = SubElement(mapdata, 'qclevel')
        qclevel.text = str(self.mapdata.qclevel)

        qcname = SubElement(mapdata, 'qcname')
        qcname.text = str(self.mapdata.qcname)

        access = SubElement(mapdata, 'access')
        access.text = str(self.mapdata.access)

        glideno = SubElement(mapdata, 'glideno')
        glideno.text = str(self.mapdata.glideno)

        summary = SubElement(mapdata, 'summary')
        summary.text = str(self.mapdata.summary)

        imagerydate = SubElement(mapdata, 'imagerydate')
        imagerydate.text = str(self.mapdata.imagerydate)

        datasource = SubElement(mapdata, 'datasource')
        datasource.text = str(self.mapdata.datasource)

        location = SubElement(mapdata, 'location')
        location.text = str(self.mapdata.location)

        themes = SubElement(mapdata, 'themes')
        for setTheme in self.mapdata.themes:
            theme = SubElement(themes, 'theme')
            theme.text = setTheme

        scale = SubElement(mapdata, 'scale')
        scale.text = str(self.mapdata.scale)

        papersize = SubElement(mapdata, 'papersize')
        papersize.text = str(self.mapdata.papersize)

        jpgresolutiondpi = SubElement(mapdata, 'jpgresolutiondpi')
        jpgresolutiondpi.text = str(self.mapdata.jpgresolutiondpi)

        pdfresolutiondpi = SubElement(mapdata, 'pdfresolutiondpi')
        pdfresolutiondpi.text = str(self.mapdata.pdfresolutiondpi)

        kmlresolutiondpi = SubElement(mapdata, 'kmlresolutiondpi')
        kmlresolutiondpi.text = str(self.mapdata.kmlresolutiondpi)

        mxdfilename = SubElement(mapdata, 'mxdfilename')
        mxdfilename.text = str(self.mapdata.mxdfilename)

        paperxmax = SubElement(mapdata, 'paperxmax')
        paperxmax.text = str(self.mapdata.paperxmax)

        paperxmin = SubElement(mapdata, 'paperxmin')
        paperxmin.text = str(self.mapdata.paperxmin)

        paperymax = SubElement(mapdata, 'paperymax')
        paperymax.text = str(self.mapdata.paperymax)

        paperymin = SubElement(mapdata, 'paperymin')
        paperymin.text = str(self.mapdata.paperymin)

        accessnotes = SubElement(mapdata, 'accessnotes')
        accessnotes.text = str(self.mapdata.accessnotes)

        product_type = SubElement(mapdata, 'product-type')
        product_type.text = str(self.mapdata.product_type)

        language_iso2 = SubElement(mapdata, 'language-iso2')
        language_iso2.text = str(self.mapdata.language_iso2)

        jpgfilename = SubElement(mapdata, 'jpgfilename')
        jpgfilename.text = str(self.mapdata.jpgfilename)

        pdffilename = SubElement(mapdata, 'pdffilename')
        pdffilename.text = str(self.mapdata.pdffilename)

        jpgfilesize = SubElement(mapdata, 'jpgfilesize')
        jpgfilesize.text = str(self.mapdata.jpgfilesize)

        pdffilesize = SubElement(mapdata, 'pdffilesize')
        pdffilesize.text = str(self.mapdata.pdffilesize)

        dom = xml.dom.minidom.parseString(tostring(mapDoc, encoding='utf-8', method='xml'))
        return(dom.toprettyxml())
