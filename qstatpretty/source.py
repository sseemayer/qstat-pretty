import subprocess

from io import BytesIO


def source_file(opt):
    def get(_p, _a):
        with open(opt.source_file_path, "rb") as f:
            return BytesIO(f.read())

    return get


def source_local(opt):
    def get(parser, args):
        commandline = parser.suggest_commandline(args)

        try:
            proc = subprocess.Popen(commandline, stdout=subprocess.PIPE)
            res = BytesIO(proc.stdout.read())
        finally:
            proc.stdout.close()

        return res

    return get


def source_ssh(opt, ssh_args=[]):
    def get(parser, args):
        commandline = ['ssh', opt.source_ssh_hostname] + ssh_args + ['--', 'source /etc/profile; ', " ".join("'{0}'".format(a) for a in parser.suggest_commandline(args))]

        try:
            proc = subprocess.Popen(commandline, stdout=subprocess.PIPE)
            res = BytesIO(proc.stdout.read())
        finally:
            proc.stdout.close()

        return res

    return get


SOURCES = {
    "file": source_file,
    "local": source_local,
    "ssh": source_ssh,
}
