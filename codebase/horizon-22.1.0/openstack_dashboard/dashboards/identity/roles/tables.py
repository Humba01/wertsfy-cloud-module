# Copyright 2013 Hewlett-Packard Development Company, L.P.
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

from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

from horizon import tables

from openstack_dashboard import api


class CreateRoleLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Role")
    url = "horizon:identity:roles:create"
    classes = ("ajax-modal",)
    icon = "plus"
    policy_rules = (("identity", "identity:create_role"),)

    def allowed(self, request, role):
        return api.keystone.keystone_can_edit_role()


class EditRoleLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:identity:roles:update"
    classes = ("ajax-modal",)
    icon = "pencil"
    policy_rules = (("identity", "identity:update_role"),)

    def allowed(self, request, role):
        return api.keystone.keystone_can_edit_role()


class DeleteRolesAction(tables.DeleteAction):
    @staticmethod
    def action_present(count):
        return ngettext_lazy(
            "Delete Role",
            "Delete Roles",
            count
        )

    @staticmethod
    def action_past(count):
        return ngettext_lazy(
            "Deleted Role",
            "Deleted Roles",
            count
        )
    policy_rules = (("identity", "identity:delete_role"),)

    def allowed(self, request, role):
        return api.keystone.keystone_can_edit_role()

    def delete(self, request, obj_id):
        api.keystone.role_delete(request, obj_id)


class RoleFilterAction(tables.FilterAction):
    filter_type = "server"
    filter_choices = (("name", _("Role Name ="), True),
                      ("id", _("Role ID ="), True))


class RolesTable(tables.DataTable):
    name = tables.WrappingColumn('name', verbose_name=_('Role Name'))
    id = tables.Column('id', verbose_name=_('Role ID'))

    class Meta(object):
        name = "roles"
        verbose_name = _("Roles")
        row_actions = (EditRoleLink, DeleteRolesAction)
        table_actions = (RoleFilterAction, CreateRoleLink, DeleteRolesAction)
