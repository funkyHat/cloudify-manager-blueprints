#!/usr/bin/env python

import os
from os.path import join, dirname
import requests
import json

from cloudify import ctx

ctx.download_resource(
        join('components', 'utils.py'),
        join(dirname(__file__), 'utils.py'))
import utils  # NOQA

APP_NAME = 'cloudify-hello-world-example'
APP_URL = 'https://github.com/cloudify-cosmo/' \
          '{0}/archive/master.tar.gz'.format(APP_NAME)
BLUEPRINT_ID = 'sanity_bp'
DEPLOYMENT_ID = 'sanity_deployment'

manager_ip = os.environ.get('manager_ip')
manager_user = ctx.instance.runtime_properties['manager_user']
manager_remote_key_path = \
    ctx.instance.runtime_properties['manager_remote_key_path']


def prepare_sanity_app():
    app_tar = utils.download_file(APP_URL)
    ctx.instance.runtime_properties['sanity_app_tar'] = app_tar
    ctx.instance.runtime_properties['blueprint_id'] = BLUEPRINT_ID
    ctx.instance.runtime_properties['deployment_id'] = DEPLOYMENT_ID
    ctx.instance.runtime_properties['manager_ip'] = manager_ip

    upload_app_blueprint()
    deploy_app()


def upload_app_blueprint():
    app_tar = ctx.instance.runtime_properties['sanity_app_tar']
    data = utils.request_data_file_stream_gen(app_tar)
    requests.put(
        'http://{0}/api/v2.1/blueprints/'
        '{1}'.format(manager_ip, BLUEPRINT_ID),
        data=data,
        params={'application_file_name': 'singlehost-blueprint.yaml'})


def deploy_app():
    dep_inputs = {'server_ip': manager_ip,
                  'agent_user': manager_user,
                  'agent_private_key_path': manager_remote_key_path}
    data = {
        'blueprint_id': BLUEPRINT_ID,
        'inputs': dep_inputs
    }
    requests.put(
        'http://{0}/api/v2.1/deployments'
        '/{1}'.format(manager_ip, DEPLOYMENT_ID),
        data=json.dumps(data),
        headers={'content-type': 'application/json'})

    # Waiting for create deployment env to end
    utils.repetitive(
            _wait_for_dep_env,
            timeout_msg='timed out while waiting for '
                        'deployment {0} to be created'.format(DEPLOYMENT_ID))


def _wait_for_dep_env():
    resp = requests.get(
        'http://{0}/api/v2.1/executions'.format(manager_ip),
        params={'deployment_id': DEPLOYMENT_ID})

    json_resp = json.loads(resp.content)
    for execution in json_resp['items']:
        if execution['workflow_id'] == 'create_deployment_environment':
            return execution['status'] == 'terminated'
    return False

prepare_sanity_app()
