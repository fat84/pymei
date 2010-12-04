# helper functions to output to various representations.
import time

import types
from lxml import etree

from pymei import MEI_NS
from pymei.Helpers import prefix_to_ns

import logging
lg = logging.getLogger('pymei')

def meitoxml(meidocument, filename=None):
    """ Prints XML to the screen, or writes out an MeiDocument object to a file."""
    r = meidocument.gettoplevel()
    t1 = time.time()
    d = _mei_to_xml(r)
    t2 = time.time()
    lg.debug("Time taken: {0}".format(t2 - t1))
    
    d.set('xmlns', MEI_NS)
    t = etree.ElementTree(d)
    
    if not isinstance(filename, types.NoneType):
        t.write(filename, 
                pretty_print=True, 
                xml_declaration=True,
                encoding=meidocument.getencoding(),
                standalone=meidocument.getstandalone())
    else:
        print(etree.tostring(t, 
                pretty_print=True,
                xml_declaration=True,
                encoding=meidocument.getencoding(),
                standalone=meidocument.getstandalone()))

def _mei_to_xml(el):
    t1 = time.time()
    el_x = el.as_xml_object()
    if len(el.children) > 0:
        children = map(_mei_to_xml, el.children)
        
        for child in children:
            el_x.append(child)
    return el_x
    