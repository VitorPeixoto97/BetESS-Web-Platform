# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        import os
        if not os.environ.get('RUN_MAIN', None):
            from . import messaging
            messaging.RabbitMessaging('user_queue')