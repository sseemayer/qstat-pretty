import qstatpretty.ttyutil.table as ttytable
import qstatpretty.ttyutil.resize as ttyresize
import qstatpretty.ttyutil.size as ttysize


def job_table(jobs, table_format):
    header = [col['title'] for col in table_format]
    body = [[job[col['key']]
             if col['key'] in job and str(job[col['key']]) else ""
             for col in table_format]
            for job in jobs]

    return [header] + body


def pretty_table(jobs, table_format, terminal_width=ttysize.terminal_size()[0], table_algorithm=None, delimiters=ttytable.DELIMITERS_MINIMAL):

    if not jobs:
        return

    tbl = job_table(jobs, table_format)
    tbl, delimiters = table_algorithm(tbl, terminal_width, table_format, delimiters)
    print(ttytable.pretty_table(tbl, table_format, delimiters=delimiters))
