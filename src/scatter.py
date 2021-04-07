import logging
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)


def maya_main_window():
    """Return Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter UI Class"""
    def __init__(self):
        """Constructor"""
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumWidth(1000)
        self.setMaximumHeight(500)
        self.setWindowFlags(self.windowFlags() ^
                           QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.source_dd_lay = self._create_source_dd()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.source_dd_lay)
        self.setLayout(self.main_lay)

    def _create_source_dd(self):
        self.source_dd_lbl = QtWidgets.QLabel("Select Source Object")
        self.source_dd = QtWidgets.QComboBox()
        selection = cmds.ls(type="mesh")
        for geo in selection:
            self.source_dd.addItem(geo)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_dd_lbl)
        layout.addWidget(self.source_dd)
        return layout

