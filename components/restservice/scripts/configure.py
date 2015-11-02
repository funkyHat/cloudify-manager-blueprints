#!/usr/bin/env python

import os
from os.path import join, dirname

import tempfile

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


# TODO: change to /opt/cloudify-rest-service
REST_SERVICE_HOME = '/opt/manager'


def _deploy_security_configuration():
    ctx.logger.info('Deploying REST Security configuration file...')
    security_configuration = \
        ctx.instance.runtime_properties['security_configuration']
    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, 'w') as f:
        f.write(security_configuration)
    utils.move(path, join(REST_SERVICE_HOME, 'rest-security.conf'))


def configure_restservice():
    _deploy_security_configuration()
    utils.systemd.configure('restservice')


configure_restservice()
