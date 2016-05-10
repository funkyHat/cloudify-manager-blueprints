#!/bin/python

import fabric.api

from cloudify import ctx


def upload_keypair(manager_user, local_key_path):
    ctx.logger.info('putting key from {0}'.format(local_key_path))
    manager_remote_key_path = '/home/{0}/.ssh/mng-key.pem'.format(manager_user)
    fabric.api.put(local_key_path,
                   manager_remote_key_path,
                   use_sudo=True)

    ctx.instance.runtime_properties['manager_user'] = manager_user
    ctx.instance.runtime_properties['manager_remote_key_path'] = \
        manager_remote_key_path
