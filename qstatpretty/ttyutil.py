# -*- coding: utf8 -*-

COLOR_BLACK = 30
COLOR_RED = 31
COLOR_GREEN = 32
COLOR_YELLOW = 33
COLOR_BLUE = 34
COLOR_MAGENTA = 35
COLOR_CYAN = 36
COLOR_WHITE = 37

def colortext(t, color, bold=False):
	if not color: return t

	x = 1 if bold else 0
	return "\033[{x};{y}m{text}\033[0m".format(x=x, y=color, text=t)

def pretty_table(tbl, colordef, header_row=True, col_delimiter="│", header_underline="─", header_delimiter="┼", border_l="│", border_tl="┌", border_t="─", border_tr="┐", border_r="│", border_br="┘", border_b="─", border_bl="└", linker_l="├", linker_t="┬", linker_r="┤", linker_b="┴"):

	max_widths = [ max( len(str(c)) for c in col ) for col in zip(*tbl) ]  

	tjust = [ [ "{{:{}s}}".format(w).format(c) for w, c in zip(max_widths, row) ] for row in tbl]

	pretty_top = border_tl + linker_t.join( border_t * w for w in max_widths ) + border_tr + "\n"
	pretty_bottom = border_bl + linker_b.join( border_b * w for w in max_widths ) + border_br 

	if header_row:
		header = tjust.pop(0)
		header = [ colortext(h, COLOR_BLACK, True) for h in header ]

		pretty_colheader = border_l + col_delimiter.join( header ) + border_r
		pretty_underline = linker_l + header_delimiter.join( header_underline * w for w in max_widths) + linker_r
		pretty_header = pretty_colheader + "\n" + pretty_underline + "\n"

		pretty_top = pretty_top + pretty_header 


	tjust = [ [ colortext(t, fmt['color'](t)) for fmt, t in zip(colordef, row) ] for row in tjust ]

	return pretty_top + "".join( border_l + col_delimiter.join( row ) + border_r + "\n" for row in tjust ) + pretty_bottom

def terminal_size():
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
        '1234'))
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

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])
