import re
import datetime

from django.utils.safestring import mark_safe
from django.db import models

from eulexistdb.manager import Manager
from eulexistdb.models import XmlModel
from eulxml.xmlmap.core import XmlObject 
#from eulxml.xmlmap.dc import DublinCore
from eulxml.xmlmap.fields import StringField, NodeField, StringListField, NodeListField, IntegerField
from eulxml.xmlmap.teimap import Tei, TeiDiv, _TeiBase, TEI_NAMESPACE, xmlmap, TeiInterpGroup, TeiInterp


class Fields(_TeiBase):
    ROOT_NAMESPACES = {
        'tei' : TEI_NAMESPACE,
        'xml' : 'http://www.w3.org/XML/1998/namespace'}
    id = StringField('@xml:id')
    head = StringField('tei:head')
    author = StringField("tei:byline//tei:sic")
    type = StringField("@type") 
    num = StringField("@n")
    pages = StringField("tei:docDate")
    head = StringField('tei:head')
    ana = StringField("@ana")


class Issue(XmlModel):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('/tei:TEI')
    id = StringField('@xml:id')
    divs = NodeListField('//tei:div2', Fields)
    pids = NodeListField('//tei:idno', Fields)
    date = StringField('//tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:date/@when')
    head = StringField('//tei:div1/tei:head')
    year = StringField('//tei:div1/tei:p/tei:date')

    source = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl')
    issued_date = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:date')
    created_date = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:date/@when')
    author = StringField('tei:teiHeader/tei:fileDesc/tei:sourceDesc/tei:bibl/tei:publisher')
    identifier_ark = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:idno[@type="ark"]')
    title = StringField('tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title')
    publisher = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:publisher')
    rights = StringField('tei:teiHeader/tei:fileDesc/tei:publicationStmt/tei:availability/tei:p')
    series = StringField('tei:teiHeader/tei:fileDesc/tei:seriesStmt/tei:title')
    project_desc = StringField('tei:teiHeader/tei:encodingDesc/tei:projectDesc')


class Article(XmlModel):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager("//tei:div2")
    article = NodeField("//tei:div2", "self")
    id = NodeField('@xml:id', 'self')
    pid = NodeField('ancestor::tei:TEI//tei:idno[@n=%s]' % 'self', Issue)
    date = StringField('tei:docDate/@when')
    head = StringField('tei:head')
    author = StringField("tei:byline//tei:sic")
    type = StringField("@type")
    pages = StringField("tei:docDate")
    ana = StringField("@ana", "self") 

    # TODO: DRY this out
    issue = NodeField('ancestor::tei:TEI', Issue)
    issue_id = NodeField('ancestor::tei:TEI/@xml:id', Issue)
    issue_title = NodeField('ancestor::tei:TEI//tei:div1/tei:head', Issue)
    next_id = NodeField("following::tei:div2[1]/@xml:id", "self")
    next_title = NodeField("following::tei:div2[1]/tei:head", "self")  
    previous_id = NodeField("preceding::tei:div2[1]/@xml:id", "self")
    previous_title = NodeField("preceding::tei:div2[1]/tei:head", "self")


class ArticlePid(XmlModel):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager("//tei:idno") 
    id = NodeField('@n', 'self')
    pid = StringField("//tei:idno", "self")
    

class Topic(XmlModel):
    objects = Manager("//interp")
    id = StringField('@xml:id')
    name = StringField("//interp", "self")

    
class TopicArticle(XmlModel):
    ROOT_NAMESPACES = {'tei' : TEI_NAMESPACE}
    objects = Manager('//tei:certainty')

    interp = NodeField('ancestor::tei:interp', Topic)
    degree = StringField("@degree")
    topic_id = StringField("@ana")
    
    # TODO: DRY this out
    date = NodeField('ancestor::tei:TEI//tei:div1/tei:p[1]/tei:date', Issue)
    issue_id = NodeField('ancestor::tei:TEI/@xml:id', Issue)
    article_id = NodeField('ancestor::tei:div2/@xml:id', Article)
    article_title = NodeField('ancestor::tei:div2//tei:head', Article)
    article_author = NodeField('ancestor::tei:div2//tei:byline//tei:sic', Article)
    article_type = NodeField('ancestor::tei:div2/@type', Article)



   
