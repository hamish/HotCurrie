from tipfy import (RequestHandler, RequestRedirect, Response, abort,
    cached_property, redirect, redirect_to, url_for)

import logging
import urllib

from google.appengine.api import urlfetch
from google.appengine.api import mail

from apps.stonewareglazes.handlers import BaseHandler, AdminUserHandler
from apps.stonewareglazes.Model import IndexItem, Page, TocItem

class PaymentCompleteHandler(BaseHandler):
    def get(self, **kwargs):
        return self.render_response('thanks.html')
 

class PaypalIPNHandler(AdminUserHandler):
    live_url = "https://www.paypal.com/cgi-bin/webscr"
    test_url = 'https://www.sandbox.paypal.com/cgi-bin/webscr'

    def post(self):
        self.get()
    def get(self):
        self.process_ipn(1)
        return Response('ipn processing complete')

    def process_ipn(self, do_paypal_verification):
        logging.info("process_IPN")

        data = {}
        for i in self.request.args.keys():
            data[i] = self.request.args.get(i)
            logging.info("IPN GET data: %s: %s" %(i, data[i]))
        for i in self.request.form.keys():
            data[i] = self.request.form.get(i)
            logging.info("IPN POST data: %s: %s" %(i, data[i]))
         

        ipn_verified = True
        if do_paypal_verification:
            ipn_verified = self.is_ipn_valid(data)
        else:
            ipn_verified = (self.request.args.get('paypal_verification') == 'Success')
            
        verified = ipn_verified
        message="Thank you for opening an account with Stoneware Glazes online. "
            
        if verified:
            # create user account
            user = self.createUser(data['payer_email'], message)
            mail.send_mail(to='hcurrie@gmail.com', 
            	    sender='hcurrie@gmail.com', 
            	    subject='Stoneware glazes online payment', 
            	    body="There was a payment.\n\nData:\n%s\n" % dict_to_string(data))
            
        else:
            # what to do? email admin?
            mail.send_mail(to='hcurrie@gmail.com', 
            	    sender='hcurrie@gmail.com', 
            	    subject='Stoneware glazes online payment verification failure', 
            	    body="There was an attempted payment verification which was denied by paypal.\n\nData:\n%s\n" % dict_to_string(data))

    def get_verification_url(self, data):
        verification_url = self.live_url
        if (self.request.args.get('test_ipn', '0') == '1'):
            verification_url = self.test_url
        data['verification+url'] = verification_url
        return verification_url
        
    def is_ipn_valid(self, data):
        data['cmd'] = '_notify-validate'
            
        verification_url = self.get_verification_url(data)
        result = self.do_post(verification_url, data)
        data['ipn+post+result'] = result
        ipn_verified = (result == 'VERIFIED')
        return ipn_verified
    

    def do_post(self, url, args):
        return urlfetch.fetch(
            url = url,
            method = urlfetch.POST,
            payload = urllib.urlencode(args)
        ).content

    def verify(self, data):
        verify_url = self.live_url
        if (data.get('test_ipn', '0')=='1'):
            verify_url = self.test_url
        args = {
            'cmd': '_notify-validate',
        }
        args.update(data)
        result = self.do_post(verify_url, args)
        r = {'post_result': result }
        r.update(data)
        return result == 'VERIFIED'
def dict_to_string(dict):
    s=""
    for key in dict.keys():
        s="%s %s : %s \n" %(s,key,dict[key])
    return s
