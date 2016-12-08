def days_in_month(m, y):  # m is 1 indexed: 1-12
    if m == 2:
        return 29 if (y % 4 == 0 and y % 100) or y % 400 == 0 else 28
    elif m in [9, 4, 6, 11]:
        return 30
    else:
        return 31


def is_valid_date(d, m, y):
    return 0 < m <= 12 and 0 < d <= days_in_month(m, y) and 1957 <= y < 2100


class OrbitGraph():
    def __init__(self, orbit_list):
        self.edges = {}
