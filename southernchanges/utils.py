import os
#import requests
import hashlib
from urlparse import urlparse
#from sunburnt import sunburnt

from django.conf import settings
from django.contrib.sites.models import Site

def absolutize_url(local_url):
    '''Convert a local url to an absolute url, with scheme and server name,
    based on the current configured :class:`~django.contrib.sites.models.Site`.

    :param local_url: local url to be absolutized, e.g. something generated by
        :meth:`~django.core.urlresolvers.reverse`
    '''
    if local_url.startswith('http'):
        return local_url

    # add scheme and server (i.e., the http://example.com) based
    # on the django Sites infrastructure.
    root = Site.objects.get_current().domain
    # but also add the http:// if necessary, since most sites docs
    # suggest using just the domain name
    if not root.startswith('http'):
        root = 'http://' + root

    # make sure there is no double slash between site url and local url
    if local_url.startswith('/'):
        root = root.rstrip('/')

    return root + local_url
