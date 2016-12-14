# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.contrib.admin.sites import AdminSite
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.conf.urls import url
from core.views import WelcomeAdminView


class AdminMixin(object):

    def __init__(self, *args, **kwargs):
        return super(AdminMixin, self).__init__(*args, **kwargs)

    def get_urls(self):
        urls = super(AdminMixin, self).get_urls()
        custom_url = [
               url(r'^$', self.admin_view(WelcomeAdminView.as_view()), 
                    name="index")
        ]
        return custom_url + urls 
    
class SitePlus(AdminMixin, AdminSite):
    site_title = _('Sistema de controle de relógio de ponto')
    index_title = _('Sistema de controle de relógio de ponto')
    site_header = _('Sistema de controle de relógio de ponto')
    site_url = None
    
    @never_cache
    def index(self, request, extra_context=None):
        return AdminSite.index(self, request, extra_context=extra_context)
    
admin_site = SitePlus()