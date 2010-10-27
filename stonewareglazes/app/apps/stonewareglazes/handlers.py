from django.utils import simplejson

from tipfy import (RequestHandler, RequestRedirect, Response, abort,
    cached_property, redirect, url_for)
from tipfy.ext.auth import MultiAuthMixin, login_required, user_required
from tipfy.ext.auth.facebook import FacebookMixin
from tipfy.ext.auth.friendfeed import FriendFeedMixin
from tipfy.ext.auth.google import GoogleMixin
from tipfy.ext.auth.twitter import TwitterMixin
from tipfy.ext.jinja2 import Jinja2Mixin
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.wtforms import Form, fields, validators

from google.appengine.api import users
from google.appengine.api import mail
import random
import string

REQUIRED = validators.required()
EMAIL = validators.email()

PASSWORD_SEED= string.letters[:26]+string.digits[1:]+'!@#$%^&*'
class LoginForm(Form):
    username = fields.TextField('Username', validators=[REQUIRED, EMAIL])
    password = fields.PasswordField('Password', validators=[REQUIRED])
    remember = fields.BooleanField('Keep me signed in')

class RegistrationForm(Form):
    username = fields.TextField('Username', validators=[REQUIRED, EMAIL])
    message = fields.TextAreaField('Message')


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
        return self.render_response('admin.html', form=self.form)

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

class PaypalHandler(AdminHandler):
    def post(self, **kwargs):
        username=self.request.get('payer_email')
        message="Thanks for your payment"
        
        
        ### TODO DO Verification checks
        user = self.createUser(username, message)

        
