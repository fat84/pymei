from lxml import etree #AH
from lxml import objectify #AH
import json
# import lxml #GVM

from pymei.Components import MeiAttribute, MeiElement, MeiDocument
from pymei.Components import Modules as mod

import types
import logging

lg = logging.getLogger('pymei')

def jsontomei(js, docname):
    """ Takes an incoming JSON stream and returns a MeiDocument object.
        
        Requires that you pass it a name.
    """
    
    jsn = json.loads(js)
    doc = MeiDocument.MeiDocument('jsonstream')
    j = _json_to_mei(jsn)
    doc.addelement(j)
    return doc

def _json_to_mei(el):
    """ Takes a JSON-structured MEI file and converts it to a set of nested Python
        MEI objects.
        
        See test/meijson.py for an example of how JSON-structured MEI looks.
    """
    lg.debug(el)
    
    # Strings are interpreted as values.
    if isinstance(el, types.StringType) or isinstance(el, types.UnicodeType):
        return el
    
    # attributes have a special attribute dictionary key.
    if isinstance(el, types.DictType) and "@attributes" in el.keys():
        return el
    
    if isinstance(el, types.DictType) and "@tail" in el.keys():
        return el
    
    if isinstance(el, types.DictType) and "@value" in el.keys():
        return el
        
    # don't pop from an empty dict!
    if len(el.keys()) < 1:
        return
    
    # convert the dict key name to an MEI object name.
    tagname = el.keys().pop()
    objname = "{0}_".format(tagname)
    obj = getattr(mod, objname)()
    
    # map this on to the object
    if isinstance(el[tagname], types.ListType):
        
        # loopdy-loopdy!
        m = map(_json_to_mei, el[tagname])
        lg.debug("M is {0}".format(m))
        # our map operation will return a number of things. Depending on what 
        # is in our map result, we put that it the MeiElement object accordingly.
        for d in m:
            if isinstance(d, types.DictType):
                lg.debug("Keys: {0}".format(d.keys()))
                
            if isinstance(d, types.DictType) and "@attributes" in d.keys():
                lg.debug("Setting Attributes")
                obj.setattributes(d['@attributes'])
            
            elif isinstance(d, types.DictType) and "@tail" in d.keys():
                lg.debug("Setting Tail Text {0}".format(d['@tail']))
                obj.settail(d['@tail'])
            
            elif isinstance(d, types.DictType) and "@value" in d.keys():
                lg.debug("Setting Value text {0}".format(d['@value']))
                obj.setvalue(d['@value'])
                
            else:
                obj.addchildren([d])
    lg.debug(obj)
    return obj