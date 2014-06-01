from collections import defaultdict
from xml.etree import ElementTree as ET

# Code snippet from K3---rnc for the conversion of XML to the python dictionary format.
# http://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary-in-python/10077069#10077069
def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d
                
def xml_to_dict(xmlstring, encoding = None):
    if encoding != None:
        xparser = ET.XMLParser(encoding = encoding)
    else:
        xparser = None
    tree = ET.XML(xmlstring, xparser)
    xmldict = etree_to_dict(tree)
    
    return xmldict