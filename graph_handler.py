import math

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent

import numpy as np

import csv_handler
import point_handler


class DraggablePlotExample(object):
    u""" An example of plot with draggable markers """

    def __init__(self, existing_points, Cgraph, range_dict):
        self._figure, self._axes, self._line = None, None, None
        self._dragging_point = None
        self._points = {}

        self._init_plot(existing_points, Cgraph, range_dict)

    def _init_plot(self, existing_points, Cgraph, range_dict):
        # self._figure = plt.figure("Example plot")
        # axes = plt.subplot(1, 1, 1)
        # axes.set_xlim(int(range_dict['min_x']), int(range_dict['max_x']))
        # axes.set_ylim(int(range_dict['min_y']), int(range_dict['max_y']))
        # plt.xticks(np.linspace(range_dict['min_x'], range_dict['max_x'], range_dict['num_points']).tolist())
        # plt.yticks(np.linspace(range_dict['min_y'], range_dict['max_y'], range_dict['num_points']).tolist())
        # axes.grid(which="both")
        # self._axes = axes
        #
        # self._figure.canvas.mpl_connect('button_press_event', self._on_click)
        # self._figure.canvas.mpl_connect('button_release_event', self._on_release)
        # self._figure.canvas.mpl_connect('motion_notify_event', self._on_motion)
        #
        # # for existing_point in existing_points:
        # #     self._add_point(existing_point.get_x(), existing_point.get_y())
        # #     self._update_plot()
        #
        # # self.plot_poly(range_dict, Cgraph, axes)
        # plt.show()

        self._figure = plt.figure("Example plot")
        axes = plt.subplot(1, 1, 1)
        # abs_max_x = np.max([abs(int(range_dict['min_x'])), abs(int(range_dict['max_x']))])
        # axes.set_xlim(abs_max_x*range_dict['min_x']*20, abs_max_x*range_dict['max_x']*20)
        # abs_max_y = np.max([abs(int(range_dict['min_y'])), abs(int(range_dict['max_y']))])
        # axes.set_ylim(abs_max_y*range_dict['min_y']*20, abs_max_y*range_dict['max_y']*20)
        axes.grid(which="both")
        self._axes = axes

        self._figure.canvas.mpl_connect('button_press_event', self._on_click)
        self._figure.canvas.mpl_connect('button_release_event', self._on_release)
        self._figure.canvas.mpl_connect('motion_notify_event', self._on_motion)

        self.plot_poly(range_dict, Cgraph, axes)

        for existing_point in existing_points:
            self._add_point(existing_point.get_x(), existing_point.get_y())
        self._update_plot()

        plt.show()


    def _update_plot(self, color='blue', size=10):
        if not self._points:
            self._line.set_data([], [])
        else:
            x, y = zip(*sorted(self._points.items()))
            # Add new plot
            if not self._line:
                self._line, = self._axes.plot(x, y, color, marker="o", markersize=size)
                self._line.set_linewidth(0)
            # Update current plot
            else:
                self._line.set_data(x, y)
        self._figure.canvas.draw()
        print(self._points) # TODO: change to copy to csv

    def _add_point(self, x, y=None):
        if isinstance(x, MouseEvent):
            x, y = int(x.xdata), int(x.ydata)
        self._points[x] = y
        return x, y

    def _remove_point(self, x, _):
        if x in self._points:
            self._points.pop(x)

    def _find_neighbor_point(self, event):
        u""" Find point around mouse position
        :rtype: ((int, int)|None)
        :return: (x, y) if there are any point around mouse else None
        """
        distance_threshold = 0.01
        nearest_point = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for x, y in self._points.items():
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (x, y)
        if min_distance < distance_threshold:
            return nearest_point
        return None

    def _on_click(self, event):
        u""" callback method for mouse click event
        :type event: MouseEvent
        """
        # left click
        if event.button == 1 and event.inaxes in [self._axes]:
            # point = self._find_neighbor_point(event)
            # if point:
            #     self._dragging_point = point
            #     self._remove_point(*point)
            # else:
            #     self._add_point(event)
            self._add_point(event)
            self._update_plot()
        # right click
        elif event.button == 3 and event.inaxes in [self._axes]:
            point = self._find_neighbor_point(event)
            if point:
                self._remove_point(*point)
                self._update_plot()

    def _on_release(self, event):
        u""" callback method for mouse release event
        :type event: MouseEvent
        """
        if event.button == 1 and event.inaxes in [self._axes] and self._dragging_point:
            self._add_point(event)
            self._dragging_point = None
            self._update_plot()

    def _on_motion(self, event):
        u""" callback method for mouse motion event
        :type event: MouseEvent
        """
        if not self._dragging_point:
            return
        self._remove_point(*self._dragging_point)
        self._dragging_point = self._add_point(event)
        self._update_plot()

    def PolyCoefficients(self, range_x, coeffs):
        """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

        The coefficients must be in ascending order (``x**0`` to ``x**o``).
        """
        o = len(coeffs)
        y = 0
        for i in range(o):
            y += coeffs[i] * range_x ** i
        return y

    def plot_poly(self, range_dict, coeffs, axes):
        range_x = np.linspace(range_dict['min_x'], range_dict['max_x'], range_dict['num_points'] * 100)
        axes.plot(range_x, self.PolyCoefficients(range_x, coeffs))


if __name__ == "__main__":
    points = csv_handler.get_points_from_csv()
    coeffs = [1, 2, 3, 4, 5]
    range_dict = csv_handler.get_range(points)
    plot = DraggablePlotExample(points, coeffs, range_dict)


