# importing Qt widgets
from datetime import datetime

from PyQt5.QtWidgets import *
import sys

# importing pyqtgraph as pg
import pyqtgraph as pg
from pyqtgraph import debug as debug


class TimeAxisItem(pg.AxisItem):
    hide_ticks = 0

    def __init__(self, *args, **kwargs):
        super(TimeAxisItem, self).__init__(*args, **kwargs)
        # Paint tick every 1 second
        self.setTickSpacing(levels=[(1, 0)])
        # Paint tick every 1 minute
        # self.setTickSpacing(levels=[(60, 0)])
        # Set fixed tick height
        self.fixedHeight = 150

    def tickStrings(self, values, scale, spacing):
        return [int2dt(value).strftime("%Y-%m-%d %H:%M:%S") for value in values]

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs):

        profiler = debug.Profiler()

        p.setRenderHint(p.RenderHint.Antialiasing, False)
        p.setRenderHint(p.RenderHint.TextAntialiasing, True)

        ## draw long line along axis
        pen, p1, p2 = axisSpec
        p.setPen(pen)
        p.drawLine(p1, p2)
        # p.translate(0.5,0)  ## resolves some damn pixel ambiguity

        ## draw ticks
        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)
        profiler('draw ticks')

        # Draw all text
        if self.style['tickFont'] is not None:
            p.setFont(self.style['tickFont'])
        p.setPen(self.textPen())
        bounding = self.boundingRect().toAlignedRect()
        p.setClipRect(bounding)
        for rect, flags, text in textSpecs:
            p.save()  # save the painter state
            p.translate(rect.center())  # move coordinate system to center of text rect
            p.rotate(-90)  # rotate text
            p.translate(-rect.center())  # revert coordinate system
            p.translate(-65, 0)  # Move rotated tick down by 65 pixels
            p.drawText(rect, int(flags), text)
            p.restore()  # restore the painter state

        profiler('draw text')

    def tickValues(self, minVal, maxVal, size):
        if minVal == 0:
            return []
        else:
            ticks = super().tickValues(minVal, maxVal, size)
            ticks = [(1.0, ticks[0][1][self.hide_ticks:])]
            return ticks


def int2dt(ts):
    return datetime.fromtimestamp(ts)


class MyPlotWidget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        if self.plotItem.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)
            x = round(mousePoint.x())
            if x == 1:
                Result = "Jan"
            else:
                Result = x
            y = round(mousePoint.y(), 1)
            QToolTip.showText(self.mapToGlobal(pos), f"x={Result}, y={y}")
        else:
            QToolTip.hideText()


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("PyQtGraph")

        # setting geometry
        self.setGeometry(100, 100, 600, 500)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):
        # creating a widget object
        widget = QWidget()

        # creating a push button object
        btn = QPushButton('Push Button')
        btn.clicked.connect(self.update)

        # creating a line edit widget
        text = QLineEdit("Line Edit")

        # creating a check box widget
        check = QCheckBox("Check Box")

        # creating a plot window
        self.plot = MyPlotWidget()

        xdict = {0: 'Jan', 1: 'Feb', 2: 'Mar', 3: 'Apr', 4: 'May', 5: 'Jun', 6: 'Jul', 7: 'Aug', 8: 'Sep', 9: 'Oct',
                 10: 'Nov', 11: 'Dec'}
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        self.plot.setAxisItems(axisItems={'bottom': stringaxis})

        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # create list for y-axis
        y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2, 1, 1]

        # create horizontal list i.e x-axis
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        # create pyqt5graph bar graph item
        # with width = 0.6
        # with bar colors = green
        bargraph = pg.BarGraphItem(x=x, height=y1, width=0.9, brush='g')

        # add item to plot window
        # adding bargraph item to the plot window
        self.plot.addItem(bargraph)

        # Creating a grid layout
        layout = QGridLayout()

        # setting this layout to the widget
        widget.setLayout(layout)

        # adding widgets in the layout in their proper positions
        # button goes in upper-left
        layout.addWidget(btn, 0, 0)

        # text edit goes in middle-left
        layout.addWidget(text, 1, 0)

        # check box widget goes in bottom-left
        layout.addWidget(check, 3, 0)

        # plot window goes on right side, spanning 3 rows
        layout.addWidget(self.plot, 0, 1, 3, 1)

        # setting this widget as central widget of the main window
        self.setCentralWidget(widget)

    def update(self):
        self.plot.clear()
        self.plot.setMouseEnabled(x=False, y=False)


        x = [0,1, 2, 3, 4, 5, 6,7,8,9,10,11]
        import random

        # Generate 12 random numbers between 0 and 12
        y1 = [random.randint(0, 100) for _ in range(12)]
        # y1 = [10, 2, 3, 4, 5, 6,7,8,9,10,11,12]

        # create pyqt5graph bar graph item
        # with width = 0.6
        # with bar colors = green
        bargraph = pg.BarGraphItem(x=x, height=y1, width=0.6, brush='g')
        # Get the y-axis values
        y_values = bargraph.y()
        print(y_values)

        # add item to plot window
        # adding bargraph item to the plot window
        self.plot.addItem(bargraph)


if __name__ == "__main__":
    import sys

    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # start the app
    sys.exit(App.exec())
