# -*- coding: utf-8 -*-

import thread
import time
import sys
import os

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.utils.termcolors import colorize

from requests import get

from geoip.redis_wrapper import RedisSync
from geoip.defaults import DB_IMPORT_URL


DB_FILE_NAME = os.path.basename(DB_IMPORT_URL)


class Command(NoArgsCommand):
    _status = ''

    def handle_noargs(self, **options):
        sys.stdout.write(colorize(
            'Please, wait. This will take some time\n', fg='magenta'))
        self._clean_database()
        self._clean_redis()
        self._sync()

    def _clean_database(self):
        for model in ContentType.objects.filter(app_label='geoip'):
            model.model_class().objects.all().delete()

    def _clean_redis(self):
        sync = RedisSync()
        sync.clean_all()

    def _sync(self):
        thread.start_new_thread(self._bg_sync, ())
        self._progress()

    def _bg_sync(self):
        try:
            self.__download()
            self.__loaddata()
        except:
            sys.stdout.write(' Error\n')
        self.__clean()
        self._status = None

    def _progress_line(self, label, task, end='', color='white'):
        label = colorize('[%s]' % label, fg=color)
        sys.stdout.write("\r%s %s ...%s" % (label, task, end))
        sys.stdout.flush()

    def __download(self):
        self._status = 'downloading database'
        open(DB_FILE_NAME, 'w').write(get(DB_IMPORT_URL).content)

    def __loaddata(self):
        self._status = 'importing database'
        call_command('loaddata', DB_FILE_NAME, verbosity=0)
        time.sleep(3)

    def __clean(self):
        self._status = 'cleaning'
        if os.path.exists(DB_FILE_NAME):
            os.unlink(DB_FILE_NAME)
        time.sleep(2)

    def _progress(self, i=0):
        progress = ['-', '\\', '|', '/']
        old_status = None

        while True:
            if self._status:
                if self._status and old_status and self._status != old_status:
                    self._progress_line('done', old_status, '\n', 'green')
                else:
                    self._progress_line(progress[i], self._status)
                old_status = self._status

                time.sleep(1)
                i = 0 if i == 3 else i + 1
                if self._status is None:
                    self._progress_line('done', old_status, '\n', 'green')
                    break
