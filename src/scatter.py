import random
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import pymel.core as pmc


def maya_main_window():
    """Return Maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterUI(QtWidgets.QDialog):
    """Scatter UI Class"""

    def __init__(self):
        """Constructor"""
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.scatter = RandomScatter(self)
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.setMaximumHeight(500)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.source_dd_lay = self._create_source_dd()
        self.percentage_lay = self._create_percentage()
        self.destination_lay = self._create_destination()
        self.input_ui = self._create_input_ui()
        self.button_lay = self._create_button_ui()
        self.normals_checkbox_lay = self._create_normals_checkbox()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addLayout(self.source_dd_lay)
        self.main_lay.addLayout(self.percentage_lay)
        self.main_lay.addLayout(self.destination_lay)
        self.main_lay.addLayout(self.normals_checkbox_lay)
        self.main_lay.addLayout(self.input_ui)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

    @QtCore.Slot()
    def create_connections(self):
        self.scatter_btn.clicked.connect(self.scatter_objects)

    def _create_normals_checkbox(self):
        self.normals_checkbox = QtWidgets.QCheckBox("Align with Normals")
        self.normals_checkbox.setChecked(False)
        self.normals_checkbox.toggled.connect(self._on_clicked)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.normals_checkbox, 0, 0)
        return layout

    def _on_clicked(self):
        self.normals_checkbox = self.sender()
        print("this works") #this is where the checkbox logic is called i think lol

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

    @QtCore.Slot()
    def _create_percentage(self):
        self.percentage_lbl = QtWidgets.QLabel("Enter percentage "
                                                       "of vertices to scattter to")
        self.percentage = QtWidgets.QSlider(Qt.Horizontal)
        self.percentage.setMinimum(0)
        self.percentage.setMaximum(100)
        self.percentage.setValue(100)
        self.percentage_value_lbl = QtWidgets.QLabel(str(self.percentage.value()))
        self.percentage.valueChanged.connect(self._slider_changed)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.percentage_lbl)
        layout.addWidget(self.percentage)
        layout.addWidget(self.percentage_value_lbl)
        return layout

    def _slider_changed(self):
        print(self.percentage.value())
        self.percentage_value_lbl.setText(str(self.percentage.value()))

    def _create_destination(self):
        """select destination vertices"""
        self.destination_lbl = QtWidgets.QLabel("Please select the "
                                                   "objects and vertices you would "
                                                   "like to scatter to.")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.destination_lbl)
        return layout

    def _create_input_ui(self):
        layout = self._create_input_headers()
        self._min_input_ui(layout)
        self._max_input_ui(layout)
        return layout

    def _min_input_ui(self, layout):
        self.xscale_min_le = QtWidgets.QLineEdit('1')
        self.xscale_min_le.setMinimumWidth(100)
        self.yscale_min_le = QtWidgets.QLineEdit('1')
        self.yscale_min_le.setMinimumWidth(100)
        self.zscale_min_le = QtWidgets.QLineEdit('1')
        self.zscale_min_le.setMinimumWidth(100)
        self.xrotate_min_le = QtWidgets.QLineEdit('0')
        self.xrotate_min_le.setMinimumWidth(100)
        self.yrotate_min_le = QtWidgets.QLineEdit('0')
        self.yrotate_min_le.setMinimumWidth(100)
        self.zrotate_min_le = QtWidgets.QLineEdit('0')
        self.zrotate_min_le.setMinimumWidth(100)
        layout.addWidget(self.xscale_min_le, 1, 1)
        layout.addWidget(self.yscale_min_le, 2, 1)
        layout.addWidget(self.zscale_min_le, 3, 1)
        layout.addWidget(self.xrotate_min_le, 4, 1)
        layout.addWidget(self.yrotate_min_le, 5, 1)
        layout.addWidget(self.zrotate_min_le, 6, 1)
        return layout

    def _max_input_ui(self, layout):
        self.xscale_max_le = QtWidgets.QLineEdit('1')
        self.xscale_max_le.setMinimumWidth(100)
        self.yscale_max_le = QtWidgets.QLineEdit('1')
        self.yscale_max_le.setMinimumWidth(100)
        self.zscale_max_le = QtWidgets.QLineEdit('1')
        self.zscale_max_le.setMinimumWidth(100)
        self.xrotate_max_le = QtWidgets.QLineEdit('0')
        self.xrotate_max_le.setMinimumWidth(100)
        self.yrotate_max_le = QtWidgets.QLineEdit('0')
        self.yrotate_max_le.setMinimumWidth(100)
        self.zrotate_max_le = QtWidgets.QLineEdit('0')
        self.zrotate_max_le.setMinimumWidth(100)
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
        self.scatter.scatter_objects(self.source_dd.currentText(),
                                     cmds.ls(sl=True))


class RandomScatter(object):
    """random scatter logic."""

    def __init__(self, ui_instance):
        self.ui_scatter = ui_instance
        pass

    def scatter_objects(self, source_selection, destination_selection):
        vtx_selection = cmds.polyListComponentConversion(
            destination_selection, toVertex=True)
        vtx_selection = cmds.filterExpand(vtx_selection, selectionMask=31)

        scattered_instances = []
        for vtx in vtx_selection:
            scatter_instance = cmds.instance(source_selection)
            self.random_scale(scatter_instance)
            scattered_instances.extend(scatter_instance)
            pos = cmds.xform([vtx], query=True, translation=True)
            cmds.xform(scatter_instance, translation=pos)
        cmds.group(scattered_instances, name="scattered")

    def random_scale(self, randomized_object):
        xRot = random.uniform(float(self.ui_scatter.xrotate_min_le.displayText()), float(self.ui_scatter.xrotate_max_le.displayText()))
        yRot = random.uniform(float(self.ui_scatter.yrotate_min_le.displayText()), float(self.ui_scatter.yrotate_max_le.displayText()))
        zRot = random.uniform(float(self.ui_scatter.zrotate_min_le.displayText()), float(self.ui_scatter.zrotate_max_le.displayText()))

        cmds.rotate(xRot, yRot, zRot, randomized_object)

        xScale = random.uniform(float(self.ui_scatter.xscale_min_le.displayText()), float(self.ui_scatter.xscale_max_le.displayText()))
        yScale = random.uniform(float(self.ui_scatter.yscale_min_le.displayText()), float(self.ui_scatter.yscale_max_le.displayText()))
        zScale = random.uniform(float(self.ui_scatter.zscale_min_le.displayText()), float(self.ui_scatter.zscale_max_le.displayText()))

        cmds.scale(xScale, yScale, zScale, randomized_object)

    def select_percentage(self):
        selection = cmds.ls(selection=True, flatten=True)
        selected_verts = cmds.polyListComponentConversion(selection,
                                                          toVertex=True)
        selected_verts = cmds.filterExpand(selected_verts, selectionMask=31)
        seed = 453    #change seed
        percentage_selection = []
        for idx in range(0, len(selected_verts)):
            random.seed(idx + seed)
            rand_value = random.random()
            if rand_value <= 0.1:   #put slider value here
                percentage_selection.append(selected_verts[idx])
        cmds.select(percentage_selection)


