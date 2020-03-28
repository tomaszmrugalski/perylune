#/
from poliastro.czml.extract_czml import CZMLExtractor
from poliastro.examples import iss, molniya  # noqa: E402

start_epoch = iss.epoch
end_epoch = iss.epoch + molniya.period

sample_points = 100

extractor = CZMLExtractor(start_epoch, end_epoch, sample_points)

extractor.add_orbit(
    molniya, rtol=1e-4, label_text="Molniya", label_fill_color=[125, 80, 120, 255]
)
extractor.add_orbit(iss, rtol=1e-4, label_text="ISS", path_show=False)

f = open("molniya100.czml", "w")
f.write(repr(extractor.packets))
f.close()
