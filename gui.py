from PyQt5 import QtWidgets
from mydesign import Ui_MainWindow
from util import Task
import pyqtgraph as pg
import sys

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.task = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.graphWidget = pg.PlotWidget()
        self.ui.layoutGraph.addWidget(self.graphWidget)
        self.graphWidget.setBackground('w')
        self.graphWidget.setLabel('left', 'Температура (К)', color='red', size=30)
        self.graphWidget.setLabel('bottom', 'Длина (см)', color='red', size=30)
        self.ui.label_current_time.setText("Индекс времени k = " + str(0))
        self.ui.sliderImage.valueChanged.connect(self.plotNextGraph)
        self.ui.buttonCaluclate.clicked.connect(self.calculate)
        self.ui.buttonClear.clicked.connect(self.clear)
        self.l = pg.LegendItem((160, 60), offset=(430, 10))
        self.l.setParentItem(self.graphWidget.graphicsItem())


    def clear(self):
        self.ui.edit_l.setText("")
        self.ui.edit_D.setText("")
        self.ui.edit_s.setText("")
        self.ui.edit_c.setText("")
        self.ui.edit_T.setText("")
        self.ui.edit_alpha.setText("")
        self.ui.edit_K.setText("")
        self.ui.edit_I.setText("")
        self.graphWidget.clear()
        self.task = None
        self.ui.label_gridInfo.setStyleSheet("color: rgb(0, 0, 0);")
        self.ui.label_gridInfo.setText("")
        self.ui.label_max_t.setText("0")
        self.ui.sliderImage.setMaximum(0)
        self.ui.label_current_time.setText("Индекс времени k = " + str(0))

    def legend_del(self):
        while (len(self.l.items)):
            item, label = self.l.items[0]
            self.l.items.remove((item, label))  # удалить линию
            self.l.layout.removeItem(item)
            item.close()
            self.l.layout.removeItem(label)  # удалить надпись
            label.close()
            self.l.updateSize()

    def calculate(self):
        self.ui.label_gridInfo.setStyleSheet("color: rgb(0, 0, 0);")
        self.ui.label_gridInfo.setText("")
        try:
            l =     float(self.ui.edit_l.text())
            D =     float(self.ui.edit_D.text())
            s =     float(self.ui.edit_s.text())
            c =     float(self.ui.edit_c.text())
            T =     float(self.ui.edit_T.text())
            alpha = float(self.ui.edit_alpha.text())
            K =     int(  self.ui.edit_K.text())
            I =     int(  self.ui.edit_I.text())
            self.ui.label_gridInfo.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_gridInfo.setText("Идут вычисления. Подождите.")
            self.task = Task(l, D, c, s, alpha, T, I, K)
            answer = self.task.calculate()
            answer_analytic = self.task.analytic_decision()
            self.ui.label_gridInfo.setText("Готово!")
            y = answer[0]
            x = self.task.x
            self.ui.sliderImage.setValue(0)
            self.ui.label_max_t.setText(str(len(answer) - 1))
            self.ui.sliderImage.setMaximum(len(answer) - 1)
            self.graphWidget.clear()
            self.legend_del()
            self.plotGraph(x, answer_analytic[0], "Температура при t=0", 'b')
            self.plotGraph(x, y, "Температура при t=0", 'r')
            self.ui.label_gridInfo.setText(self.ui.label_gridInfo.text() +
                                           "\nabsolute error: " + str(self.task.calculateAbsError()) +
                                           "\nРешение устойчиво: " + str(self.task.isStable()))

        except ValueError:
            self.ui.label_gridInfo.setStyleSheet("color: rgb(255, 0, 0);")
            self.ui.label_gridInfo.setText("Проверьте поля!")

    def plotNextGraph(self):
        self.legend_del()
        t = self.ui.sliderImage.value()
        self.ui.label_current_time.setText("Индекс времени k = " + str(t))
        if(self.task != None):
            y = self.task.answer[t]
            x = self.task.x
            self.graphWidget.clear()
            self.plotGraph(x, self.task.answer_analytic[t],
                           "Аналитическое решение при t=" + str(round(t * self.task.ht, 1)) + " c", 'b')
            self.plotGraph(x, y, "Явная схема при t=" + str(round(t * self.task.ht, 1)) + " c", 'r')

    def plotGraph(self, x, y, plotname, color):
        self.graphWidget.showGrid(x=True, y=True)
        pen = pg.mkPen(color=color, width=3)
        self.l.addItem(self.graphWidget.plot(x, y, name=plotname, pen=pen), plotname)



app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())

