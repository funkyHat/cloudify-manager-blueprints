#!/usr/bin/env python

from os.path import join, dirname

from cloudify import ctx

ctx.download_resource(
    join('components', 'utils.py'),
    join(dirname(__file__), 'utils.py')
)
import utils  # NOQA

NODE_NAME = 'manager-config'

ctx_properties = utils.ctx_factory.create(NODE_NAME)


def _disable_requiretty():
    script_dest = '/tmp/configure_manager.sh'
    utils.deploy_blueprint_resource('components/manager/scripts'
                                    '/configure_manager.sh',
                                    script_dest,
                                    NODE_NAME)

    utils.sudo('chmod +x {0}'.format(script_dest))
    utils.sudo(script_dest)


def _configure_security_properties():

    agent_config = ctx_properties['cloudify']['cloudify_agent']
    security_config = ctx_properties['security']
    security_enabled = security_config['enabled']
    ssl_enabled = security_config['ssl']['enabled']

    if security_enabled:
        # agent access-control settings
        agents_rest_username = agent_config['rest_username']
        agents_rest_password = agent_config['rest_password']
        ctx.instance.runtime_properties['agents_rest_username'] = \
            agents_rest_username
        ctx.instance.runtime_properties['agents_rest_password'] = \
            agents_rest_password
        ctx.logger.info('agents_rest_username: {0}'.
                        format(agents_rest_username))
        ctx.logger.info('agents_rest_password: {0}'.
                        format(agents_rest_password))

    if security_enabled and ssl_enabled:
        # manager SSL settings
        ctx.logger.info('SSL is enabled, setting rest port to 443 and '
                        'rest_protocol to https')
        ctx.instance.runtime_properties['rest_port'] = 443
        ctx.instance.runtime_properties['rest_protocol'] = 'https'
        # agent SSL settings related
        verify_manager_certificate = agent_config['verify_manager_certificate']
        ctx.instance.runtime_properties['verify_manager_certificate'] = \
            verify_manager_certificate
        ctx.logger.info('verify_manager_certificate: {0}'.
                        format(verify_manager_certificate))
    else:
        ctx.logger.info('Security is off or SSL disabled, setting rest port '
                        'to 80 and rest protocols to http')
        ctx.instance.runtime_properties['rest_port'] = 80
        ctx.instance.runtime_properties['rest_protocol'] = 'http'


def main():
    _disable_requiretty()
    _configure_security_properties()
    if utils.is_upgrade:
        utils.resource_factory.archive_resources(NODE_NAME)
        utils.ctx_factory.archive_properties(NODE_NAME)

main()
