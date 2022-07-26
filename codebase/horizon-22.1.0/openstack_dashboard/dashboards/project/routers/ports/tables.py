# Copyright 2012,  Nachi Ueno,  NTT MCL,  Inc.
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

import logging

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django.utils.translation import pgettext_lazy

from horizon import tables
from openstack_dashboard import api
from openstack_dashboard.dashboards.project.networks.ports \
    import tables as project_tables
from openstack_dashboard import policy

LOG = logging.getLogger(__name__)


def get_device_owner(port):
    if port['device_owner'] == 'network:router_gateway':
        return _('External Gateway')
    if port['device_owner'] == 'network:router_interface':
        return _('Internal Interface')
    return ' '


class AddInterface(policy.PolicyTargetMixin, tables.LinkAction):
    name = "create"
    verbose_name = _("Add Interface")
    url = "horizon:project:routers:addinterface"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("network", "add_router_interface"),)

    def get_link_url(self, datum=None):
        router_id = self.table.kwargs['router_id']
        return reverse(self.url, args=(router_id,))


class RemoveInterface(policy.PolicyTargetMixin, tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete Interface",
            "Delete Interfaces",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Deleted Interface",
            "Deleted Interfaces",
            count
        )

    failure_url = 'horizon:project:routers:detail'
    policy_rules = (("network", "remove_router_interface"),)

    def allowed(self, request, datum=None):
        if datum and datum.get('device_owner'):
            if datum['device_owner'] == 'network:router_ha_interface':
                return False
        return True

    def delete(self, request, obj_id):
        try:
            router_id = self.table.kwargs['router_id']
            port = api.neutron.port_get(request, obj_id)
            if port['device_owner'] == 'network:router_gateway':
                api.neutron.router_remove_gateway(request, router_id)
            else:
                api.neutron.router_remove_interface(request,
                                                    router_id,
                                                    port_id=obj_id)
        except Exception as e:
            LOG.info('Failed to delete interface %(id)s: %(exc)s',
                     {'id': obj_id, 'exc': e})
            # NOTE: No exception handling is required here because
            # BatchAction.handle() does it. What we need to do is
            # just to re-raise the exception.
            raise


DISPLAY_CHOICES = (
    ("UP", pgettext_lazy("Admin state of a Port", "UP")),
    ("DOWN", pgettext_lazy("Admin state of a Port", "DOWN")),
)
STATUS_DISPLAY_CHOICES = (
    ("ACTIVE", pgettext_lazy("current status of port", "Active")),
    ("BUILD", pgettext_lazy("current status of port", "Build")),
    ("DOWN", pgettext_lazy("current status of port", "Down")),
    ("ERROR", pgettext_lazy("current status of port", "Error")),
    ("N/A", pgettext_lazy("current status of port", "N/A")),
)


class PortsTable(tables.DataTable):
    name = tables.Column("name_or_id",
                         verbose_name=_("Name"),
                         link="horizon:project:networks:ports:detail")
    fixed_ips = tables.Column(project_tables.get_fixed_ips,
                              verbose_name=_("Fixed IPs"))
    status = tables.Column("status",
                           verbose_name=_("Status"),
                           display_choices=STATUS_DISPLAY_CHOICES)
    device_owner = tables.Column(get_device_owner,
                                 verbose_name=_("Type"))
    admin_state = tables.Column("admin_state",
                                verbose_name=_("Admin State"),
                                display_choices=DISPLAY_CHOICES)

    def get_object_display(self, port):
        return port.name_or_id

    class Meta(object):
        name = "interfaces"
        verbose_name = _("Interfaces")
        table_actions = (AddInterface, RemoveInterface)
        row_actions = (RemoveInterface, )
