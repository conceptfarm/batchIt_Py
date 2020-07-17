# -*- coding: utf-8 -*-

import sys
import os
import traceback
import configparser

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from batchItConfigDialogClass import BatchItConfigDialog

class WorkerSignals(QObject):

	finished = pyqtSignal()
	error = pyqtSignal(tuple)
	result = pyqtSignal(object)
	progressTuple = pyqtSignal(tuple)
	progressInt = pyqtSignal(int)
	progressNone = pyqtSignal()

class Worker(QRunnable):

	def __init__(self, fn, progressType=None, *args, **kwargs):
		super(Worker, self).__init__()

		# Store constructor arguments (re-used for processing)
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()	
		#self.nameFrom = nameFrom
		#self.index = index
		
		# Add the callback to our kwargs
		self.kwargs['progress_callback'] = None
		if progressType == 'tuple':
			self.kwargs['progress_callback'] = self.signals.progressTuple
		elif progressType == 'int':
			self.kwargs['progress_callback'] = self.signals.progressInt
		elif progressType == None:
			self.kwargs['progress_callback'] = self.signals.progressNone
		

	@pyqtSlot()
	def run(self):
		'''
		Initialise the runner function with passed args, kwargs.
		'''
		
		# Retrieve args/kwargs here; and fire processing using them
		try:
			#result = self.fn(self.fileList, self.size, self.i, *self.args, **self.kwargs)
			result = self.fn(*self.args, **self.kwargs)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)  # Return the result of the processing
		finally:
			self.signals.finished.emit()  # Done


class MainWindow(QMainWindow):
	def __init__(self, msFilePath, maxFilePath, maxPaths):
		super().__init__()
		self.msFilePath = msFilePath
		self.maxFilePath = maxFilePath
		self.maxPaths = maxPaths

		self.threadpool = QThreadPool().globalInstance()
		self.threadpool.setMaxThreadCount(1)
		self.maxBatchExec = '"C:\\Program Files\\Autodesk\\3ds Max 2020\\3dsmaxbatch.exe"'
		self.setupUi(self)

	def setupUi(self, MainWindow):
		MainWindow.setObjectName('MainWindow')
		MainWindow.resize(700, 800)
		
		self.centralwidget = QWidget(MainWindow)
		self.centralwidget.setObjectName('centralwidget')
		self.verticalLayout = QVBoxLayout(self.centralwidget)
		self.verticalLayout.setObjectName('verticalLayout')
		
		self.scriptFiles_gl = QGridLayout()
		self.scriptFiles_gl.setContentsMargins(-1, -1, -1, 8)
		self.scriptFiles_gl.setSpacing(6)
		self.scriptFiles_gl.setObjectName('scriptFiles_gl')
		
		self.scriptFiles_list = QListWidget(self.centralwidget)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.scriptFiles_list.sizePolicy().hasHeightForWidth())
		self.scriptFiles_list.setSizePolicy(sizePolicy)
		#self.scriptFiles_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.scriptFiles_list.setObjectName('scriptFiles_list')
	
		self.scriptDir_lbl = QLabel(self.centralwidget)
		self.scriptDir_lbl.setMinimumSize(QSize(140, 22))
		self.scriptDir_lbl.setMaximumSize(QSize(16777215, 22))
		self.scriptDir_lbl.setObjectName('scriptDirlbl')
	
		self.scriptDir_btn = QPushButton(self.centralwidget)
		self.scriptDir_btn.setMinimumSize(QSize(40, 22))
		self.scriptDir_btn.setMaximumSize(QSize(40, 16777215))
		self.scriptDir_btn.setObjectName('scriptDir_btn')
		
		self.scriptDir_txt = QLineEdit(self.msFilePath, self.centralwidget)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.scriptDir_txt.sizePolicy().hasHeightForWidth())
		self.scriptDir_txt.setSizePolicy(sizePolicy)
		self.scriptDir_txt.setObjectName('scriptDir_txt')
		
		self.scriptFiles_lbl = QLabel(self.centralwidget)
		self.scriptFiles_lbl.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
		self.scriptFiles_lbl.setObjectName('scriptFiles_lbl')
		
		self.scriptFiles_gl.addWidget(self.scriptFiles_list, 2, 1, 1, 2)
		self.scriptFiles_gl.addWidget(self.scriptDir_lbl, 0, 0, 1, 1)
		self.scriptFiles_gl.addWidget(self.scriptDir_btn, 0, 2, 1, 1)
		self.scriptFiles_gl.addWidget(self.scriptDir_txt, 0, 1, 1, 1)
		self.scriptFiles_gl.addWidget(self.scriptFiles_lbl, 2, 0, 1, 1)
		self.scriptFiles_gl.setColumnStretch(1, 1)
		
		self.line_top = QFrame(self.centralwidget)
		self.line_top.setMinimumSize(QSize(0, 16))
		self.line_top.setFrameShape(QFrame.HLine)
		self.line_top.setFrameShadow(QFrame.Sunken)
		self.line_top.setObjectName('line_top')
		
		self.processDir_gl = QGridLayout()
		self.processDir_gl.setContentsMargins(-1, 8, -1, -1)
		self.processDir_gl.setSpacing(6)
		self.processDir_gl.setObjectName('processDir_gl')
		
		self.maxFilesDir_txt = QLineEdit(self.maxFilePath, self.centralwidget)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.maxFilesDir_txt.sizePolicy().hasHeightForWidth())
		self.maxFilesDir_txt.setSizePolicy(sizePolicy)
		self.maxFilesDir_txt.setMinimumSize(QSize(0, 22))
		
		
		self.maxFilesDir_txt.setObjectName('maxFilesDir_txt')
		
		self.maxFilesDir_lbl = QLabel(self.centralwidget)
		self.maxFilesDir_lbl.setMinimumSize(QSize(140, 22))
		self.maxFilesDir_lbl.setObjectName('maxFilesDir_lbl')
		
		self.maxFilesDir_btn = QPushButton(self.centralwidget)
		self.maxFilesDir_btn.setMinimumSize(QSize(40, 22))
		self.maxFilesDir_btn.setMaximumSize(QSize(40, 16777215))
		
		
		self.maxFilesDir_btn.setObjectName('maxFilesDir_btn')
		self.processDir_gl.addWidget(self.maxFilesDir_txt, 0, 1, 1, 1)
		self.processDir_gl.addWidget(self.maxFilesDir_lbl, 0, 0, 1, 1)
		self.processDir_gl.addWidget(self.maxFilesDir_btn, 0, 2, 1, 1)
		self.processDir_gl.setColumnStretch(1, 1)
	
		self.maxFilesGet_gl = QGridLayout()
		self.maxFilesGet_gl.setSpacing(6)
		self.maxFilesGet_gl.setObjectName('maxFilesGet_gl')
		
		self.maxFilesRecursive_chb = QCheckBox(self.centralwidget)
		self.maxFilesRecursive_chb.setObjectName('maxFilesRecursive_chb')
		
		self.maxFilesGet_btn = QPushButton(self.centralwidget)
		self.maxFilesGet_btn.setMinimumSize(QSize(80, 22))
		self.maxFilesGet_btn.setObjectName('maxFilesGet_btn')
		
		self.empty_lbl = QLabel(self.centralwidget)
		self.empty_lbl.setMinimumSize(QSize(140, 0))
		self.empty_lbl.setText('')
		self.empty_lbl.setObjectName('empty_lbl')
		
		self.maxFilesGet_gl.addWidget(self.maxFilesRecursive_chb, 0, 2, 1, 1)
		self.maxFilesGet_gl.addWidget(self.maxFilesGet_btn, 0, 1, 1, 1)
		self.maxFilesGet_gl.addWidget(self.empty_lbl, 0, 0, 1, 1)
		self.maxFilesGet_gl.setColumnStretch(2, 1)
		
		self.maxFiles_gl = QGridLayout()
		self.maxFiles_gl.setContentsMargins(-1, 8, -1, 8)
		self.maxFiles_gl.setSpacing(6)
		self.maxFiles_gl.setObjectName('maxFiles_gl')
		self.maxFilesSelectNone_btn = QPushButton(self.centralwidget)
		
		
		self.maxFilesSelectNone_btn.setObjectName('maxFilesSelectNone_btn')
		
		self.maxFilesSearch_lbl = QLabel(self.centralwidget)
		sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.maxFilesSearch_lbl.sizePolicy().hasHeightForWidth())
		self.maxFilesSearch_lbl.setSizePolicy(sizePolicy)
		self.maxFilesSearch_lbl.setMinimumSize(QSize(140, 22))
		self.maxFilesSearch_lbl.setMaximumSize(QSize(16777215, 22))
		
		
		self.maxFilesSearch_lbl.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
		self.maxFilesSearch_lbl.setObjectName('maxFilesSearch_lbl')
		
		self.maxFilesSelectAll_btn = QPushButton(self.centralwidget)
		self.maxFilesSelectAll_btn.setMinimumSize(QSize(140, 0))
		self.maxFilesSelectAll_btn.setObjectName('maxFilesSelectAll_btn')
		
		self.maxFilesSearch_txt = QLineEdit(self.centralwidget)
		self.maxFilesSearch_txt.setEnabled(True)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.maxFilesSearch_txt.sizePolicy().hasHeightForWidth())
		self.maxFilesSearch_txt.setSizePolicy(sizePolicy)
		self.maxFilesSearch_txt.setMinimumSize(QSize(0, 22))
		self.maxFilesSearch_txt.setObjectName('maxFilesSearch_txt')
		
		self.maxFiles_lbl = QLabel(self.centralwidget)
		self.maxFiles_lbl.setMinimumSize(QSize(140, 22))
		self.maxFiles_lbl.setMaximumSize(QSize(16777215, 16777215))
		self.maxFiles_lbl.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
		self.maxFiles_lbl.setObjectName('maxFiles_lbl')
		
		self.maxFiles_list = QListWidget(self.centralwidget)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.maxFiles_list.sizePolicy().hasHeightForWidth())
		self.maxFiles_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.maxFiles_list.setSizePolicy(sizePolicy)
		self.maxFiles_list.setObjectName('maxFiles_list')
		

		self.maxFiles_gl.addWidget(self.maxFilesSearch_lbl, 0, 0, 1, 1)
		self.maxFiles_gl.addWidget(self.maxFilesSearch_txt, 0, 1, 1, 1)
		self.maxFiles_gl.addWidget(self.maxFiles_lbl, 1, 0, 1, 1)
		self.maxFiles_gl.addWidget(self.maxFiles_list, 1, 1, 3, 1)	
		self.maxFiles_gl.addWidget(self.maxFilesSelectAll_btn, 2, 0, 1, 1)
		self.maxFiles_gl.addWidget(self.maxFilesSelectNone_btn, 3, 0, 1, 1)
		self.maxFiles_gl.setColumnStretch(1, 1)
		
		self.line_bottom = QFrame(self.centralwidget)
		self.line_bottom.setMinimumSize(QSize(0, 16))
		self.line_bottom.setFrameShape(QFrame.HLine)
		self.line_bottom.setFrameShadow(QFrame.Sunken)

		
		self.saveMaxFile_gl = QGridLayout()
		self.saveMaxFile_gl.setContentsMargins(-1, 8, -1, -1)
		self.saveMaxFile_gl.setSpacing(6)

		
		self.saveMaxFile_lbl = QLabel(self.centralwidget)
		self.saveMaxFile_lbl.setEnabled(False)
		self.saveMaxFile_lbl.setMinimumSize(QSize(140, 22))
		self.saveMaxFile_lbl.setObjectName('saveMaxFile_lbl')
		
		self.saveMaxFil_txt = QLineEdit(self.centralwidget)
		self.saveMaxFil_txt.setEnabled(False)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.saveMaxFil_txt.sizePolicy().hasHeightForWidth())
		self.saveMaxFil_txt.setSizePolicy(sizePolicy)
		self.saveMaxFil_txt.setMinimumSize(QSize(0, 22))
		self.saveMaxFil_txt.setObjectName('saveMaxFil_txt')
		
		self.saveMaxFileDir_btn = QPushButton(self.centralwidget)
		self.saveMaxFileDir_btn.setEnabled(False)
		self.saveMaxFileDir_btn.setMinimumSize(QSize(40, 22))
		self.saveMaxFileDir_btn.setMaximumSize(QSize(40, 16777215))
		self.saveMaxFileDir_btn.setObjectName('saveMaxFileDir_btn')
		

		self.saveMaxFile_gl.addWidget(self.saveMaxFile_lbl, 0, 0, 1, 1)
		self.saveMaxFile_gl.addWidget(self.saveMaxFil_txt, 0, 1, 1, 1)
		self.saveMaxFile_gl.addWidget(self.saveMaxFileDir_btn, 0, 2, 1, 1)
		
		self.process_gl = QGridLayout()
		self.process_gl.setContentsMargins(-1, -1, -1, 8)
		self.process_gl.setSpacing(6)
		
		self.processDontSave_chb = QCheckBox(self.centralwidget)
		self.processDontSave_chb.setMinimumSize(QSize(150, 0))
		self.processDontSave_chb.setMaximumSize(QSize(150, 16777215))
		self.processDontSave_chb.setChecked(True)
		self.processDontSave_chb.setObjectName('processDontSave_chb')

		self.process_btn = QPushButton(self.centralwidget)
		self.process_btn.setMinimumSize(QSize(80, 22))
		self.process_btn.setMaximumSize(QSize(80, 16777215))
		self.process_btn.setLayoutDirection(Qt.LeftToRight)
		self.process_btn.setObjectName('process_btn')

		self.processOverwrite_chb = QCheckBox(self.centralwidget)
		self.processOverwrite_chb.setEnabled(False)
		self.processOverwrite_chb.setMinimumSize(QSize(180, 0))
		self.processOverwrite_chb.setMaximumSize(QSize(180, 16777215))
		self.processOverwrite_chb.setObjectName('processOverwrite_chb')

		self.processMaxVer_dd = QComboBox(self.centralwidget)
		self.processMaxVer_dd.setMinimumSize(QSize(80, 22))
		self.processMaxVer_dd.setMaximumSize(QSize(100, 16777215))
		self.processMaxVer_dd.setEditable(False)
		self.processMaxVer_dd.setCurrentText('2018')
		self.processMaxVer_dd.setObjectName('processMaxVer_dd')
		
		for key, value in self.maxPaths.items():  
			if value != '' : self.processMaxVer_dd.addItem(key)


		self.processMaxVer_lbl = QLabel(self.centralwidget)
		self.processMaxVer_lbl.setMaximumSize(QSize(80, 16777215))
		self.processMaxVer_lbl.setObjectName('processMaxVer_lbl')
		
		self.process_gl.addWidget(self.processDontSave_chb, 0, 1, 1, 1)
		self.process_gl.addWidget(self.process_btn, 0, 4, 1, 1)
		self.process_gl.addWidget(self.processOverwrite_chb, 0, 0, 1, 1)
		self.process_gl.addWidget(self.processMaxVer_dd, 0, 3, 1, 1)
		self.process_gl.addWidget(self.processMaxVer_lbl, 0, 2, 1, 1)
		self.process_gl.setColumnStretch(4, 1)
		
		self.processBar_gl = QGridLayout()
		self.processBar_gl.setSpacing(6)

		self.progress_pb = QProgressBar(self.centralwidget)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(1)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.progress_pb.sizePolicy().hasHeightForWidth())
		self.progress_pb.setSizePolicy(sizePolicy)
		self.progress_pb.setMinimumSize(QSize(0, 15))
		self.progress_pb.setMaximumSize(QSize(16777215, 15))
		self.progress_pb.setProperty('value', 0)
		self.progress_pb.setAlignment(Qt.AlignCenter)
		self.progress_pb.setObjectName('progress_pb')
		
		self.processBar_gl.addWidget(self.progress_pb, 0, 0, 1, 1)
		
		self.verticalLayout.addLayout(self.scriptFiles_gl)
		self.verticalLayout.addWidget(self.line_top)
		self.verticalLayout.addLayout(self.processDir_gl)
		self.verticalLayout.addLayout(self.maxFilesGet_gl)
		self.verticalLayout.addLayout(self.maxFiles_gl)
		self.verticalLayout.addWidget(self.line_bottom)
		self.verticalLayout.addLayout(self.saveMaxFile_gl)
		self.verticalLayout.addLayout(self.process_gl)
		self.verticalLayout.addLayout(self.processBar_gl)

		self.menubar = QMenuBar(MainWindow)
		self.menubar.setGeometry(QRect(0, 0, 700, 21))
		self.menubar.setObjectName('menubar')
		
		self.menuPreferences = QMenu(self.menubar)
		self.menuPreferences.setObjectName('menuPreferences')

		self.statusbar = QStatusBar(MainWindow)
		self.statusbar.setObjectName('statusbar')
		
		self.actionDo_Something = QAction(MainWindow)
		self.actionDo_Something.setObjectName('actionDo_Something')
		self.actionDo_Another_thing = QAction(MainWindow)
		self.actionDo_Another_thing.setObjectName('actionDo_Another_thing')
		self.menuPreferences.addAction(self.actionDo_Something)
		self.menuPreferences.addSeparator()
		self.menuPreferences.addAction(self.actionDo_Another_thing)
		self.menubar.addAction(self.menuPreferences.menuAction())
		
		MainWindow.setCentralWidget(self.centralwidget)
		MainWindow.setMenuBar(self.menubar)
		MainWindow.setStatusBar(self.statusbar)
		
		#self.scriptDir_btn.clicked.connect(self._printMessage)


		QMetaObject.connectSlotsByName(MainWindow)
		
		self.retranslateUi(MainWindow)
		
		if self.msFilePath != '':
			it = QDirIterator(self.msFilePath, ['*.ms'],  QDir.Files, QDirIterator.NoIteratorFlags)
			self.populateList(self.scriptFiles_list, it)

		self.show()

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle('BatchIt Py')
		
		self.scriptDir_lbl.setText('Scripts Directory:')
		self.scriptFiles_lbl.setText('Select Batch Script to Run:')
		self.maxFilesDir_lbl.setText('Process Directory:')
		self.maxFilesSearch_lbl.setText('Select by file name:')
		self.maxFiles_lbl.setText('Select Max Files to Process:')
		self.saveMaxFile_lbl.setText('Save Max File To:')
		self.processMaxVer_lbl.setText('3dsmax ver:')
		
		self.scriptDir_btn.setText('...')
		self.maxFilesDir_btn.setText('...')
		self.maxFilesGet_btn.setText('Get Files')
		self.maxFilesSelectNone_btn.setText('Select None')
		self.maxFilesSelectAll_btn.setText('Select All')
		self.saveMaxFileDir_btn.setText('...')
		self.process_btn.setText('Process')
				
		self.maxFilesRecursive_chb.setText('Recursive')
		self.processDontSave_chb.setText('Don\'t Save File')
		self.processOverwrite_chb.setText('Overwrite File on Save')
				
		self.menuPreferences.setTitle('Preferences')
		self.actionDo_Something.setText('Do Something')
		self.actionDo_Another_thing.setText('Do Another thing')
	
	
	###################
	# FUNCTIONS
	###################

	def populateList(self, listObject, items):
		while items.hasNext():
			file = items.next()
			tempItem = QListWidgetItem(os.path.basename(file))
			tempItem.setToolTip(file)
			listObject.addItem(tempItem)

	#TODO: write config writer function
	#write to config every time a directory is chosen

	def writeToConfig(self, setting, key, value):
		#config = configparser.ConfigParser()
		config.read('batchItPy.ini')
		config.set(setting, key, value)
		
		with open('batchItPy.ini', 'w') as configfile:
			config.write(configfile)


	###################
	# ACTION EVENTS
	###################

	@pyqtSlot()
	def on_actionDo_Something_triggered(self):
		print('didsomething')

	###################
	# BUTTON EVENTS
	###################

	@pyqtSlot()
	def on_scriptDir_btn_clicked(self):
		defaultDir = self.scriptDir_txt.text() if self.scriptDir_txt.text() != '' else QDir.home().dirName()
		dirPath = QFileDialog.getExistingDirectory(self, 'Select a directory', defaultDir, QFileDialog.ShowDirsOnly)
		
		self.scriptFiles_list.clear()
		
		if dirPath:
			self.scriptDir_txt.setText(dirPath)
			
			it = QDirIterator(dirPath, ['*.ms'],  QDir.Files, QDirIterator.NoIteratorFlags)
			self.populateList(self.scriptFiles_list, it)
			self.writeToConfig('batchItSettings', 'msFilePath', dirPath)


	@pyqtSlot()
	def on_maxFilesDir_btn_clicked(self):
		defaultDir = self.maxFilesDir_txt.text() if self.maxFilesDir_txt.text() != '' else QDir.home().dirName()
		dirPath = QFileDialog.getExistingDirectory(self, 'Select a directory',defaultDir, QFileDialog.ShowDirsOnly)
		
		if dirPath:
			self.maxFilesDir_txt.setText(dirPath)
			self.writeToConfig('batchItSettings', 'maxFilePath', dirPath)

	@pyqtSlot()
	def on_maxFilesGet_btn_clicked(self):
		dirPath = self.maxFilesDir_txt.text()
		self.maxFiles_list.clear()
		
		if self.maxFilesRecursive_chb.isChecked():
			it = QDirIterator(dirPath, ['*.max'],  QDir.Files, QDirIterator.Subdirectories)
		else:
			it = QDirIterator(dirPath, ['*.max'],  QDir.Files, QDirIterator.NoIteratorFlags)
		
		self.populateList(self.maxFiles_list, it)


	@pyqtSlot()
	def on_maxFilesSelectNone_btn_clicked(self):
		self.maxFiles_list.setCurrentRow(0, QItemSelectionModel.Clear)

	@pyqtSlot()
	def on_maxFilesSelectAll_btn_clicked(self):
		for item in range(self.maxFiles_list.count()):
			self.maxFiles_list.setCurrentRow(item, QItemSelectionModel.Select)

	@pyqtSlot()
	def on_saveMaxFileDir_btn_clicked(self):
		dirPath = QFileDialog.getExistingDirectory(self, 'Select a directory', QDir.home().dirName(), QFileDialog.ShowDirsOnly)
		
		if dirPath:
			self.saveMaxFileDir_txt.setText(dirPath)

	@pyqtSlot()	
	def workerFinished(self):
		self.progress_pb.setValue(self.progress_pb.value() + 1)

	def nothing(self):
		print('nothing')

	def maxBatchProcess(self, maxFile, msFile, maxExecPath, progress_callback):
		fString = maxExecPath + ' ' + msFile + ' -sceneFile ' + maxFile
		#subprocess.Popen(fString)
		print(fString)
		return fString

	@pyqtSlot()
	def on_process_btn_clicked(self):
		self.progress_pb.setMaximum(len(self.maxFiles_list.selectedItems()))

		for f in self.maxFiles_list.selectedItems():
			maxFilePath = f.toolTip()
			msFilePath = self.scriptFiles_list.currentItem().toolTip()
			maxExecPath = self.maxPaths[self.processMaxVer_dd.currentText()]
			
			worker = Worker(self.maxBatchProcess, None, maxFilePath, msFilePath, maxExecPath)
			worker.signals.finished.connect(self.workerFinished)
			#worker.signals.result.connect(self.nothing)
			self.threadpool.start(worker)	


	###################
	# TEXT EDIT EVENTS
	###################

	@pyqtSlot(str)
	def on_maxFilesSearch_txt_textEdited(self,text):
		if len(text) >=3:
			self.maxFiles_list.setCurrentRow(0, QItemSelectionModel.Clear)
			for i in range(self.maxFiles_list.count()):
				item = self.maxFiles_list.item(i)
				#print(e, ' ', os.path.basename(f))
				if text.lower() in (item.text().lower()):
					self.maxFiles_list.setCurrentRow(i, QItemSelectionModel.Select)

	###################
	# CHECKBOX EVENTS
	###################

	@pyqtSlot(bool)
	def on_processOverwrite_chb_clicked(self,e):
		print(e)

	@pyqtSlot(bool)
	def on_processDontSave_chb_clicked(self,e):
		print(e)

	@pyqtSlot(bool)
	def on_maxFilesRecursive_chb_clicked(self,e):
		print(e)

	###################
	# LIST EVENTS
	###################
	#scriptFiles_list
	#maxFiles_list


if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	
	config = configparser.ConfigParser()
	config.read('batchItPy.ini')
	configuration = False

	msFilePath = ''
	maxFilePath = ''
	maxPaths = ''
	
	#appIcon = icons.qIconFromBase64(icons.appIconBase64)
	
	try:
		msFilePath = (config['batchItSettings']['msFilePath'])
		maxFilePath = (config['batchItSettings']['maxFilePath'])
	except:
		pass


	try:
		maxPaths = config['3dsMaxPaths']
		configuration = True
	except:
		configDialog = BatchItConfigDialog()
		var = configDialog.exec()
		#return 1 if accepted, 0 if rejected
		if var == 1:
			maxPaths = {'2018':configDialog.le1.text(),'2019':configDialog.le2.text(),'2020':configDialog.le3.text(),'2021':configDialog.le4.text()}
			configuration = True
	
	if configuration == True:
		ex = MainWindow(msFilePath,maxFilePath,maxPaths)


	#ex = MainWindow()
	sys.exit(app.exec_())
