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
