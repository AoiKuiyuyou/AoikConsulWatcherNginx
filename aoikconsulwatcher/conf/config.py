# coding: utf-8
from __future__ import absolute_import

import os
import subprocess
import sys

from jinja2 import Template


CONSUL_HOST = os.environ.get('CONSUL_HOST', '127.0.0.1')

CONSUL_PORT = int(os.environ.get('CONSUL_PORT', '8500'))

TEMPLATE_FILE_PATH = os.environ.get(
    'TEMPLATE_FILE_PATH',
    'nginx/nginx_sites.conf.template'
)


def handle_service_infos(service_infos):
    filtered_service_infos = dict(
        (service_name, service_info)
        for service_name, service_info in service_infos.items()
        if filter_service(service_name, service_info)
    )

    template_text = get_template_text()

    template_obj = Template(template_text)

    template_env = {
        'service_infos': filtered_service_infos
    }

    rendered_text = template_obj.render(**template_env)

    handle_rendered_text(rendered_text)


def filter_service(service_name, service_info):
    nodes = service_info.get('nodes', None)

    if not nodes:
        return False

    node = nodes[0]

    if not node.get('ServiceAddress', None):
        return False

    if not node.get('ServicePort', None):
        return False

    if service_name == 'consul-8500':
        server_name = 'consul.local'
    else:
        server_name = service_name + '.local'

    service_info['nginx_config'] = {
        'upstream_name': service_name,
        'server_name': server_name,
        'listen_port': 80,
    }

    return True


_TEMPLATE_TEXT = None


def get_template_text():
    global _TEMPLATE_TEXT

    if _TEMPLATE_TEXT is None:
        try:
            _TEMPLATE_TEXT = open(TEMPLATE_FILE_PATH).read()
        except Exception:
            msg = 'Failed opening template file: {0}\n'\
                .format(TEMPLATE_FILE_PATH)

            sys.stderr.write(msg)

            raise

    return _TEMPLATE_TEXT


def handle_rendered_text(rendered_text):
    output_file_path = '/etc/nginx/sites-enabled/nginx_sites.conf'

    with open(output_file_path, mode='w') as output_file:
        output_file.write(rendered_text)

    msg = 'Updated `{0}`.'.format(output_file_path)

    print(msg)

    reload_cmd = ['/usr/sbin/nginx', '-s', 'reload']

    exit_code = subprocess.call(reload_cmd)

    msg = 'Reloaded Nginx config. Exit code: {0}'.format(exit_code)

    print(msg)
