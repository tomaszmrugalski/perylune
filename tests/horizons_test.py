from astropy import units as u
from perylune import horizons

def test_name_to_horizons_id():

    expected = [
        [ "mars", "499", "majorbody" ],
        [ "eris", "eris", "minorbody "]
    ]

    for case in expected:
        in_name, exp_name, bodytype = case
        print("checking %s" % in_name)
        assert exp_name, bodytype == horizons.name_to_horizons_id(in_name)
