import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        loadUi('generator_gui.ui', self)
        self.browse_btn.clicked.connect(self.browse_files)

    def browse_files(self):
        # remember to change the folder where filedialog starts
        file_path = QFileDialog.getOpenFileName(self, 'Choose Summary File Below:', 'C:\\Users\\mcmco\\Desktop\\QuikMed\\Payroll\\Summary', '*.csv')
        fname = file_path[0].split('/')[-1]
        self.file_name.setText(fname)


app = QApplication(sys.argv)
main_window = MainWindow()
#widget = QtWidgets.QStackedWidget()
main_window.show()
app.exec()
