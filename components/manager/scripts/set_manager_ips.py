from cloudify import ctx
from cloudify.state import ctx_parameters as inputs

source_runtime_props = ctx.source.instance.runtime_properties

# set private ip according to the host ip
private_ip = ctx.target.instance.host_ip
ctx.logger.info('Setting manager_configuration private ip to: {0}'.
                format(private_ip))
source_runtime_props['private_ip'] = private_ip

public_ip = inputs['public_ip']
ctx.logger.info('Setting manager_configuration public ip to: {0}'.
                format(public_ip))
source_runtime_props['public_ip'] = public_ip

# set the Riemann server host to the private IP (backward compatible)
source_runtime_props['riemann_server_host'] = private_ip
ctx.logger.info('riemann_server_host set to: {0}'.format(
    source_runtime_props['riemann_server_host']))

# If the agent's broker ip is empty, set it to the private ip
agent_configuration = ctx.source.node.properties['cloudify']['cloudify_agent']
broker_ip = agent_configuration.get('broker_ip', '').strip()
if not broker_ip:
    broker_ip = private_ip
    ctx.logger.info('broker_ip is empty, setting it to: {0}'.
                    format(private_ip))
source_runtime_props['broker_ip'] = broker_ip
ctx.logger.info('broker_ip is set to: {0}'.format(
    source_runtime_props['broker_ip']))

# set the internal file server host according to the file server internal
# identifier (public ip / private ip)
file_server_internal_identifier = inputs['file_server_internal_identifier']
ctx.logger.info('file_server_internal_identifier is: {0}'.format(
    file_server_internal_identifier))
if file_server_internal_identifier == 'private_ip':
    source_runtime_props['internal_file_server_host'] = private_ip
elif file_server_internal_identifier == 'public_ip':
    source_runtime_props['internal_file_server_host'] = public_ip
else:
    # how to raise exception here?
    ctx.logger.info('invalid file_server_internal_identifier: {0}'.format(
        file_server_internal_identifier))
ctx.logger.info('internal_file_server_host set to: {0}'.format(
    source_runtime_props['internal_file_server_host']))

# set the external file server host according to the file server external
# identifier (public ip / private ip)
file_server_external_identifier = inputs['file_server_external_identifier']
ctx.logger.info('file_server_external_identifier is: {0}'.format(
    file_server_external_identifier))
if file_server_external_identifier == 'private_ip':
    source_runtime_props['external_file_server_host'] = private_ip
elif file_server_external_identifier == 'public_ip':
    source_runtime_props['external_file_server_host'] = public_ip
else:
    # how to raise exception here?
    ctx.logger.info('invalid file_server_external_identifier: {0}'.format(
        file_server_external_identifier))
ctx.logger.info('external_file_server_host set to: {0}'.format(
    source_runtime_props['external_file_server_host']))


# set the internal REST host according to the REST internal identifier
# (public ip / private ip)
rest_host_internal_identifier = inputs['rest_host_internal_identifier']
ctx.logger.info('rest_host_internal_identifier is: {0}'.format(
    rest_host_internal_identifier))
if rest_host_internal_identifier == 'private_ip':
    source_runtime_props['internal_rest_host'] = private_ip
elif rest_host_internal_identifier == 'public_ip':
    source_runtime_props['internal_rest_host'] = public_ip
else:
    # how to raise exception here?
    ctx.logger.info('invalid rest_host_internal_identifier: {0}'.format(
        rest_host_internal_identifier))
ctx.logger.info('internal_rest_host set to: {0}'.format(
    source_runtime_props['internal_rest_host']))

# set the external REST host according to the REST external identifier
# (public ip / private ip)
rest_host_external_identifier = inputs['rest_host_external_identifier']
ctx.logger.info('rest_host_external_identifier is: {0}'.format(
    rest_host_external_identifier))
if rest_host_external_identifier == 'private_ip':
    source_runtime_props['external_rest_host'] = private_ip
elif rest_host_external_identifier == 'public_ip':
    source_runtime_props['external_rest_host'] = public_ip
else:
    # how to raise exception here?
    ctx.logger.info('invalid rest_host_external_identifier: {0}'.format(
        rest_host_external_identifier))
ctx.logger.info('external_rest_host set to: {0}'.format(
    source_runtime_props['external_rest_host']))
