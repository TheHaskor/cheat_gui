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


def get_line_color_from_csv(file_path='C:/Users\Shahar Haskor\PycharmProjects\cheat_gui\csv_files\params.csv'):
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            color = row['line_color']
            return color


def get_line_size_from_csv(file_path='C:/Users\Shahar Haskor\PycharmProjects\cheat_gui\csv_files\params.csv'):
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            size = row['line_size']
            return int(size)


def get_point_size_from_csv(file_path='C:/Users\Shahar Haskor\PycharmProjects\cheat_gui\csv_files\params.csv'):
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            size = row['point_size']
            return int(size)
