# uncompyle6 version 3.7.2
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:20:19) [MSC v.1925 32 bit (Intel)]
# Embedded file name: ReferenceDialog.py
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RefDialog(object):

    def setupUi(self, RefDialog):
        RefDialog.setObjectName('RefDialog')
        RefDialog.resize(275, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(RefDialog)
        self.verticalLayout.setObjectName('verticalLayout')
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName('formLayout')
        self.lineEdit = QtWidgets.QLineEdit(RefDialog)
        self.lineEdit.setObjectName('lineEdit')
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label = QtWidgets.QLabel(RefDialog)
        self.label.setObjectName('label')
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(RefDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName('buttonBox')
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(RefDialog)
        self.buttonBox.accepted.connect(RefDialog.accept)
        self.buttonBox.rejected.connect(RefDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RefDialog)

    def retranslateUi(self, RefDialog):
        _translate = QtCore.QCoreApplication.translate
        RefDialog.setWindowTitle(_translate('RefDialog', 'Enter Reference...'))
        self.label.setText(_translate('RefDialog', 'Enter Reference:'))
# okay decompiling ReferenceDialog.pyc
