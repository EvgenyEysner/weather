import config

from dataclasses import dataclass
from subprocess import Popen, PIPE
from exceptions import CantGetCoordinates


@dataclass(slots=True, frozen=True)
class Coordinates:
    longitude: float
    latitude: float


def get_gps_coordinates() -> Coordinates:
    """Returns current coordinates using MacBook GPS"""
    process = Popen(["whereami"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    output_lines = output.decode().strip().lower().split("\n")

    latitude = longitude = None
    for line in output_lines:
        if line.startswith("latitude:"):
            latitude = float(line.split()[1])
        if line.startswith("longitude:"):
            longitude = float(line.split()[1])
    if config.USE_ROUNDED_COORDS:  # Добавили округление координат
        latitude, longitude = map(lambda c: round(c, 1), [latitude, longitude])
        return Coordinates(longitude=longitude, latitude=latitude)


if __name__ == "__main__":
    print(get_gps_coordinates())
