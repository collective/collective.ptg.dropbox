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


# Get your app key and secret from the Dropbox developer website
APP_KEY = 'l 
APP_SECRET = 'otpc2 '

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
        
        #self.sess = StoredSession('l8fqxygy25xq7jq', 'otpc22qrc0gy7mc', access_type='dropbox')
        #self.api_client = self.client.DropboxClient(self.sess)
        #self.current_path = ''
        #self.prompt = "Dropbox> "

        #self.sess.load_creds()
        
        path='https://dl.dropbox.com/sh/1294vo0qreb8iad/tZIay8d54h'
        resp = 'list(path)'
        
        myfiles = ['1', '2']
        if 'contents' in resp:
            for f in resp['contents']:
                #name = os.path.basename(f['path'])
                #encoding = locale.getdefaultlocale()[1]
                #self.stdout.write(('%s\n' % name).encode(encoding))
                name = f['path']
                myfiles.append(name)
 
        import pdb; pdb.set_trace()
        try:
            images = [self.assemble_image_information(i)
                for i in myfiles]
            return images
        except Exception, inst:
            self.log_error(Exception, inst, "Error getting all images")
            return []
            
    def do_ls(self):
        """list files in remote directory"""
        
        self.sess = StoredSession('l8fqxygy25xq7jq', 'otpc22qrc0gy7mc', access_type='dropbox')
        self.api_client = client.DropboxClient(self.sess)
        self.current_path = ''
        self.prompt = "Dropbox> "

        self.sess.load_creds()
        
        
        resp = self.api_client.metadata(self.current_path)
        
        myfiles = ['1', '2']
        if 'contents' in resp:
            for f in resp['contents']:
                #name = os.path.basename(f['path'])
                #encoding = locale.getdefaultlocale()[1]
                #self.stdout.write(('%s\n' % name).encode(encoding))
                name = f['path']
                myfiles.append(name)
        return myfiles
        
        
        
        
        
        
        
        
        
        
        
        
        
class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""
    TOKEN_FILE = "token_store.txt"

    def load_creds(self):
        try:
            stored_creds = open(self.TOKEN_FILE).read()
            self.set_token(*stored_creds.split('|'))
            print "[loaded access token]"
        except IOError:
            pass # don't worry if it's not there

    def write_creds(self, token):
        f = open(self.TOKEN_FILE, 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def delete_creds(self):
        os.unlink(self.TOKEN_FILE)

    def link(self):
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()

        self.obtain_access_token(request_token)
        self.write_creds(self.token)

    def unlink(self):
        self.delete_creds()
        session.DropboxSession.unlink(self)
