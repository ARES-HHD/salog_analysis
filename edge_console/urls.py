# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from commons import edge_permission_required_by_url, permitted_url

from edge_console.views_salog import *

# 系统工具
urlpatterns += patterns(
    'edge_console.views_salog',

    permitted_url(r'^notes/salog/analysis/$',
                  salog_analysis),
    )
