import datetime
import matplotlib
from PyQt5.QtWidgets import QLabel
from mplcursors import cursor

matplotlib.use('Qt5Agg')
from Database import Log

from PyQt5 import QtWidgets
from datetime import datetime

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure


def strToDate(date_string):
    # date_string = "2022-03-05"
    date_format = "%Y-%m-%d"
    date_object = datetime.strptime(date_string, date_format)
    return date_object


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
        self.bargraph()

        self.show()

    def line(self):
        # self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=5))
        # self.canvas.axes.xaxis.set_major_locator(FixedLocator([15500, 16500, 17500, 18500, 19500]))
        from Database.Statement import Statement
        Statement = Statement()
        # self.cursor = mplcursors.cursor(self.canvas.axes, hover=True)
        # self.cursor.connect("add", lambda sel: sel.annotation.set_text(
        #     f"{sel.artist.get_xdata()[sel.target.index]:.2f}, {sel.artist.get_ydata()[sel.target.index]:.2f}"))
        ValueSelect = "Gold"
        data = Statement.traverse_all_dates(ValueSelect, Preset="Month", Mode=None)
        # Define the format of the date string
        # format_str = '%Y-%m-%d'
        # # Convert each dictionary key to a datetime object
        # for key in data:
        #     datetime_obj = datetime.datetime.strptime(key, format_str)
        #     data[datetime_obj] = data.pop(key)
        # print(data)
        x = list(data.keys())
        y = list(data.values())
        print(x)
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
        self.canvas.axes.set_xlabel('Date')
        self.canvas.axes.set_ylabel(ValueSelect)

        # # Format the x-axis ticks as dates
        date_format = mdates.DateFormatter('%Y-%m-%d')
        self.canvas.axes.xaxis.set_major_formatter(date_format)
        self.canvas.axes.xaxis.set_major_locator(mdates.DayLocator())

    def hist(self):
        # self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=5))
        # self.canvas.axes.xaxis.set_major_locator(FixedLocator([15500, 16500, 17500, 18500, 19500]))
        from Database.Statement import Statement
        Statement = Statement()
        # self.cursor = mplcursors.cursor(self.canvas.axes, hover=True)
        # self.cursor.connect("add", lambda sel: sel.annotation.set_text(
        #     f"{sel.artist.get_xdata()[sel.target.index]:.2f}, {sel.artist.get_ydata()[sel.target.index]:.2f}"))
        data = Statement.traverse_all_dates("BoughtFor", StartDate=strToDate("2022-01-01"),
                                            EndDate=strToDate("2023-03-31"))
        # Define the format of the date string
        # format_str = '%Y-%m-%d'
        # # Convert each dictionary key to a datetime object
        # for key in data:
        #     datetime_obj = datetime.datetime.strptime(key, format_str)
        #     data[datetime_obj] = data.pop(key)
        # print(data)
        x = list(data.keys())
        y = list(data.values())
        self.canvas.axes.hist(x, bins=12, edgecolor="k")

    def pie(self):
        Money = Log.Log.Money()
        Money.setProfile("ma")
        data = Money.dataforgraph()
        # print(data)
        # data = {'C': 20, 'C++': 15, 'Java': 30,
        #         'Python': 35}
        # courses = list(data.keys())
        # values = list(data.values())
        cursor(hover=True)
        data_without_zero = {k: v for k, v in data.items() if v > 0}
        names = list(data_without_zero.keys())
        values = list(data_without_zero.values())
        # explode = (0.1,0.1)
        wp = {'linewidth': 1, 'edgecolor': "black"}
        _, _, autotexts = self.canvas.axes.pie(values, labels=[''] * len(values), shadow=True, autopct='%1.1f%%',
                                               wedgeprops=wp, pctdistance=1.3)
        # create legend labels with percentages
        legend_labels = [f'{label} ({values[i]:.1f})' for i, label in enumerate(names)]
        self.canvas.axes.legend(legend_labels, loc='best')
        # self.canvas.axes.legend(bars, names, loc="best")

    def bargraph(self):
        from Database.Statement import Statement
        Statement = Statement()
        # self.cursor = mplcursors.cursor(self.canvas.axes, hover=True)
        # self.cursor.connect("add", lambda sel: sel.annotation.set_text(
        #     f"{sel.artist.get_xdata()[sel.target.index]:.2f}, {sel.artist.get_ydata()[sel.target.index]:.2f}"))
        ValueSelect = "Gold"
        data = Statement.traverse_all_dates(ValueSelect, Preset="Month", Mode=None)
        x = list(data.keys())
        y = list(data.values())

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
        self.canvas.axes.axhline(y=0, color='black', linestyle='-')
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