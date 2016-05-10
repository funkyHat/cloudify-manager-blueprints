# #!/usr/bin/env python
#
# from os.path import join, dirname
# from os import remove
# import requests
# import json
#
# from cloudify import ctx
#
# ctx.download_resource(
#         join('components', 'utils.py'),
#         join(dirname(__file__), 'utils.py'))
# import utils  # NOQA
#
# BLUEPRINT_ID = ctx.instance.runtime_properties['blueprint_id']
# DEPLOYMENT_ID = ctx.instance.runtime_properties['deployment_id']
# manager_ip = ctx.instance.runtime_properties['manager_ip']
# app_tar = ctx.instance.runtime_properties['sanity_app_tar']
#
#
# def cleanup_sanity():
#     _uninstall_sanity_app()
#     _delete_sanity_deployment()
#     _delete_sanity_blueprint()
#     _delete_app_tar()
#
#
# def _uninstall_sanity_app():
#     data = {
#         'deployment_id': DEPLOYMENT_ID,
#         'workflow_id': 'uninstall'
#     }
#     requests.post(
#             'http://{0}/api/v2.1/executions'.format(manager_ip),
#             data=json.dumps(data),
#             headers={'content-type': 'application/json'})
#
#     # Waiting for installation to complete
#     utils.repetitive(
#             _wait_for_uninstallation,
#             timeout=5*60,
#             interval=30,
#             timeout_msg='timed out while waiting for '
#                         'deployment {0} to uninstall.'.format(DEPLOYMENT_ID))
#
#
# def _delete_sanity_deployment():
#     requests.delete(
#             'http://{0}/api/v2.1/deployments'
#             '/{1}'.format(manager_ip, DEPLOYMENT_ID))
#
#
# def _delete_sanity_blueprint():
#     requests.delete(
#             'http://{0}/api/v2.1/blueprints/'
#             '{1}'.format(manager_ip, BLUEPRINT_ID))
#
#
# def _delete_app_tar():
#     remove(app_tar)
#
#
# def _wait_for_uninstallation():
#
#     resp = requests.get(
#             'http://{0}/api/v2.1/executions'.format(manager_ip),
#             params={'deployment_id': DEPLOYMENT_ID})
#
#     json_resp = json.loads(resp.content)
#     for execution in json_resp['items']:
#         if execution['workflow_id'] == 'uninstall':
#             return execution['status'] == 'terminated'
#     return False
#
# cleanup_sanity()
