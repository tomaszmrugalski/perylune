from perylune import utils

def test_url_to_filename():
    # Tests if URL can be properly converted to a filename
    values = [ ['https://celestrak.com/NORAD/elements/active.txt', 'celestrak.com-NORAD-elements-active.txt'],
               ['ftp://isc.org/foo.txt', 'isc.org-foo.txt'] ]

    for _, row in enumerate(values):
        assert utils.url_to_filename(row[0]) == row[1]
