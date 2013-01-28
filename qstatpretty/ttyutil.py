# -*- coding: utf8 -*-

COLOR_BLACK = 30
COLOR_RED = 31
COLOR_GREEN = 32
COLOR_YELLOW = 33
COLOR_BLUE = 34
COLOR_MAGENTA = 35
COLOR_CYAN = 36
COLOR_WHITE = 37


DELIMITERS_DEFAULT = {

	'header_tl'     : "┌",
	'header_t'      : "─",
	'header_tr'     : "┐",
	'header_b'      : "─",
	'header_bl'     : "├",
	'header_l'      : "│",
	'header_r'      : "│",
	'header_br'     : "┤",
	'header_csep_t' : "┬",
	'header_csep_m' : "│",
	'header_csep_b' : "┼",

	'body_r'        : "│",
	'body_br'       : "┘",
	'body_l'        : "│",
	'body_bl'       : "└",
	'body_b'        : "─",
	'body_csep_m'   : "│",
	'body_csep_b'   : "┴",

}


DELIMITERS_MINIMAL = {

	'header_tl'     : "",
	'header_t'      : "",
	'header_tr'     : "",
	'header_b'      : "─",
	'header_bl'     : "",
	'header_l'      : "",
	'header_r'      : "",
	'header_br'     : "",
	'header_csep_t' : "",
	'header_csep_m' : "│",
	'header_csep_b' : "┼",

	'body_r'        : "",
	'body_br'       : "",
	'body_l'        : "",
	'body_bl'       : "",
	'body_b'        : "",
	'body_csep_m'   : "│",
	'body_csep_b'   : "",

}

def colortext(t, color, bold=False):
	if not color: return t

	x = 1 if bold else 0
	return "\033[{x};{y}m{text}\033[0m".format(x=x, y=color, text=t)

def pretty_table(tbl, colordef, header_row=True, delimiters=DELIMITERS_DEFAULT ):
	d = delimiters

	max_widths = [ max( len(str(c)) for c in col ) for col in zip(*tbl) ]  

	tjust = [ [ "{{:{}s}}".format(w).format(c) for w, c in zip(max_widths, row) ] for row in tbl]

	pretty_top = d['header_tl'] + d['header_csep_t'].join( d['header_t'] * w for w in max_widths ) + d['header_tr'] + "\n"
	pretty_bottom = d['body_bl'] + d['body_csep_b'].join( d['body_b'] * w for w in max_widths ) + d['body_br'] 

	if header_row:
		header = tjust.pop(0)
		header = [ colortext(h, COLOR_BLACK, True) for h in header ]

		pretty_colheader = d['header_l'] + d['header_csep_m'].join( header ) + d['header_r']
		pretty_underline = d['header_bl'] + d['header_csep_b'].join( d['header_b'] * w for w in max_widths) + d['header_br']
		pretty_header = pretty_colheader + "\n" + pretty_underline + "\n"

		pretty_top = pretty_top + pretty_header 


	tjust = [ [ colortext(t, fmt['color'](t)) for fmt, t in zip(colordef, row) ] for row in tjust ]

	return pretty_top + "".join( d['body_l'] + d['body_csep_m'].join( row ) + d['body_r'] + "\n" for row in tjust ) + pretty_bottom

def terminal_size():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])
