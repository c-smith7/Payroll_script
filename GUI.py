import sys
import time
import os
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile, QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from format import format_script

class MainWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi('generator_gui.ui', self)
        self.app_icon = QtGui.QIcon()
        self.app_icon.addFile('quikmed-logo.ico', QtCore.QSize(16, 16))
        self.setWindowIcon(self.app_icon)
        self.threadpool = QThreadPool()
        self.payroll_complete.setVisible(False)
        self.prog_bar.setVisible(False)
        self.open_file_btn.setVisible(False)
        self.open_file_btn.setEnabled(False)
        self.browse_btn.clicked.connect(self.browse_files)
        self.generate_btn.clicked.connect(self.generate_slots)
        self.open_file_btn.clicked.connect(self.open_file_btn_clicked)

    def browse_files(self):
        file_path = QFileDialog.getOpenFileName(self, 'Choose Summary File:', 'C:\\Users\\mcmco\\Desktop\\QuikMed\\Payroll\\Summary', '*.csv')
        fname = file_path[0].split('/')[-1]
        self.file_name.setText(fname)

    def generate_payroll(self):
        file = self.file_name.text()
        format_script(file)
        
    def payroll_complete_msg(self):
        self.payroll_complete.setVisible(True)

    def payroll_complete_msg_close(self):
        self.payroll_complete.setVisible(False)

    def progress_bar(self):
        self.prog_bar.setVisible(True)
        for i in range(0, 100):
            self.prog_bar.setValue(i)
            time.sleep(0.007)
        self.prog_bar.setValue(95)
        self.prog_bar.setValue(100)
        time.sleep(0.5)
        self.prog_bar.setVisible(False)

    def open_file_btn_clicked(self):
        os.system('explorer.exe "C:\\Users\\mcmco\\Desktop\\QuikMed\\Payroll\\Final"')
        self.open_file_btn.setEnabled(False)
        self.open_file_btn.setVisible(False)

    def open_file_btn_enabled(self):
        self.open_file_btn.setEnabled(True)
        self.open_file_btn.setVisible(True)
    
        
    def generate_slots(self):
            worker = WorkerThread(self.generate_payroll)
            worker.signal.prog_start.connect(self.progress_bar)
            worker.signal.complete.connect(self.payroll_complete_msg)
            worker.signal.reset.connect(self.payroll_complete_msg_close)
            worker.signal.open_file_btn.connect(self.open_file_btn_enabled)
            self.threadpool.start(worker)


class WorkerSignals(QObject):
    complete = pyqtSignal()
    reset = pyqtSignal()
    prog_start = pyqtSignal()
    open_file_btn = pyqtSignal()



class WorkerThread(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(WorkerThread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signal = WorkerSignals()

    @pyqtSlot()
    def run(self):
            self.fn(*self.args, **self.kwargs)
            time.sleep(0.05)
            self.signal.prog_start.emit()
            time.sleep(1)
            self.signal.complete.emit()
            time.sleep(3)
            self.signal.reset.emit()
            self.signal.open_file_btn.emit()

            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    #widget = QtWidgets.QStackedWidget()
    main_window.show()
    sys.exit(app.exec())