from osmium.osm import Location


def distance(a: Location, b: Location):
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5
