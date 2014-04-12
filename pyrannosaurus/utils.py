import base64
from lxml import etree

NS = "http://soap.sforce.com/2006/04/metadata"
NS_FULL = "{http://soap.sforce.com/2006/04/metadata}"
NAMESPACES = {"sf": NS}

def package_to_dict(file_path):
    parser = etree.XMLParser(remove_blank_text=True)
    meta_types = {}
    pkg_manifest = etree.parse(file_path,parser)
    root = pkg_manifest.getroot()
    #loop through each type node in the package
    for item in root.xpath("sf:types",namespaces=NAMESPACES):
        #get the meta name and create it in  the new package if it doesn't exist, using asterisk wildcard
        meta_name = item.xpath("sf:name/text()", namespaces=NAMESPACES)[0]
        meta_types[meta_name] = []
        for mem in item.xpath("sf:members/text()", namespaces=NAMESPACES):
            meta_types[meta_name].append(mem)

    return meta_types

def zip_to_fs(zip_response):
    ''' Handle the SF Metadata API checkRetrieveStatus zip file response ''' 

    decoded_file = base64.b64decode(zip_response.zipFile)
    zip_file = open('retrieve.zip', 'w')
    zip_file.write(decoded_file)
    zip_file.close()