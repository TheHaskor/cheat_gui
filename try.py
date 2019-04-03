from bokeh.plotting import figure, output_file, show, Column
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button
from bokeh.io import show

import numpy as np

import csv_handler
import point_handler


def PolyCoefficients(range_x, coeffs):
    """ Returns a polynomial for ``x`` values for the ``coeffs`` provided.

    The coefficients must be in ascending order (``x**0`` to ``x**o``).
    """
    o = len(coeffs)
    y = 0
    for i in range(o):
        y += coeffs[i] * range_x ** i
    return y


def poly_values(dots_range, coeffs):
    range_x = np.linspace(dots_range['min_x'], dots_range['max_x'], dots_range['num_points']*100)
    dots_x = range_x.tolist()
    dots_y = list(PolyCoefficients(range_x, coeffs))
    return dots_x, dots_y


def button2csv():
    button = Button(label="Download", button_type="success")

    javaScript = """
    function table_to_csv(source) {
        const columns = Object.keys(source.data)
        const nrows = source.get_length()
        const lines = [columns.join(',')]

        for (let i = 0; i < nrows; i++) {
            let row = [];
            for (let j = 0; j < columns.length; j++) {
                const column = columns[j]
                row.push(source.data[column][i].toString())
            }
            lines.push(row.join(','))
        }
        return lines.join('\\n').concat('\\n')
    }


    const filename = 'data_result.csv'
    filetext = table_to_csv(source)
    const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

    //addresses IE
    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, filename)
    } else {
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = filename
        link.target = '_blank'
        link.style.visibility = 'hidden'
        link.dispatchEvent(new MouseEvent('click'))
    }
    """

    button.callback = CustomJS(args=dict(source=source), code=javaScript)
    show(button)


output_file("cheat_gui.html")

points = csv_handler.get_points_from_csv()
dots_range = point_handler.Point.get_range(points)

tools = ["pan", "box_select", "wheel_zoom", "reset"]
p = figure(x_range=(int(dots_range['min_x'])-1, int(dots_range['max_x'])+1),
           y_range=(int(dots_range['min_y'])-1, int(dots_range['max_y'])+1), tools=tools,
           title='cheat_gui')
p.background_fill_color = 'lightgrey'

coeffs = [1, 2]
dots_x_line, dots_y_line = poly_values(dots_range, coeffs)
line_color = csv_handler.get_line_color_from_csv()
line_size = csv_handler.get_line_size_from_csv()
p.line(dots_x_line, dots_y_line, line_width=line_size, color=line_color)

dots_x = []
dots_y = []
dots_color = []
for point in points:
    dots_x.append(point.get_x())
    dots_y.append(point.get_y())
    dots_color.append(point.get_color())

source = ColumnDataSource({
    'x': dots_x, 'y': dots_y, 'color': dots_color
})


renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
columns = [TableColumn(field="x", title="x"),
           TableColumn(field="y", title="y"),
           TableColumn(field='color', title='color')]
table = DataTable(source=source, columns=columns, editable=True, height=200)

draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
p.add_tools(draw_tool)
p.toolbar.active_tap = draw_tool

show(Column(p, table))

button2csv()

