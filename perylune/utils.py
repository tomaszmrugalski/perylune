


def coords(lon, lat):
    t = "%2.4f" % lat
    if (lat>0):
        t += "N"
    else:
        t += "S"

    t += " %2.4f" % lon
    if (lon>0):
        t += "E"
    else:
        t += "W"
    return t

def is_safe_filename_character(c: str) -> bool:
    return c.isalpha() or c.isdigit() or c in ('.', '-', '_')

def safe_filename(filename: str, replacement: str="_") -> str:
    chars = [c if is_safe_filename_character(c) else replacement for c in filename]
    return "".join(chars).rstrip()

def url_to_filename(url: str) -> str:
    """Returns a filename based on URL"""
    # First we need to get rid of the
    s = url[url.find("//")+2:]
    s = safe_filename(s, "-")

    return s
