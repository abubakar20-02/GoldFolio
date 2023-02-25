import datetime
import sys
import random
import matplotlib
import mplcursors
from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QToolTip, QLabel
from mplcursors import cursor

matplotlib.use('Qt5Agg')
import Log

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import yfinance as yf
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import FixedLocator


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.setCentralWidget(self.canvas)
        self.tooltip = QLabel(self)
        self.tooltip.hide()

        # n_data = 50
        # self.xdata = list(range(n_data))
        # self.ydata = [random.randint(0, 10) for i in range(n_data)]
        self.line()

        self.show()

    def line(self):
        # self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=5))
        # self.canvas.axes.xaxis.set_major_locator(FixedLocator([15500, 16500, 17500, 18500, 19500]))
        from Investment import Investment
        Investment = Investment()
        # self.cursor = mplcursors.cursor(self.canvas.axes, hover=True)
        # self.cursor.connect("add", lambda sel: sel.annotation.set_text(
        #     f"{sel.artist.get_xdata()[sel.target.index]:.2f}, {sel.artist.get_ydata()[sel.target.index]:.2f}"))
        data = Investment.traverse_all_dates("BoughtFor")
        # Define the format of the date string
        # format_str = '%Y-%m-%d'
        # # Convert each dictionary key to a datetime object
        # for key in data:
        #     datetime_obj = datetime.datetime.strptime(key, format_str)
        #     data[datetime_obj] = data.pop(key)
        # print(data)
        x = list(data.keys())
        y = list(data.values())
        print(y)
        # x = [datetime.datetime(2022, 1, 1, 0, 0),
        #      datetime.datetime(2022, 1, 2, 0, 0),
        #      datetime.datetime(2022, 1, 3, 0, 0),
        #      datetime.datetime(2022, 1, 4, 0, 0),
        #      datetime.datetime(2022, 1, 5, 0, 0)]
        self.canvas.axes.set_xticks(x)
        self.canvas.axes.set_xticklabels(x, rotation=90)
        # x = [1, 2, 3, 4, 5]
        # y = [1850, 1800, 1900, 1950, 1750]
        self.canvas.axes.plot(x, y, '-o')
        self.canvas.axes.grid(True)
        self.canvas.axes.set_xlabel('X-axis')
        self.canvas.axes.set_ylabel('Y-axis')

        # # Format the x-axis ticks as dates
        date_format = mdates.DateFormatter('%Y-%m-%d')
        self.canvas.axes.xaxis.set_major_formatter(date_format)
        self.canvas.axes.xaxis.set_major_locator(mdates.DayLocator())

    def pie(self):
        Money = Log.Log.Money()
        Money.setProfile("ma")
        data = Money.dataforgraph()
        type1 = list(data.keys())
        values = list(data.values())
        # print(data)
        # data = {'C': 20, 'C++': 15, 'Java': 30,
        #         'Python': 35}
        # courses = list(data.keys())
        # values = list(data.values())
        cursor(hover=True)
        explode = (0.1, 0.1, 0.1, 0.1)
        wp = {'linewidth': 1, 'edgecolor': "black"}
        bars = self.canvas.axes.pie(values, labels=type1, shadow=True, autopct='%1.0f%%', pctdistance=1.1,
                                    labeldistance=1.2, explode=explode, wedgeprops=wp)

    def bargraph(self):
        Money = Log.Log.Money()
        Money.setProfile("ma")
        data = Money.dataforgraph()
        type1 = list(data.keys())
        values = list(data.values())
        # print(data)
        # data = {'C': 20, 'C++': 15, 'Java': 30,
        #         'Python': 35}
        # courses = list(data.keys())
        # values = list(data.values())
        cursor(hover=True)
        bars = self.canvas.axes.bar(type1, values)
        for bars in self.canvas.axes.containers:
            self.canvas.axes.bar_label(bars)
        self.canvas.axes.set_title('Bar Graph Example')
        self.canvas.axes.set_xlabel('X-axis')
        self.canvas.axes.set_ylabel('Y-axis')
        self.plotarea = self.canvas.figure.subplotpars.left, self.canvas.figure.subplotpars.top
        self.plotarea = self.canvas.figure.transFigure.transform(self.plotarea)

        # self.canvas.mpl_connect('motion_notify_event', self.on_move)

    #     # Setup a timer to trigger the redraw by calling update_plot.
    #     self.timer = QtCore.QTimer()
    #     self.timer.setInterval(10000)
    #     self.timer.timeout.connect(self.update_plot)
    #     self.timer.start()
    #
    # def update_plot(self):
    #     # Drop off the first y element, append a new one.
    #     self.ydata = self.ydata[1:] + [random.randint(0, 10)]
    #     self.canvas.axes.cla()  # Clear the canvas.
    #     self.canvas.axes.plot(self.xdata, self.ydata, 'r')
    #     # Trigger the canvas to update and redraw.
    #     self.canvas.draw()

    # def on_move(self, event):
    #     if event.inaxes == self.canvas.axes:
    #         x, y = event.xdata, event.ydata
    #         self.tooltip.setText(f'x={round(x)}, y={round(y)}')
    #         self.tooltip.move(event.x, self.canvas.height()-event.y)
    #         self.tooltip.show()
    #     else:
    #         self.tooltip.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
