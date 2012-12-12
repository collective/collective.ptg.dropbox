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

# XXX Fill in your consumer key and secret below
# You can find these at http://www.dropbox.com/developers/apps
APP_KEY = ' '
APP_SECRET = ' '
ACCESS_TYPE = 'app_folder'  # should be 'dropbox' or 'app_folder' as configured for your app




#import cmd
#import locale
#import os
#import pprint
#import shlex

from dropbox import client, rest, session


def add_condition():
    return True
   

class IDropboxAdapter(IGalleryAdapter):
    """
    Nothing works here
    """

    dropbox = Attribute("returns a dropbox object for the ap key")


 

    def get_mini_photo_url(photo):
        """
        takes a photo and creates the thumbnail photo url
        I think this is 178x178 pixels
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
        try:
            images = [self.assemble_image_information(i)
                for i in ['1', '2', 'need to get images from dropbox']]
            print images
            return images
        except Exception, inst:
            self.log_error(Exception, inst, "Error getting all images")
            return []
            