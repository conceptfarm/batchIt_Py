import sys
import os
import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class BatchItConfigDialog(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		
		self.verticalLayout = QVBoxLayout(self)
		self.gridLayoutControlls = QGridLayout()

		self.lbl1 = QLabel()
		self.lbl1.setText('3dsmax 2018 Path')
		self.gridLayoutControlls.addWidget(self.lbl1, 0, 0, 1, 1)
		
		self.btn1 = QPushButton("...")
		self.btn1.setFixedWidth(35)
		self.btn1.clicked.connect(lambda: self.getDir(self.le1))
		self.le1 = QLineEdit()
		self.le1.setReadOnly(True)
		self.gridLayoutControlls.addWidget(self.btn1, 1, 1)
		self.gridLayoutControlls.addWidget(self.le1, 1, 0)

		self.lbl2 = QLabel()
		self.lbl2.setText('3dsmax 2019 Path')
		self.gridLayoutControlls.addWidget(self.lbl2, 2, 0, 1, 1)

		self.btn2 = QPushButton("...")
		self.btn2.setFixedWidth(35)
		self.btn2.clicked.connect(lambda: self.getDir(self.le2))
		self.le2 = QLineEdit()
		self.le2.setReadOnly(True)
		self.gridLayoutControlls.addWidget(self.btn2, 3, 1)
		self.gridLayoutControlls.addWidget(self.le2, 3, 0)

		self.lbl3 = QLabel()
		self.lbl3.setText('3dsmax 2020 Path')
		self.gridLayoutControlls.addWidget(self.lbl3, 4, 0, 1, 1)

		self.btn3 = QPushButton("...")
		self.btn3.setFixedWidth(35)
		self.btn3.clicked.connect(lambda: self.getDir(self.le3))
		self.le3 = QLineEdit()
		self.le3.setReadOnly(True)
		self.gridLayoutControlls.addWidget(self.btn3, 5, 1)
		self.gridLayoutControlls.addWidget(self.le3, 5, 0)

		self.lbl4 = QLabel()
		self.lbl4.setText('3dsmax 2021 Path')
		self.gridLayoutControlls.addWidget(self.lbl4, 6, 0, 1, 1)

		self.btn4 = QPushButton("...")
		self.btn4.setFixedWidth(35)
		self.btn4.clicked.connect(lambda: self.getDir(self.le4))
		self.le4 = QLineEdit()
		self.le4.setReadOnly(True)
		self.gridLayoutControlls.addWidget(self.btn4, 7, 1)
		self.gridLayoutControlls.addWidget(self.le4, 7, 0)
		
		self.gridLayoutOKCancel = QGridLayout()
		self.okCancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.okButton = self.okCancel.button(QDialogButtonBox.Ok)
		self.okButton.setEnabled(False)
		self.okCancel.accepted.connect(self.okPressed)
		self.okCancel.rejected.connect(self.cancelPressed)
		self.gridLayoutOKCancel.addWidget(self.okCancel, 0, 0)

		self.spacerItem = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.gridLayoutOKCancel.addItem(self.spacerItem, 1, 0)

		self.verticalLayout.addLayout(self.gridLayoutControlls)
		self.verticalLayout.addLayout(self.gridLayoutOKCancel)

		self.setWindowTitle("batch It Configuration")
		self.setModal(True)
		self.setFixedWidth(400)
		#self.setWindowIcon(_appIcon)
		self.adjustSize()
		self.setFixedHeight(self.height())

		self.show()
		
	@pyqtSlot()
	def getDir(self, _widget):
		#QFileDialog(parent, caption = QString(), QString &directory, QString &filter = QString())
		dirPath = QFileDialog.getExistingDirectory(self, 'Select a directory', QDir.home().dirName(), QFileDialog.ShowDirsOnly)
		
		if dirPath:
			execPath = os.path.join(dirPath,'3dsmaxbatch.exe')
			if os.path.isfile(execPath):
				_widget.setText('"'+ execPath + '"')

		if self.le1.text() != '' or self.le2.text() != '' or self.le3.text() != '' or self.le4.text() != '':
			self.okButton.setEnabled(True)

	@pyqtSlot()
	def okPressed(self):
		config = configparser.ConfigParser()
		#config.read('batchItPy.ini')
		#config.set('batchItSettings','3dsmax2018Path', self.le1.text())
		config['3dsMaxPaths'] = {'2018':self.le1.text(),'2019':self.le2.text(),'2020':self.le3.text(),'2021':self.le4.text()}
		
		with open('batchItPy.ini', 'w') as configfile:
			config.write(configfile)

		self.accept()

	@pyqtSlot()
	def cancelPressed(self):
		self.reject()

#'''
#use
def main(): 
	app = QApplication(sys.argv)
	ex = BatchItConfigDialog()
	var = ex.exec()
	if var == 1:
		print(var)
		print(ex.le2.text())
		print(ex.le1.text())
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()
#'''
