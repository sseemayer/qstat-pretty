try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import os.path


CONFIGS_ORDER = [
    '/etc/qstat-pretty/qstat-pretty.conf',
    os.path.expanduser('~/.config/qstat-pretty/qstat-pretty.conf'),
    'qstat-pretty.conf',
]


def get_config(configs_order=CONFIGS_ORDER):
    parser = configparser.SafeConfigParser()
    try:
        parser.read(configs_order)
        cfg = parser.items('defaults')
    except:
        cfg = {
            'flavor': 'gridengine',
            'table_algorithm': 'grow',
            'delimiters': 'minimal',
            'source': 'local',
            'source_ssh_hostname': '',
            'source_file_path': ''
        }

    return dict(cfg)
