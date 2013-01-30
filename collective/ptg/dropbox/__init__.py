from z3c.form import validator, error
import zope.interface
import zope.component

from zope.interface import Interface, Attribute
from collective.plonetruegallery.interfaces import \
    IGalleryAdapter, IBaseSettings
from collective.plonetruegallery.validators import \
    Data
from collective.plonetruegallery.utils import getGalleryAdapter
    
from zope.interface import implements
from collective.plonetruegallery.galleryadapters.base import BaseAdapter
from zope import schema

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.ptg.dropbox')



# Include the Dropbox SDK libraries
from dropbox import client, rest, session

# Might need some of these, not sure yet
import urllib2, urllib, commands, dircache, os, struct, time

import webbrowser
import pickle

import sys
import os
import time
import locale
from optparse import OptionParser

import re
import os.path

import logging

from urllib import urlencode, quote
import urllib2
import cookielib
#import keychain


# Get your app key and secret from the Dropbox developer website
APP_KEY = 'l8fqxygy25xq7jq'
APP_SECRET = 'otpc22qrc0gy7mc'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'


def add_condition():
    "no idea what to put here"
    return True
   

class IDropboxAdapter(IGalleryAdapter):
    """
    Nothing works here
    """

    dropbox = Attribute("returns a dropbox object for the ap key")


  
    def get_mini_photo_url(photo):
        """
        takes a photo and creates the thumbnail photo url
        https://api-content.dropbox.com/1/thumbnails/<root>/<path>
        I think this is 178x178 pixels
        xs 	32x32
        s	64x64
        m	128x128
        l	640x480
        xl	1024x768
        """

    def get_photo_link(photo):
        """
        creates the photo link url
        something like:
        https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h/Costa%20Rican%20Frog.jpg
        """

    def get_large_photo_url(photo):
        """
        create the large photo url
        """
        

 
     

class IDropboxGallerySettings(IBaseSettings):
    dropbox_username = schema.TextLine(
        title=_(u"label_dropbox_username", default=u"dropbox username"),
        description=_(u"description_dropbox_username",
            default=u"The username/id of your dropbox account. "
                    u"(*dropbox* gallery type)"
        ),
        required=False)
    dropbox_set = schema.TextLine(
        title=_(u"label_dropbox_set", default="Dropbox Set"),
        description=_(u"description_dropbox_set",
            default=u"Name/id of your dropbox set."
                    u"(*dropbox* gallery type)"
        ),
        required=False)

class DropboxAdapter(BaseAdapter):
    implements(IDropboxAdapter, IGalleryAdapter)
    
    urlbase = 'https://www.dropbox.com/'
    dlbase = 'https://dl-web.dropbox.com/'
    
    db_uid = None
    db_token = None




    schema = IDropboxGallerySettings
    name = u"dropbox"
    description = _(u"label_dropbox_gallery_type",
        default=u"Dropbox")

    sizes = {
        'small': {
            'width': 500,
            'height': 375
        },
        'medium': {
            'width': 640,
            'height': 480
        },
        'large': {
            'width': 1024,
            'height': 768
        },
        'thumb': {
            'width': 72,
            'height': 72
        },
        'dropbox': {
            'small': '_m',
            'medium': '',
            'large': '_b'
        }
    }
    
    def assemble_image_information(self, image):
        return {
            'image_url': self.get_large_photo_url(image),
            'thumb_url': self.get_mini_photo_url(image),
            'link': self.get_photo_link(image),
            'title': "image.get('title')",
            'description': "",
            'bodytext': ""
        }

 

    def get_mini_photo_url(self, photo):
        return "https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h/Costa%20Rican%20Frog.jpg"

    def get_photo_link(self, photo):
        return "https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h/Costa%20Rican%20Frog.jpg"

    def get_large_photo_url(self, photo):
        return "https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h/Costa%20Rican%20Frog.jpg"

    @property
    def dropbox(self):
        return  DropboxAPI(API_KEY)

    def retrieve_images(self):
        """list files in remote directory http://dl.dropbox.com/u/57194316/index.xml"""
        #access_token = self.get_access_token()
        sess = session.DropboxSession(APP_KEY,APP_SECRET, ACCESS_TYPE)
        #sess.set_token(access_token.key, access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        
        #resp = client.metadata('/')
        meta = dropbox_client.metadata('/')
        
        #path='https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h'
        
        filelist = []

        for item in meta['contents']:
			if item['is_dir']:
				filelist += self._listfiles(client,item['path'])
			else:
				filelist.append(item['path'])
            
        return filelist
        
        
    def get_request_token(self):
        #console.clear()
        sess = session.DropboxSession(APP_KEY,APP_SECRET, ACCESS_TYPE)
        request_token = None
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        #console.clear()
        webbrowser.open(url)
        import pdb; pdb.set_trace()
        return request_token
     
    def get_access_token(self):
        #token_str = keychain.get_password('dropbox', app_key)
        token_str = None
        if token_str:
            key, secret = pickle.loads(token_str)
            return session.OAuthToken(key, secret)
        request_token = self.get_request_token()
        sess = session.DropboxSession(APP_KEY,APP_SECRET, ACCESS_TYPE)
        access_token = sess.obtain_access_token(request_token)
        token_str = pickle.dumps((access_token.key, access_token.secret))
        #keychain.set_password('dropbox', app_key, token_str)
        return access_token
     
    def get_client(self):
        access_token = self.get_access_token()
        sess = session.DropboxSession(APP_KEY,APP_SECRET, ACCESS_TYPE)
        sess.set_token(access_token.key, access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        return dropbox_client
     
    def call(self):
        # Demo if started run as a script...
        # Just print the account info to verify that the authentication worked:
        #print 'Getting account info...'
        dropbox_client = get_client()
        account_info = dropbox_client.account_info()
        #print 'linked account:', account_info
        
        
    
    
    
    
    def theclient (self):
        sess = session.DropboxSession (APP_KEY,APP_SECRET, ACCESS_TYPE)
        sess = self.handle_oauth (sess)
        return client.DropboxClient (sess)
    
    def handle_oauth (self, sess):
        """ Retrieve OAUTH token & secret 
        or retrieve new ones if required.
    """
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)

        # This will fail if the user didn't visit
        # the above URL and hit 'Allow'
        #return sess.obtain_access_token(request_token)
        #return sess.obtain_access_token(url)  
        
        
        
        sess = session.DropboxSession(APP_KEY,APP_SECRET, ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        webbrowser.open(url)
        return request_token
        
        
        
        