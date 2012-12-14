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
import os, shutil, datetime, time, sys
from oauth import oauth
#import oauth.oauth as oauth
from datetime import datetime, timedelta



# Get your app key and secret from the Dropbox developer website
APP_KEY = 'l8fqxygy25xq7jq'
APP_SECRET = 'otpc22qrc0gy7mc'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'


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
        """list files in remote directory"""
        
        #sess = StoredSession('l8fqxygy25xq7jq', 'otpc22qrc0gy7mc', access_type='dropbox')
        sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        dir_sep = "/"
        
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        access_token = sess.obtain_access_token(request_token)
        
        resp = client.metadata(self.current_path)
        
        path='https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h'
        
        meta = client.metadata(path)
        filelist = []

        for item in meta['contents']:
			if item['is_dir']:
				filelist += self._listfiles(client,item['path'])
			else:
				filelist.append(item['path'])
            
        return filelist
        
        
    def get_request_token():
	    console.clear()
        print 'Getting request token...'	
        sess = session.DropboxSession(app_key, app_secret, access_type)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        console.clear()
        webbrowser.open(url, modal=True)
        return request_token
     
    def get_access_token():
        token_str = keychain.get_password('dropbox', app_key)
        if token_str:
            key, secret = pickle.loads(token_str)
            return session.OAuthToken(key, secret)
        request_token = get_request_token()
        sess = session.DropboxSession(app_key, app_secret, access_type)
        access_token = sess.obtain_access_token(request_token)
        token_str = pickle.dumps((access_token.key, access_token.secret))
        keychain.set_password('dropbox', app_key, token_str)
        return access_token
     
    def get_client():
        access_token = get_access_token()
        sess = session.DropboxSession(app_key, app_secret, access_type)
        sess.set_token(access_token.key, access_token.secret)
        dropbox_client = client.DropboxClient(sess)
        return dropbox_client
     
    def call(self):
        # Demo if started run as a script...
        # Just print the account info to verify that the authentication worked:
        print 'Getting account info...'
        dropbox_client = get_client()
        account_info = dropbox_client.account_info()
        print 'linked account:', account_info
     
            
    
            
     
