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


            Rule('/content', endpoint='content/index', handler='handlers.ContentHandler'),
            Rule('/admin', endpoint='admin', handler='handlers.AdminHandler'),
            Rule('/paypal/ipn', endpoint='ipn', handler='handlers.IpnHandler'),
        ]),
    ]

    return rules
