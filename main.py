from PyQt6.QtWidgets import QMainWindow, QApplication,QFileDialog,QMessageBox
import sys
from NotePad import Ui_MainWindow
from PyQt6.QtPrintSupport import QPrinter,QPrintDialog
from PyQt6.QtCore import QFileInfo
class NotePadWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.actionSave.triggered.connect(self.saveFile)
        self.actionNew.triggered.connect(self.fileNew)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionPrint.triggered.connect(self.printFile)
        self.actionExport_PDF.triggered.connect(self.exportFdf)
        self.actionExit.triggered.connect(self.exitApp)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionAbout_app.triggered.connect(self.about)
    def isSaved(self):
        if not self.textEdit.document().isModified():
            return True

        ret = QMessageBox.warning(self,"Application","The document has been modified.\n Do you want to save ?",
        QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard)

        if ret == QMessageBox.StandardButton.Save:
            return self.saveFile()
        if ret == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def exportFdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Export PDF')
        if fn != "":
            if QFileInfo(fn).suffix() == "" : fn += '.pdf'
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)
    def saveFile(self):
        filename = QFileDialog.getSaveFileName(self,"save File")
        if filename[0]:
            f = open(filename[0],'w')\

            with f:
                text = self.textEdit.toPlainText()
                f.write(text)
                QMessageBox.about(self,"save file","file has been saved")


    def fileNew(self):
        if self.isSaved():
            self.textEdit.clear()

    def openFile(self):
        fName = QFileDialog.getOpenFileName(self,"Open File")
        if fName[0]:
            f = open(fName[0],'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

    def printFile(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)
    def exitApp(self):
        self.close()

    def about(self):
        QMessageBox.about(self,"About app","This is simple notepad app with PyQt6")

app = QApplication(sys.argv)
note = NotePadWindow()

sys.exit(app.exec())