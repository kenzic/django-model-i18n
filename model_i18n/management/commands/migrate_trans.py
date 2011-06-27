# -*- coding: utf-8 -*-
import sys
import os
import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Migrate apps configured in TRANSLATED_APP_MODELS."

    def handle(self, *args, **options):
        if 'south' in settings.INSTALLED_APPS:
            do_migrate = False
            try:
                 do_migrate = (args[0] == "migrate")
            except:
                pass
            from model_i18n.conf import TRANSLATED_APP_MODELS
            for app_path in TRANSLATED_APP_MODELS:
                app_name = app_path.split(".")[-1]
                mig_path = 'model_i18n.migrations.' + app_name
                extra_south_modules = {app_name: mig_path}
                settings.SOUTH_MIGRATION_MODULES.update(extra_south_modules)
                try:
                    call_command('convert_to_south', app_name)
                    call_command('schemamigration', app_name, auto=True)
                except:
                    pass
                if do_migrate:
                    call_command('migrate', app_name)
        else:
            pass
            #TODO: Generate dumpdata, reset and loaddata
