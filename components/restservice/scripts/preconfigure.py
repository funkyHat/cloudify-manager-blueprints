#!/usr/bin/env python

from cloudify import ctx


def preconfigure_restservice():

    target_runtime_props = ctx.target.instance.runtime_properties
    source_runtime_props = ctx.source.instance.runtime_properties

    ctx.logger.info('Reading internal_rest_host from manager_configuration...')
    internal_rest_host = target_runtime_props['internal_rest_host']
    ctx.logger.info('internal_rest_host is: {0}'.format(internal_rest_host))
    source_runtime_props['internal_rest_host'] = internal_rest_host

    ctx.logger.info('Reading external_rest_host from manager_configuration...')
    external_rest_host = target_runtime_props['external_rest_host']
    ctx.logger.info('external_rest_host is: {0}'.format(external_rest_host))
    source_runtime_props['external_rest_host'] = external_rest_host

    ctx.logger.info('Reading security property from manager_configuration...')
    security_config = str(ctx.target.node.properties['security'])
    ctx.logger.info('security_config is: {0}'.format(security_config))
    source_runtime_props['security_configuration'] = security_config


preconfigure_restservice()
