from django.utils import simplejson

from tipfy import (RequestHandler, RequestRedirect, Response, abort,
    cached_property, redirect, redirect_to, url_for)
from tipfy.ext.auth import MultiAuthMixin, login_required, user_required
from tipfy.ext.blobstore import BlobstoreDownloadMixin, BlobstoreUploadMixin

from tipfy.ext.auth.facebook import FacebookMixin
from tipfy.ext.auth.friendfeed import FriendFeedMixin
from tipfy.ext.auth.google import GoogleMixin
from tipfy.ext.auth.twitter import TwitterMixin
from tipfy.ext.jinja2 import Jinja2Mixin
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.wtforms import Form, fields, validators

from apps.stonewareglazes.Model import Page, IndexItem, TocItem
from apps.stonewareglazes.roman import toRoman, fromRoman

from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.api import images 
from google.appengine.api import urlfetch

import random
import string
import csv
import logging
import urllib

REQUIRED = validators.required()
EMAIL = validators.email()

PASSWORD_SEED= string.letters[:26]+string.digits[1:]+'!@#$%^&*'
IMG_SERVING_SIZES = [
              32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128, 144,
              150, 160, 200, 220, 288, 320, 400, 512, 576, 640, 720,
              800, 912, 1024, 1152, 1280, 1440, 1600]
 
class LoginForm(Form):
    username = fields.TextField('Username', validators=[REQUIRED, EMAIL])
    password = fields.PasswordField('Password', validators=[REQUIRED])
    remember = fields.BooleanField('Keep me signed in')

class RegistrationForm(Form):
    username = fields.TextField('Username', validators=[REQUIRED, EMAIL])
    message = fields.TextAreaField('Message')
class IndexForm(Form):
    label = fields.TextField('Label', validators=[REQUIRED])
    pagenumbers = fields.TextField('Page Numbers', validators=[REQUIRED])

class BaseHandler(RequestHandler, MultiAuthMixin, Jinja2Mixin,
    AllSessionMixins):
    middleware = [SessionMiddleware]

    def render_response(self, filename, **kwargs):
        auth_session = None
        if 'id' in self.auth_session:
            auth_session = self.auth_session



        self.request.context.update({
            'auth_session': auth_session,
            'current_user': self.auth_current_user,
            'login_url':    self.auth_login_url(),
            'logout_url':   self.auth_logout_url(),
            'current_url':  self.request.url,
        })
        user = users.get_current_user()
        if user:
            self.request.context['goolge_user'] = 1
            self.request.context['goolge_logout_url'] = users.create_logout_url('/')
            
        if self.messages:
            self.request.context['messages'] = simplejson.dumps(self.messages)

        return super(BaseHandler, self).render_response(filename, **kwargs)

    def redirect_path(self, default='/'):
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = self.request.args.get('continue', '/')

        if not url.startswith('/'):
            url = default

        return url

    def _on_auth_redirect(self):
        """Redirects after successful authentication using third party
        services.
        """
        if '_continue' in self.session:
            url = self.session.pop('_continue')
        else:
            url = '/'

        if not self.auth_current_user:
            url = self.auth_signup_url()

        return redirect(url)


class HomeHandler(BaseHandler):
    def get(self, **kwargs):
        return self.render_response('home.html', section='home')
        
       
class ContentHandler(BaseHandler):
    @user_required
    def get(self, **kwargs):
        return self.render_response('content.html', section='content')

class PageListHandler(BaseHandler):
    def getPages(self):
        pages = Page.gql('ORDER BY sequenceNumber')
        processedPages=[]
        for page in pages:
            p={
               'url': url_for('page_def', number=page.pageLabel),
               'name': 'Page %s' % (page.pageLabel),
               }
            processedPages.append(p)
        return processedPages

class BookHandler(PageListHandler):
    def get(self):
        processedPages = self.getPages()
        arguments={'pages': self.getPages()}            
        return self.render_response('Book.html', **arguments)

class IndexListHandler(BaseHandler):
    def getIndexItems(self):
        items = IndexItem.gql('ORDER BY sequenceNumber')
        processedItems=[]
        for item in items:
            reader = csv.reader([item.pageNumbers.strip()], skipinitialspace=True)
            pageNumberList= list(reader)[0]
            p={
               'label': item.label,
               'pages': pageNumberList
               }
            processedItems.append(p)
        return processedItems

class IndexHandler(IndexListHandler):
    def get(self, **kwargs):
        context = {
            'indexItems': self.getIndexItems()
        }
        return self.render_response('book-index.html', **context)

class TocHandler(BaseHandler):
    def get(self):
        context={
            'tocItems': TocItem.gql('ORDER BY sequenceNumber'),
                 }
        return self.render_response('toc.html', **context)

class AdminIndexHandler(IndexListHandler):
    @cached_property
    def form(self):
        return IndexForm(self.request)    

    
    def get(self, **kwargs):
        Items = IndexItem.gql('ORDER BY label')
        context = {
            'form':       self.form,
            'indexItems': self.getIndexItems()
        }
        return self.render_response('admin-index.html', **context)
    def post(self, **kwargs):

        if self.form.validate():
            label = self.form.label.data
            pagenumbers = self.form.pagenumbers.data
            #reader = csv.reader([pagenumbers], skipinitialspace=True)
            #pageNumberList= list(reader)[0]
            item= IndexItem()
            item.label=label
            item.pageNumbers=pagenumbers
            item.put()
            return self.get(**kwargs)


        self.set_message('error', 'Authentication failed. Please try again.',
            life=None)
        return self.get(**kwargs)
    
PAYPAL_ID = "ian-paypal@currie.to"
ITEM_NAME = "Account for online access to Stoneware Glazes"
class PaymentHandler(BaseHandler):
    def get(self, **kwargs):
        domain='htp://localhost:8080/'
        priceInDollars=self.request.args.get('amount', 5, type=int)
        parameters = {
            "business": "%s" % PAYPAL_ID,
            "cmd": "_xclick",
            "item_name": "%s" % ITEM_NAME,
            "custom": "%s" % "AccountSignup",
            "amount": "%s" % priceInDollars,
            "currency_code": "AUD",
            "no_shipping": "1",
            "rm": "1",
            "return": "%s%s" % (domain, '/thanks/'),
            "cancel_return": "%s%s" % (domain, url_for('auth/login')),
            "bn": "StonewareGlazes_Online",
            "notify_url": "%s%s" % (domain, "/purchase/ipn/")
        }
        parameters_encoded = urllib.urlencode(parameters)
        paypal_url = "https://www.paypal.com/cgi-bin/webscr?"
        payment_link = paypal_url + parameters_encoded
        logging.info("redirect to:" + payment_link)
        return redirect(payment_link)

class LoginHandler(BaseHandler):
    def get(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(redirect_url)

        opts = {'continue': self.redirect_path()}
        context = {
            'form':                 self.form,

        }
        return self.render_response('login.html', **context)

    def post(self, **kwargs):
        redirect_url = self.redirect_path()

        if self.auth_current_user:
            # User is already registered, so don't display the signup form.
            return redirect(redirect_url)

        if self.form.validate():
            username = self.form.username.data
            password = self.form.password.data
            remember = self.form.remember.data

            res = self.auth_login_with_form(username, password, remember)
            if res:
                return redirect(redirect_url)

        self.set_message('error', 'Authentication failed. Please try again.',
            life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return LoginForm(self.request)


class LogoutHandler(BaseHandler):
    def get(self, **kwargs):
        self.auth_logout()
        return redirect(self.redirect_path())

class AdminHandler(BaseHandler):
    def get(self, **kwargs):
        upload_url = blobstore.create_upload_url(url_for('blobstore/upload'))

        return self.render_response('admin.html', upload_url=upload_url)
class AdminUserHandler(BaseHandler):
    def get(self, **kwargs):
        upload_url = blobstore.create_upload_url(url_for('blobstore/upload'))

        return self.render_response('admin-user.html', form=self.form, upload_url=upload_url)

    def createUser(self, username, message):
        auth_id = 'own|%s' % username
        password="".join( [random.choice(PASSWORD_SEED) for i in xrange(8)] )

        user = self.auth_create_user(username, auth_id, password=password)
        body=''
        if message:
            body += "%s\n" %message
        body += "Your details are:\n"
        body += "Username: %s\n" %username
        body += "Password: %s\n" %password
        body += "\n\nBest regards\nIan Currie\n" 
        message = mail.EmailMessage(sender="hcurrie@gmail.com",
        	to=username,
        	subject="Stoneware Glazes Subscription",
        	body=body)
        message.send()
        return user

    def post(self, **kwargs):
        redirect_url = self.redirect_path()


        if self.form.validate():
            username = self.form.username.data
            message = self.form.message.data

            user = self.createUser(username, message)
            if user:
                self.set_message('success', 'User has been registered.', flash=True, life=5)
                self.form.username.data=''
                self.form.message.data=''
                
            else:
                self.set_message('error', 'This username is already '
                    'registered.', life=None)
            return self.get(**kwargs)

        self.set_message('error', 'A problem occurred. Please correct the '
            'errors listed in the form.', life=None)
        return self.get(**kwargs)

    @cached_property
    def form(self):
        return RegistrationForm(self.request)

def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]

def getPageLabel(pageSequence):
    label = toRoman(pageSequence+1)
    if (pageSequence >= 14):
        label= str(pageSequence-13)
    return label

class UploadHandler(BaseHandler, BlobstoreUploadMixin):
    def post(self):
        # 'file' is the name of the file upload field in the form.
        logging.debug("UploadHandler")

        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        seqNum = int(blob_info.filename[17:20])
        label = getPageLabel(seqNum)
        #Save entry to datastore
        logging.debug("creating Page")

        page = Page()
        page.blobKey=str(blob_info.key())
        #page.name = upload_files
        page.sequenceNumber = seqNum
        page.pageLabel = label
        page.put()
        logging.debug("redirecting")

        response = redirect_to('admin')
        #response = redirect_to('blobstore/serve', resource=blob_info.key())
        # Clear the response body.
        response.data = ''
        return response

class PageHandler(BaseHandler, BlobstoreDownloadMixin):
    #def get(self, **kwargs):
    def get(self, number='1', size='24'):
        pageLabel=number
        sizeIndex=int(size)
        #pageLabel = kwargs.get('number')
        pages = Page.gql("WHERE pageLabel=:1", pageLabel)
        page = pages.get()
        
        #if (page.loginRequired):
        #    logging.debug("loginRequired:")
        #    if not self.auth_current_user:
        #        logging.debug("failed:")
        #        return redirect(self.auth_login_url())
        url = images.get_serving_url(page.blobKey, size=IMG_SERVING_SIZES[sizeIndex], crop=False)
        
        if (containsAny(pageLabel, '0123456789')):
            pageSequence = int(pageLabel)+ 13
        else:
            pageSequence = fromRoman(pageLabel)-1

        arguments={
            'pageImageURL':url,
        }
        
        if(pageSequence>0):
            prevLabel = getPageLabel(pageSequence - 1)
            arguments['hasPrevious']=1
            arguments['previousURL']=url_for('page', number=prevLabel, size=size)
        if (pageSequence<223):
            nextLabel = getPageLabel(pageSequence + 1)
            arguments['hasNext']=1
            arguments['nextURL']=url_for('page', number=nextLabel, size=size)

        if(sizeIndex>0):
            sizeStr=str(sizeIndex-1)
            arguments['hasSmaller']=1
            arguments['smallerURL']=url_for('page', number=number, size=sizeStr)
        if(sizeIndex<29):
            sizeStr=str(sizeIndex+1)
            arguments['hasBigger']=1
            arguments['biggerURL']=url_for('page', number=number, size=sizeStr)
        
        return self.render_response('Page.html', **arguments)



