# -*- coding: utf-8 -*-
"""
    tipfy.ext.auth.model
    ~~~~~~~~~~~~~~~~~~~~

    Model for Stoneware glazes pages.
    
    :copyright: 2010 by Hamish Currie.
"""
from google.appengine.ext import db

from tipfy import get_config

class Page(db.Model):
    #: Creation date.
    created = db.DateTimeProperty(auto_now_add=True)
    #: Modification date.
    updated = db.DateTimeProperty(auto_now=True)
    # Blobstore key
    blobKey = db.StringProperty()
    # Sequence number to sort the pages in order.
    sequenceNumber = db.IntegerProperty()
    # can be a Roman numeral or a number
    pageLabel = db.StringProperty()
