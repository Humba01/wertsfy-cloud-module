# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.urls import re_path

from openstack_dashboard.dashboards.identity.projects import views


urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^create$', views.CreateProjectView.as_view(), name='create'),
    re_path(r'^(?P<tenant_id>[^/]+)/update/$',
            views.UpdateProjectView.as_view(), name='update'),
    re_path(r'^(?P<project_id>[^/]+)/usage/$',
            views.ProjectUsageView.as_view(), name='usage'),
    re_path(r'^(?P<project_id>[^/]+)/detail/$',
            views.DetailProjectView.as_view(), name='detail'),
    re_path(r'^(?P<tenant_id>[^/]+)/update_quotas/$',
            views.UpdateQuotasView.as_view(), name='update_quotas'),
]
