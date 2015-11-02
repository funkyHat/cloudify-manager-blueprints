#!/usr/bin/env python

from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py'))
import utils  # NOQA


target_runtime_props = ctx.target.instance.runtime_properties
source_runtime_props = ctx.source.instance.runtime_properties

# security setting from the manager configuration
riemann_server_host = target_runtime_props['riemann_server_host']
rest_host = target_runtime_props['internal_rest_host']
rest_protocol = target_runtime_props['rest_protocol']
rest_port = target_runtime_props['rest_port']
security_enabled = target_runtime_props['security_enabled']
ssl_enabled = target_runtime_props['ssl_enabled']

# security settings from Riemann's configuration # currently ignored by riemann
cloudify_username = ctx.source.node.properties['rest_username']
cloudify_password = ctx.source.node.properties['rest_password']
verify_certificate = ctx.source.node.properties['verify_manager_certificate']
add_server_ssl_certs_to_riemann_ca_path = \
    ctx.source.node.properties['add_server_ssl_certs_to_riemann_ca_path']


source_runtime_props['riemann_server_host'] = riemann_server_host
source_runtime_props['rest_host'] = rest_host
source_runtime_props['rest_protocol'] = rest_protocol
source_runtime_props['rest_port'] = rest_port
source_runtime_props['security_enabled'] = security_enabled
source_runtime_props['ssl_enabled'] = ssl_enabled


ctx.logger.info('***** debug: Riemann riemann_server_host: {0}'.
                format(riemann_server_host))
ctx.logger.info('***** debug: Riemann rest_host: {0}'.
                format(rest_host))
ctx.logger.info('***** debug: Riemann rest_protocol: {0}'.
                format(rest_protocol))
ctx.logger.info('***** debug: Riemann rest_port: {0}'.
                format(rest_port))
ctx.logger.info('***** debug: Riemann security_enabled: {0}'.
                format(security_enabled))
ctx.logger.info('***** debug: Riemann ssl_enabled: {0}'.
                format(ssl_enabled))
ctx.logger.info('***** debug: Riemann cloudify_username: {0}'.
                format(cloudify_username))
ctx.logger.info('***** debug: Riemann cloudify_password: {0}'.
                format(cloudify_password))
ctx.logger.info('***** debug: Riemann verify_certificate: {0}'.
                format(verify_certificate))
ctx.logger.info('***** debug: Riemann add_server_ssl_certs_to_riemann_ca_path:'
                ' {0}'.format(add_server_ssl_certs_to_riemann_ca_path))
