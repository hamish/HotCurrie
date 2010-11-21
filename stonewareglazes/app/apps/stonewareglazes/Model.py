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
    # does the user need to be logged in to view this page
    loginRequired = db.BooleanProperty()

class IndexItem(db.Model):
    #: Creation date.
    created = db.DateTimeProperty(auto_now_add=True)
    #: Modification date.
    updated = db.DateTimeProperty(auto_now=True)
    label = db.StringProperty()
    pageNumbers = db.StringProperty()
    sequenceNumber = db.IntegerProperty()

class TocItem(db.Model):
    #: Creation date.
    created = db.DateTimeProperty(auto_now_add=True)
    #: Modification date.
    updated = db.DateTimeProperty(auto_now=True)
    label = db.StringProperty()
    pageNumber = db.StringProperty()
    styleNumber = db.IntegerProperty()
    blockHeading = db.StringProperty()
    sequenceNumber = db.IntegerProperty()
    