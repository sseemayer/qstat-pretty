import subprocess

try:
    from io import StringIO
except ImportError:
    from cStringIO import StringIO


def source_file(opt):
    def get(_p, _a):
        with open(opt.source_file_path, "r") as f:
            return StringIO(f.read())

    return get


def source_local(opt):
    def get(parser, args):
        commandline = parser.suggest_commandline(args)

        with subprocess.Popen(commandline, stdout=subprocess.PIPE) as proc:
            return StringIO(proc.stdout.read().decode('utf-8'))

    return get


def source_ssh(opt, ssh_args=[]):
    def get(parser, args):
        commandline = ['ssh', opt.source_ssh_hostname] + ssh_args + ['--'] + parser.suggest_commandline(args)

        with subprocess.Popen(commandline, stdout=subprocess.PIPE) as proc:
            return StringIO(proc.stdout.read().decode('utf-8'))

    return get


SOURCES = {
    "file": source_file,
    "local": source_local,
    "ssh": source_ssh,
}
