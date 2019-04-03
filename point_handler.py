class Point:
    def __init__(self, x, y, color='blue', size=10):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

    def get_x(self):
        return float(self.x)

    def get_y(self):
        return float(self.y)

    def get_color(self):
        return self.color

    def get_size(self):
        return float(self.size)

    @staticmethod
    def get_range(points):
        range_dict = {'max_x': points[0].get_x(), 'min_x': points[0].get_x(),
                      'max_y': points[0].get_y(), 'min_y': points[0].get_y(), 'num_points': 0}

        range_dict['num_points'] = len(points)
        for point in points:
            if point.get_x() > range_dict.get('max_x'):
                range_dict['max_x'] = point.get_x()
            if point.get_x() < range_dict.get('min_x'):
                range_dict['min_x'] = point.get_x()
            if point.get_y() > range_dict.get('max_y'):
                range_dict['max_y'] = point.get_y()
            if point.get_y() < range_dict.get('min_y'):
                range_dict['min_y'] = point.get_y()
        return range_dict

