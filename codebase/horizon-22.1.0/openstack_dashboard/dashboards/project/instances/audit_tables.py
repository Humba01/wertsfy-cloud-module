# Copyright 2013 Metacloud, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.


from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from horizon import tables
from horizon.utils import filters


class AuditTable(tables.DataTable):
    ACTION_DISPLAY_CHOICES = (
        ("create", pgettext_lazy("Action log of an instance", "Create")),
        ("pause", pgettext_lazy("Action log of an instance", "Pause")),
        ("unpause", pgettext_lazy("Action log of an instance", "Unpause")),
        ("rebuild", pgettext_lazy("Action log of an instance", "Rebuild")),
        ("resize", pgettext_lazy("Action log of an instance", "Resize")),
        ("confirmresize", pgettext_lazy("Action log of an instance",
                                        "Confirm Resize")),
        ("suspend", pgettext_lazy("Action log of an instance", "Suspend")),
        ("resume", pgettext_lazy("Action log of an instance", "Resume")),
        ("reboot", pgettext_lazy("Action log of an instance", "Reboot")),
        ("stop", pgettext_lazy("Action log of an instance", "Stop")),
        ("start", pgettext_lazy("Action log of an instance", "Start")),
        ("shelve", pgettext_lazy("Action log of an instance", "Shelve")),
        ("unshelve", pgettext_lazy("Action log of an instance", "Unshelve")),
        ("migrate", pgettext_lazy("Action log of an instance", "Migrate")),
        ("rescue", pgettext_lazy("Action log of an instance", "Rescue")),
        ("unrescue", pgettext_lazy("Action log of an instance", "Unrescue")),
        ("lock", pgettext_lazy("Action log of an instance", "Lock")),
        ("unlock", pgettext_lazy("Action log of an instance", "Unlock")),
        ("createimage", pgettext_lazy("Action log of an instance",
                                      "Create Image")),
    )

    request_id = tables.Column('request_id',
                               verbose_name=_('Request ID'))
    action = tables.Column('action', verbose_name=_('Action'),
                           display_choices=ACTION_DISPLAY_CHOICES)
    start_time = tables.Column('start_time', verbose_name=_('Start Time'),
                               filters=[filters.parse_isotime])
    user_id = tables.Column('user_id', verbose_name=_('User ID'))
    message = tables.Column('message', verbose_name=_('Message'))

    class Meta(object):
        name = 'audit'
        verbose_name = _('Instance Action List')

    def get_object_id(self, datum):
        return datum.request_id
