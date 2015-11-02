#!/usr/bin/env python

from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA

target_runtime_props = ctx.target.instance.runtime_properties
source_runtime_props = ctx.source.instance.runtime_properties

file_server_host = target_runtime_props['internal_file_server_host']
rest_host = target_runtime_props['internal_rest_host']
rest_protocol = target_runtime_props['rest_protocol']
rest_port = target_runtime_props['rest_port']
security_enabled = target_runtime_props['security_enabled']
ssl_enabled = target_runtime_props['ssl_enabled']
cloudify_username = target_runtime_props['agents_rest_username']
cloudify_password = target_runtime_props['agents_rest_password']
verify_certificate = target_runtime_props['verify_manager_certificate']
local_rest_cert_file = target_runtime_props['local_rest_cert_file']
# using sudo to copy the certificate to a temp folder,
# from which the unprivileged user running this script can get its content
utils.mkdir('temp')
utils.copy(local_rest_cert_file, 'temp')
temp_path = 'temp/internal_rest_host.crt'
rest_cert_content = utils.escape_for_systemd(utils.get_file_content(temp_path))
ctx.logger.info('***** debug: MgmtWorker read internal_rest_host.crt '
                'content: {0}'.format(rest_cert_content))
utils.remove_dir('temp')


source_runtime_props['file_server_host'] = file_server_host
source_runtime_props['rest_host'] = rest_host
source_runtime_props['rest_protocol'] = rest_protocol
source_runtime_props['rest_port'] = rest_port
source_runtime_props['security_enabled'] = security_enabled
source_runtime_props['ssl_enabled'] = ssl_enabled
source_runtime_props['cloudify_username'] = cloudify_username
source_runtime_props['cloudify_password'] = cloudify_password
source_runtime_props['verify_certificate'] = verify_certificate
source_runtime_props['local_rest_cert_file'] = local_rest_cert_file
source_runtime_props['rest_cert_content'] = rest_cert_content


ctx.logger.info('***** debug: MgmtWorker file_server_host: {0}'
                .format(file_server_host))
ctx.logger.info('***** debug: MgmtWorker rest_host: {0}'
                .format(rest_host))
ctx.logger.info('***** debug: MgmtWorker rest_protocol: {0}'
                .format(rest_protocol))
ctx.logger.info('***** debug: MgmtWorker rest_port: {0}'
                .format(rest_port))
ctx.logger.info('***** debug: MgmtWorker security_enabled: {0}'
                .format(security_enabled))
ctx.logger.info('***** debug: MgmtWorker ssl_enabled: {0}'
                .format(ssl_enabled))
ctx.logger.info('***** debug: MgmtWorker cloudify_username: {0}'
                .format(cloudify_username))
ctx.logger.info('***** debug: MgmtWorker cloudify_password: {0}'
                .format(cloudify_password))
ctx.logger.info('***** debug: MgmtWorker verify_certificate: {0}'
                .format(verify_certificate))
ctx.logger.info('***** debug: MgmtWorker local_rest_cert_file: {0}'
                .format(local_rest_cert_file))
ctx.logger.info('***** debug: MgmtWorker rest_cert_content: {0}'
                .format(rest_cert_content))
