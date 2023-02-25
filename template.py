import datetime
import sys
import random
import matplotlib

matplotlib.use('Qt5Agg')
import Log

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import yfinance as yf


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

        # n_data = 50
        # self.xdata = list(range(n_data))
        # self.ydata = [random.randint(0, 10) for i in range(n_data)]
        self.bargraph()

        self.show()

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
        bars = self.canvas.axes.bar(type1, values)
        self.canvas.axes.set_title('Bar Graph Example')
        self.canvas.axes.set_xlabel('X-axis')
        self.canvas.axes.set_ylabel('Y-axis')

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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
