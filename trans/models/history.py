# -*- coding: utf-8 -*-
#
# Copyright © 2013 Ilya Zhuravlev <whatever@xyz.is>
#
# This file is part of Weblate <http://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.db import models
from django.contrib.auth.models import User

from trans.util import get_user_display


class HistoryManager(models.Manager):
    def add(self, unit, target, user):
        History.objects.create(
            unit = unit,
            target = target,
            user = user
        )


class History(models.Model):
    target = models.TextField(default='', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    unit = models.ForeignKey('Unit')
    user = models.ForeignKey(User, null=True)

    objects = HistoryManager()

    class Meta:
        app_label = 'trans'

    def get_user_display(self):
        return get_user_display(self.user)
