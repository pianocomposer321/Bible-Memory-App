import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QMessageBox,
    QDialogButtonBox,
    QListWidgetItem
)
from BibleAppModel import BibleAppModel
from BibleAppViewUI import Ui_MainWindow
from ReferenceDialog import Ui_RefDialog

changedFromAdd = False


class BibleAppUI(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.listItems = []


class BibleAppController:

    def __init__(self, view: BibleAppUI, model: BibleAppModel):
        self.view = view
        self.model = model
        self.dialog = None
        self.dialogValue = ''
        self.currentItem = None
        self.currentItemLabel = ''
        self._connectSignals()

    def _connectSignals(self):
        self.view.exitBtn.clicked.connect(self.onExit)
        self.view.addBtn.clicked.connect(self.openDialog)
        self.view.editBtn.clicked.connect(self.onEdit)
        self.view.delBtn.clicked.connect(self.onDel)
        self.view.actionExit.triggered.connect(self.onExit)
        self.view.actionNew_Verse.triggered.connect(self.openDialog)
        self.view.listWidget.currentItemChanged.connect(self.onListItemChanged)
        self.view.listWidget.itemChanged.connect(self.onItemEdited)

    def populateListWidget(self):
        self.model.load_verses()
        for passage in self.model.passages:
            item = QListWidgetItem(passage, self.view.listWidget)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.view.listItems.append(item)

    def openDialog(self):
        self.dialog = DialogUI(self.view)
        self.dialog.show()
        # self.dialog.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.onDialogAccepted)
        b = self.dialog.buttonBox.button(QDialogButtonBox.Ok)
        b.clicked.connect(self.onDialogAccepted)

    def onExit(self):
        self.model.save_verses()
        sys.exit(0)

    def onEdit(self):
        index = self.view.listWidget.currentIndex()
        if index.isValid():
            item = self.view.listWidget.itemFromIndex(index)
            if not item.isSelected():
                item.setSelected(True)
            self.view.listWidget.edit(index)

    def onDel(self):
        currentRow = self.view.listWidget.currentRow()
        self.model.passages.pop(self.currentItem.text())
        self.view.listWidget.takeItem(currentRow)

    def onDialogAccepted(self):
        self.dialogValue = self.dialog.lineEdit.text()

        if self.dialogValue != '':
            if self.dialogValue not in self.model.passages:
                global changedFromAdd
                changedFromAdd = True
                self.model.set_reference(self.dialogValue)
                item = QListWidgetItem(self.dialogValue, self.view.listWidget)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                self.view.listItems.append(item)
            else:
                title = "Error"
                message = "Reference Already Exists"
                print(message)
                QMessageBox.critical(self.dialog, title, message)

    def onListItemChanged(self):
        self.currentItem = self.view.listWidget.currentItem()
        self.currentItemLabel = self.currentItem.text()
        t = self.model.passages[self.currentItemLabel]
        self.view.textEdit.setText('\n\n'.join(t))

    def onItemEdited(self, i):
        global changedFromAdd
        if changedFromAdd:
            changedFromAdd = False
            return
        newtext = i.text()
        self.model.passages.pop(self.currentItemLabel, None)
        self.model.set_reference(newtext)
        t = self.model.passages[newtext]
        self.view.textEdit.setText('\n\n'.join(t))
        self.currentItem = self.view.listWidget.currentItem()
        if self.currentItem:
            self.currentItemLabel = self.currentItem.text()


class DialogUI(QDialog, Ui_RefDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setModal(True)

    def onAccepted(self):
        print(self.lineEdit.text())


def main():
    app = QApplication(sys.argv)
    view = BibleAppUI()
    view.show()
    model = BibleAppModel()
    ctrl = BibleAppController(view, model)
    ctrl.populateListWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
# okay decompiling main.pyc
