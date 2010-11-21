# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule, import_string, HandlerPrefix


def get_rules(app):
    """Returns a list of URL rules for the application. The list can be
    defined entirely here or in separate ``urls.py`` files.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        HandlerPrefix('apps.stonewareglazes.', [
            Rule('/', endpoint='home', handler='handlers.HomeHandler'),
            Rule('/auth/login', endpoint='auth/login', handler='handlers.LoginHandler'),
            Rule('/auth/logout', endpoint='auth/logout', handler='handlers.LogoutHandler'),
            Rule('/auth/signup', endpoint='auth/signup', handler='handlers.SignupHandler'),
            Rule('/auth/register', endpoint='auth/register', handler='handlers.RegisterHandler'),
            Rule('/auth/pay', endpoint='auth/pay', handler='handlers.PaymentHandler'),


            Rule('/content', endpoint='content/index', handler='handlers.ContentHandler'),
            Rule('/admin', endpoint='admin', handler='handlers.AdminHandler'),
            Rule('/admin/user', endpoint='admin-user', handler='handlers.AdminUserHandler'),
            Rule('/admin/index', endpoint='admin-index', handler='handlers.AdminIndexHandler'),
            Rule('/admin/load/index', endpoint='admin-load-index', handler='dataloader.LoadIndexHandler'),
            Rule('/admin/load/toc', endpoint='admin-load-toc', handler='dataloader.LoadTocHandler'),
            #Rule('/admin/load/index', endoint='admin-load-index', handler='handlers.LoadIndexHandler'),
            Rule('/admin/page/upgrade', endpoint='admin-page-upgrade', handler='dataloader.UpdatePageHandler'),
            
            Rule('/paypal/ipn', endpoint='ipn', handler='handlers.IpnHandler'),

            #Rule('/', endpoint='home', handler='MainHandler'),
            Rule('/book/', endpoint='book', handler='handlers.BookHandler'),
            Rule('/book/index', endpoint='book-index', handler='handlers.IndexHandler'),
            Rule('/book/toc', endpoint='book-toc', handler='handlers.TocHandler'),
            Rule('/book/page/<number>', endpoint='page_def', handler='handlers.PageHandler'),
            Rule('/book/page/<number>/<size>', endpoint='page', handler='handlers.PageHandler'),
            #Rule('/admin/', endpoint='home', handler='AdminHandler'),
            Rule('/upload', endpoint='blobstore/upload', handler='handlers.UploadHandler'),
            
            Rule('/book/index', endpoint='book-index', handler='handlers.IndexHandler'),

        ]),
    ]

    return rules
