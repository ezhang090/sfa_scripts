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
        self.destination_dd_lay = self._create_destination_dd()
        self.scale_ui = self._create_scale_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.source_dd_lay)
        self.main_lay.addLayout(self.destination_dd_lay)
        self.main_lay.addLayout(self.scale_ui)
        self.setLayout(self.main_lay)

    def _create_source_dd(self):
        self.source_dd_lbl = QtWidgets.QLabel("Select Source Object")
        self.source_dd = QtWidgets.QComboBox()
        selection = cmds.ls(type="mesh")
        for geo in selection:
            self.source_dd.addItem(geo)
        self.source_dd.currentIndexChanged.connect(
            self.source_index_changed)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_dd_lbl)
        layout.addWidget(self.source_dd)
        return layout

    def source_index_changed(self):
        cmds.select(self.source_dd.currentText())

    def _create_destination_dd(self):
        self.destination_dd_lbl = QtWidgets.QLabel("Select Destination "
                                                   "Object")
        self.destination_dd = QtWidgets.QComboBox()
        selection = cmds.ls(type="mesh")
        for geo in selection:
            self.destination_dd.addItem(geo)
        self.destination_dd.currentIndexChanged.connect(
            self.destination_index_changed)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.destination_dd_lbl)
        layout.addWidget(self.destination_dd)
        return layout

    def destination_index_changed(self):
        cmds.select(self.destination_dd.currentText(), toggle=True)

    def _create_scale_ui(self):
        layout = self._create_scale_headers()
        self.xscale_lbl = QtWidgets.QLabel("x Scale")
        self.yscale_lbl = QtWidgets.QLabel("y Scale")
        self.zscale_lbl = QtWidgets.QLabel("z Scale")
        layout.addWidget(self.xscale_lbl, 1, 0)
        layout.addWidget(self.yscale_lbl, 2, 0)
        layout.addWidget(self.zscale_lbl, 3, 0)
        return layout

    def _create_scale_headers(self):
        self.min_lbl = QtWidgets.QLabel("Minimum")
        self.min_lbl.setStyleSheet("font: bold")
        self.max_lbl = QtWidgets.QLabel("Maximum")
        self.max_lbl.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.min_lbl, 0, 1)
        layout.addWidget(self.max_lbl, 0, 2)
        return layout
