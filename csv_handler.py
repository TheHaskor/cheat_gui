import csv


def get_points_from_csv(file_path='C:/Users\Shahar Haskor\PycharmProjects\cheat_gui\csv_files\OldPoints.csv'):
    points = []
    import point_handler
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            x_value = row['x']
            y_value = row['y']
            points.append(point_handler.Point(x_value, y_value))
    return points


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


m = get_points_from_csv()
r = get_range(m)
print(2)