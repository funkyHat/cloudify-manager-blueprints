#!/usr/bin/env python

from os.path import join, dirname, abspath
import tempfile

from cloudify import ctx

ctx.download_resource(
        join('components', 'utils.py'),
        join(dirname(__file__), 'utils.py'))
import utils  # NOQA

APP_NAME = 'cloudify-hello-world-example'
APP_URL = 'https://github.com/cloudify-cosmo/' \
          '{0}/archive/master.tar.gz'.format(APP_NAME)


def prepare_sanity():
    app_tar = utils.download_file(APP_URL)
    app_dir = tempfile.mkdtemp(prefix=APP_NAME)
    utils.untar(app_tar, destination=app_dir)
    utils.remove(app_tar)
    ctx.instance.runtime_properties['sanity_app_dir'] = app_dir

prepare_sanity()
