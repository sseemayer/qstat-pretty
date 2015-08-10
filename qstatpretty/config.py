import configparser
import os.path


CONFIGS_ORDER = [
    '/etc/qstat-pretty/qstat-pretty.conf',
    os.path.expanduser('~/.config/qstat-pretty/qstat-pretty.conf'),
    'qstat-pretty.conf',
]


def get_config(configs_order=CONFIGS_ORDER):
    parser = configparser.SafeConfigParser()
    parser.read(configs_order)
    cfg = parser.items('defaults')

    return dict(cfg)
