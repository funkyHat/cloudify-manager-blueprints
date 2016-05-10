#!/usr/bin/env python

import os
from os.path import join, dirname
from os import remove
import requests
import json

from cloudify import ctx

ctx.download_resource(
        join('components', 'utils.py'),
        join(dirname(__file__), 'utils.py'))
import utils  # NOQA


BLUEPRINT_ID = ctx.instance.runtime_properties['blueprint_id']
DEPLOYMENT_ID = ctx.instance.runtime_properties['deployment_id']
manager_ip = ctx.instance.runtime_properties['manager_ip']
app_tar = ctx.instance.runtime_properties['sanity_app_tar']
manager_remote_key_path = \
    ctx.instance.runtime_properties['manager_remote_key_path']


def start():
    # install_sanity_app()
    assert_webserver_running()
    assert_deployment_monitoring_data_exists()
    cleanup_sanity()


def install_sanity_app():
    data = {
        'deployment_id': DEPLOYMENT_ID,
        'workflow_id': 'install'
    }
    requests.post(
            'http://{0}/api/v2.1/executions'.format(manager_ip),
            data=json.dumps(data),
            headers={'content-type': 'application/json'})

    # Waiting for installation to complete
    utils.repetitive(
            _wait_for_installation,
            timeout=5*60,
            interval=30,
            timeout_msg='timed out while waiting for '
                        'deployment {0} to install.'.format(DEPLOYMENT_ID))


def assert_webserver_running():
    server_response = requests.get('http://localhost:8080', timeout=15)
    if server_response.status_code != 200:
        ctx.logger.info('bad')
    else:
        ctx.logger.info('all good')


def assert_deployment_monitoring_data_exists():
    influx_host_ip = os.environ.get('INFLUXDB_ENDPOINT_IP')
    if influx_host_ip == manager_ip:
        influx_host_ip = 'localhost'
    influx_user = 'root'
    influx_pass = 'root'

    query = 'select * from /^{0}\./i ' \
            'where time > now() - 5s'.format(DEPLOYMENT_ID)

    req = 'http://{0}:8086/db/cloudify/series?u={1}&p={2}&q={3}'.format(
            influx_host_ip,
            influx_user,
            influx_pass,
            query)

    resp = requests.get(req)
    json_resp = json.loads(resp.content)

    ctx.logger.info('monitor resp is: {0}'.format(json_resp))

    # TODO response 200 and not empty


def cleanup_sanity():
    _uninstall_sanity_app()
    _delete_sanity_deployment()
    _delete_sanity_blueprint()
    _delete_app_tar()
    _delete_key_file()


def _uninstall_sanity_app():
    ctx.logger.info('Uninstalling sanity app')
    data = {
        'deployment_id': DEPLOYMENT_ID,
        'workflow_id': 'uninstall'
    }
    requests.post(
            'http://{0}/api/v2.1/executions'.format(manager_ip),
            data=json.dumps(data),
            headers={'content-type': 'application/json'})

    # Waiting for installation to complete
    utils.repetitive(
            _wait_for_uninstallation,
            timeout=5*60,
            interval=30,
            timeout_msg='timed out while waiting for '
                        'deployment {0} to uninstall.'.format(DEPLOYMENT_ID))


def _delete_sanity_deployment():
    requests.delete(
            'http://{0}/api/v2.1/deployments'
            '/{1}'.format(manager_ip, DEPLOYMENT_ID))


def _delete_sanity_blueprint():
    requests.delete(
            'http://{0}/api/v2.1/blueprints/'
            '{1}'.format(manager_ip, BLUEPRINT_ID))


def _delete_app_tar():
    remove(app_tar)


def _delete_key_file():
    remove(manager_remote_key_path)


def _wait_for_uninstallation():
    resp = requests.get(
            'http://{0}/api/v2.1/executions'.format(manager_ip),
            params={'deployment_id': DEPLOYMENT_ID})

    json_resp = json.loads(resp.content)
    for execution in json_resp['items']:
        if execution['workflow_id'] == 'uninstall':
            return execution['status'] == 'terminated'
    return False


def _wait_for_installation():
    resp = requests.get(
            'http://{0}/api/v2.1/executions'.format(manager_ip),
            params={'deployment_id': DEPLOYMENT_ID})

    json_resp = json.loads(resp.content)
    for execution in json_resp['items']:
        if execution['workflow_id'] == 'install':
            return execution['status'] == 'terminated'
    return False

start()
