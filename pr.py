from PyQt6.QtWidgets import QMainWindow, QDialog, QApplication
from PyQt6 import uic
import sys 

class cosmos(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("cosmo_dialog.ui", self)

        if QDialog.exec() == QDialog.DialogCode.Accepted:
         
        
        
        


