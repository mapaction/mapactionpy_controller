# flake8: noqa
case1_export_metadata_dict = {
    'versionNumber': '05',
    'mapNumber': 'MA9001',
    'operationID': 'ken',
    'sourceorg': 'MapAction',
    'title': 'Country Overview with Admin 1 Boundaries and Topography',
    'ref': 'MA9001-v05-country-overview-with-admin-1-boundaries-and-topography.mxd',
    'language': 'English',
    'countries': 'Kenya',
    'createdate': '2021-05-05 09:05:38',
    'createtime': '21:05',
    'status': 'Update',
    'xmax': '42.58',
    'xmin': '33.24',
    'ymax': '5.91',
    'ymin': '-5.17',
    'proj': '',
    'datum': 'WGS 1984',
    'qclevel': '',
    'qcname': '',
    'access': 'Public',
    'glideno': 'n/a',
    'summary': 'Country overview with topography displayed',
    'imagerydate': '',
    'datasource': 'Data Sources:',
    'location': '',
    'themes': ['reference-map'],
    'scale': '1: 3,816,422',
    'papersize': 'A3',
    'jpgresolutiondpi': '300',
    'pdfresolutiondpi': '300',
    'kmlresolutiondpi': '50',
    'mapfilename': 'MA9001-v05-country-overview-with-admin-1-boundaries-and-topography.mxd',
    'paperxmax': '',
    'paperxmin': '',
    'paperymax': '',
    'paperymin': '',
    'accessnotes': '',
    'product-type': 'mapsheet',
    'language-iso2': 'en',
    'jpgfilename': 'MA9001-v05-country-overview-with-admin-1-boundaries-and-topography-300dpi.jpeg',
    'pdffilename': 'MA9001-v05-country-overview-with-admin-1-boundaries-and-topography-300dpi.pdf',
    'jpgfilesize': '2118804',
    'pdffilesize': '1411100'
}

case1_expected_xml_output = r"""<?xml version="1.0" encoding="utf-8"?>
<mapdoc>
  <mapdata>
    <access>Public</access>
    <accessnotes></accessnotes>
    <countries>Kenya</countries>
    <createdate>2021-05-05 09:05:38</createdate>
    <createtime>21:05</createtime>
    <datasource>Data Sources:</datasource>
    <datum>WGS 1984</datum>
    <glideno>n/a</glideno>
    <imagerydate></imagerydate>
    <jpgfilename>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography-300dpi.jpeg</jpgfilename>
    <jpgfilesize>2118804</jpgfilesize>
    <jpgresolutiondpi>300</jpgresolutiondpi>
    <kmlresolutiondpi>50</kmlresolutiondpi>
    <language>English</language>
    <language-iso2>en</language-iso2>
    <location></location>
    <mapNumber>MA9001</mapNumber>
    <mapfilename>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography.mxd</mapfilename>
    <operationID>ken</operationID>
    <papersize>A3</papersize>
    <paperxmax></paperxmax>
    <paperxmin></paperxmin>
    <paperymax></paperymax>
    <paperymin></paperymin>
    <pdffilename>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography-300dpi.pdf</pdffilename>
    <pdffilesize>1411100</pdffilesize>
    <pdfresolutiondpi>300</pdfresolutiondpi>
    <product-type>mapsheet</product-type>
    <proj></proj>
    <qclevel></qclevel>
    <qcname></qcname>
    <ref>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography.mxd</ref>
    <scale>1: 3,816,422</scale>
    <sourceorg>MapAction</sourceorg>
    <status>Update</status>
    <summary>Country overview with topography displayed</summary>
    <themes>
      <theme>reference-map</theme>
    </themes>
    <title>Country Overview with Admin 1 Boundaries and Topography</title>
    <versionNumber>05</versionNumber>
    <xmax>42.58</xmax>
    <xmin>33.24</xmin>
    <ymax>5.91</ymax>
    <ymin>-5.17</ymin>
  </mapdata>
</mapdoc>
"""


case3_expected_xml_output = r"""<?xml version="1.0" encoding="utf-8"?>
<mapdoc>
  <mapdata>
    <versionNumber>05</versionNumber>
    <mapNumber>MA9001</mapNumber>
    <operationID>ken</operationID>
    <sourceorg>MapAction</sourceorg>
    <title>Country Overview with Admin 1 Boundaries and Topography</title>
    <ref>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography.mxd</ref>
    <language>English</language>
    <countries>Kenya</countries>
    <createdate>2021-05-05 09:05:38</createdate>
    <createtime>21:05</createtime>
    <status>Update</status>
    <xmax>42.58</xmax>
    <xmin>33.24</xmin>
    <ymax>5.91</ymax>
    <ymin>-5.17</ymin>
    <proj></proj>
    <datum>WGS 1984</datum>
    <qclevel></qclevel>
    <qcname></qcname>
    <access>Public</access>
    <glideno>n/a</glideno>
    <summary>Country overview with topography displayed</summary>
    <imagerydate></imagerydate>
    <datasource>Data Sources:</datasource>
    <location></location>
    <themes>
      <theme>my_broken_theme</theme>
    </themes>
    <scale>1: 3,816,422</scale>
    <papersize>A3</papersize>
    <jpgresolutiondpi>300</jpgresolutiondpi>
    <pdfresolutiondpi>300</pdfresolutiondpi>
    <kmlresolutiondpi>50</kmlresolutiondpi>
    <mapfilename>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography.mxd</mapfilename>
    <paperxmax></paperxmax>
    <paperxmin></paperxmin>
    <paperymax></paperymax>
    <paperymin></paperymin>
    <accessnotes></accessnotes>
    <product-type>mapsheet</product-type>
    <language-iso2>en</language-iso2>
    <jpgfilename>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography-300dpi.jpeg</jpgfilename>
    <pdffilename>MA9001-v05-country-overview-with-admin-1-boundaries-and-topography-300dpi.pdf</pdffilename>
    <jpgfilesize>2118804</jpgfilesize>
    <pdffilesize>1411100</pdffilesize>
  </mapdata>
</mapdoc>
"""
