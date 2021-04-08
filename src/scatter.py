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
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                           QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.source_dd_lay = self._create_source_dd()
        self.destination_dd_lay = self._create_destination_dd()
        self.input_ui = self._create_input_ui()
        self.button_lay = self._create_button_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.source_dd_lay)
        self.main_lay.addLayout(self.destination_dd_lay)
        self.main_lay.addLayout(self.input_ui)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    @QtCore.Slot()
    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter_objects)

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    def _create_source_dd(self):
        """create dropdown menu to select source object"""
        self.source_dd_lbl = QtWidgets.QLabel("Select Source Object")
        self.source_dd = QtWidgets.QComboBox()
        selection = cmds.ls(type="mesh")
        self.source_dd.addItem("Please Select Object")
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
        """create dropdown menu to select destination object"""
        self.destination_dd_lbl = QtWidgets.QLabel("Select Destination "
                                                   "Object")
        self.destination_dd = QtWidgets.QComboBox()
        selection = cmds.ls(type="mesh")
        self.destination_dd.addItem("Please Select Object")
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

    def _create_input_ui(self):
        layout = self._create_input_headers()
        self._min_input_ui(layout)
        self._max_input_ui(layout)
        return layout

    def _min_input_ui(self, layout):
        self.xscale_min_le = QtWidgets.QLineEdit()
        self.xscale_min_le.setFixedWidth(100)
        self.yscale_min_le = QtWidgets.QLineEdit()
        self.yscale_min_le.setFixedWidth(100)
        self.zscale_min_le = QtWidgets.QLineEdit()
        self.zscale_min_le.setFixedWidth(100)
        self.xrotate_min_le = QtWidgets.QLineEdit()
        self.xrotate_min_le.setFixedWidth(100)
        self.yrotate_min_le = QtWidgets.QLineEdit()
        self.yrotate_min_le.setFixedWidth(100)
        self.zrotate_min_le = QtWidgets.QLineEdit()
        self.zrotate_min_le.setFixedWidth(100)
        layout.addWidget(self.xscale_min_le, 1, 1)
        layout.addWidget(self.yscale_min_le, 2, 1)
        layout.addWidget(self.zscale_min_le, 3, 1)
        layout.addWidget(self.xrotate_min_le, 4, 1)
        layout.addWidget(self.yrotate_min_le, 5, 1)
        layout.addWidget(self.zrotate_min_le, 6, 1)
        return layout

    def _max_input_ui(self, layout):
        self.xscale_max_le = QtWidgets.QLineEdit()
        self.xscale_max_le.setFixedWidth(100)
        self.yscale_max_le = QtWidgets.QLineEdit()
        self.yscale_max_le.setFixedWidth(100)
        self.zscale_max_le = QtWidgets.QLineEdit()
        self.zscale_max_le.setFixedWidth(100)
        self.xrotate_max_le = QtWidgets.QLineEdit()
        self.xrotate_max_le.setFixedWidth(100)
        self.yrotate_max_le = QtWidgets.QLineEdit()
        self.yrotate_max_le.setFixedWidth(100)
        self.zrotate_max_le = QtWidgets.QLineEdit()
        self.zrotate_max_le.setFixedWidth(100)
        layout.addWidget(self.xscale_max_le, 1, 2)
        layout.addWidget(self.yscale_max_le, 2, 2)
        layout.addWidget(self.zscale_max_le, 3, 2)
        layout.addWidget(self.xrotate_max_le, 4, 2)
        layout.addWidget(self.yrotate_max_le, 5, 2)
        layout.addWidget(self.zrotate_max_le, 6, 2)
        return layout

    def _create_input_headers(self):
        self.min_lbl = QtWidgets.QLabel("Minimum")
        self.min_lbl.setStyleSheet("font: bold")
        self.max_lbl = QtWidgets.QLabel("Maximum")
        self.max_lbl.setStyleSheet("font: bold")
        self.xscale_lbl = QtWidgets.QLabel("x Scale")
        self.yscale_lbl = QtWidgets.QLabel("y Scale")
        self.zscale_lbl = QtWidgets.QLabel("z Scale")
        self.xrotate_lbl = QtWidgets.QLabel("x Rotate")
        self.yrotate_lbl = QtWidgets.QLabel("y Rotate")
        self.zrotate_lbl = QtWidgets.QLabel("z Rotate")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.xscale_lbl, 1, 0)
        layout.addWidget(self.yscale_lbl, 2, 0)
        layout.addWidget(self.zscale_lbl, 3, 0)
        layout.addWidget(self.xrotate_lbl, 4, 0)
        layout.addWidget(self.yrotate_lbl, 5, 0)
        layout.addWidget(self.zrotate_lbl, 6, 0)
        layout.addWidget(self.min_lbl, 0, 1)
        layout.addWidget(self.max_lbl, 0, 2)
        return layout

    @QtCore.Slot()
    def scatter_objects(self):
        vtx_selection = cmds.polyListComponentConversion(self.destination_dd.currentText(),
                                                         toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31)

        scattered_instances = []
        for vtx in vtx_selection:
            scatter_instance = cmds.instance(self.source_dd.currentText())
            scattered_instances.extend(scatter_instance)
            pos = cmds.xform([vtx], query=True, translation=True)
            cmds.xform(scatter_instance, translation=pos)

        cmds.group(scattered_instances, name="scattered")
