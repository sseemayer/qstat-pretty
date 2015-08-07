import subprocess

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO


def source_file(path):
    def get(_p, _a):
        with open(path, "r") as f:
            return StringIO(f.read())

    return get


def source_local():
    def get(parser, args):
        commandline = parser.suggest_commandline(args)

        with subprocess.Popen(commandline, stdout=subprocess.PIPE) as proc:
            return StringIO(proc.stdout.read())

    return get


def source_ssh(hostname, ssh_args=[]):
    def get(parser, args):
        commandline = ['ssh', hostname] + ssh_args + ['--'] + parser.suggest_commandline(args)

        with subprocess.Popen(commandline, stdout=subprocess.PIPE) as proc:
            return StringIO(proc.stdout.read())

    return get
