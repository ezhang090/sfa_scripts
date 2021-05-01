import random
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt, QItemSelectionModel
from PySide2.QtWidgets import QAbstractItemView
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
        self.source_list_lay = self._create_source_list()
        # self.add_object_lay = self._create_add_source_button()
        self.percentage_lay = self._create_percentage()
        self.seed_lay = self._create_seed()
        self.destination_lay = self._create_destination()
        self.input_ui = self._create_input_ui()
        self.button_lay = self._create_button_ui()
        self.normals_checkbox_lay = self._create_normals_checkbox()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        # self.main_lay.addLayout(self.add_object_lay)
        self.main_lay.addLayout(self.source_list_lay)
        self.main_lay.addLayout(self.percentage_lay)
        self.main_lay.addLayout(self.seed_lay)
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
        self.normals_checkbox.toggled.connect(self._on_clicked) #might not need this connection
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.normals_checkbox, 0, 0)
        return layout

    #might not need this connection
    def _on_clicked(self):
        self.normals_checkbox = self.sender()
        print("this works") #this is where the checkbox logic is called i think lol

    def _create_button_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout

    # def _create_add_source_button(self):
    #     self.add_source_btn = QtWidgets.QPushButton("Add Source Objects")
    #     self.add_source_btn.clicked.connect(self.add_source_object)
    #     layout = QtWidgets.QHBoxLayout()
    #     layout.addWidget(self.add_source_btn)
    #     return layout

    def add_source_object(self):
        #print("ajdfhaowehfsjdfh")
        #self.source_dd.clear()
        self._create_source_list()

    def _create_source_list(self):
        """create dropdown menu to select source object"""
        self.source_lbl = QtWidgets.QLabel("Source Objects")
        self.source_list = QtWidgets.QListWidget()
        self.source_list.setSelectionMode(QAbstractItemView.MultiSelection)
        #populate source list
        for obj in cmds.ls(type='mesh'):
            self.source_list.addItem(obj)

        # self.source_list.addItem('hi')
        # self.source_list.addItem('im')
        # self.source_list.addItem('sad')
        #print(self.source_list.selectionMode())
        #print(self.source_list.selectionModel())
        #self.source_list.addItem("Selected Objects")
        # objects = cmds.ls(type="mesh")
        # for geo in objects:
        #     self.source_list.addItem(geo)
        # self.source_list.currentIndexChanged.connect(
        #     self.source_index_changed)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.source_lbl)
        layout.addWidget(self.source_list)
        return layout
    #
    # def source_index_changed(self):
    #     cmds.select(self.source_dd.currentText())

    @QtCore.Slot()
    def _create_percentage(self):
        self.percentage_lbl = QtWidgets.QLabel("Percentage of Vertices:")
        self.percentage_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.percentage_slider.setMinimum(0)
        self.percentage_slider.setMaximum(100)
        self.percentage_slider.setValue(100)
        self.percentage_value_lbl = QtWidgets.QLabel(str(self.percentage_slider.value()))
        self.percentage_slider.valueChanged.connect(self._slider_changed)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.percentage_lbl)
        layout.addWidget(self.percentage_slider)
        layout.addWidget(self.percentage_value_lbl)
        return layout

    def _slider_changed(self):
        print(self.percentage_slider.value())
        self.percentage_value_lbl.setText(str(self.percentage_slider.value()))

    def _create_seed(self):
        self.seed_lbl = QtWidgets.QLabel("Set Seed:")
        self.seed_le = QtWidgets.QLineEdit('453')
        self.seed_lbl.setAlignment(Qt.AlignRight)
        self.seed_le.setMaximumWidth(50)
        self.seed_le.setAlignment(Qt.AlignHCenter)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.seed_lbl)
        layout.addWidget(self.seed_le)
        return layout

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
        # self.scatter.scatter_objects(self.source_list.currentText(),
        #                              cmds.ls(sl=True))
        #self.scatter.scatter_objects(self.source_list.selectedItems(), cmds.ls(sl=True))
        source_objects = []
        for source_obj in self.source_list.selectedItems():
            source_objects.append(source_obj.text())

        self.scatter.scatter_objects(source_objects,
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
        scatter_vertex_selection = self.select_percentage(vtx_selection, len(vtx_selection))
        # scatter_vertex_selection = vtx_selection

        scattered_instances = self.get_scattered(source_selection, scatter_vertex_selection)
        scatter_index = 0
        for vtx in scatter_vertex_selection:
            scatter_instance = scattered_instances[scatter_index]
            # scale random or align to normals
            pos = cmds.xform([vtx], query=True, translation=True)
            cmds.xform(scatter_instance, translation=pos)
            scatter_index += 1
        # Create group for scattered objects
        cmds.group(scattered_instances, name="scattered")

    def get_scattered(self, source_selection, verts):
        scattered_instances = []
        i = 0
        for vtx in verts:
            scatter_instance = cmds.instance(source_selection[i])
            self.random_scale(scatter_instance)  # perform random scale
            scattered_instances.append(scatter_instance[0])
            if i == (len(source_selection) - 1):
                i = 0
            else:
                i += 1
        random.shuffle(scattered_instances)
        return scattered_instances

    def random_scale(self, randomized_object):
        xRot = random.uniform(float(self.ui_scatter.xrotate_min_le.displayText()), float(self.ui_scatter.xrotate_max_le.displayText()))
        yRot = random.uniform(float(self.ui_scatter.yrotate_min_le.displayText()), float(self.ui_scatter.yrotate_max_le.displayText()))
        zRot = random.uniform(float(self.ui_scatter.zrotate_min_le.displayText()), float(self.ui_scatter.zrotate_max_le.displayText()))

        cmds.rotate(xRot, yRot, zRot, randomized_object)

        xScale = random.uniform(float(self.ui_scatter.xscale_min_le.displayText()), float(self.ui_scatter.xscale_max_le.displayText()))
        yScale = random.uniform(float(self.ui_scatter.yscale_min_le.displayText()), float(self.ui_scatter.yscale_max_le.displayText()))
        zScale = random.uniform(float(self.ui_scatter.zscale_min_le.displayText()), float(self.ui_scatter.zscale_max_le.displayText()))

        cmds.scale(xScale, yScale, zScale, randomized_object)

    def select_percentage(self, vtx_selection, num_vtx):
        random_percentage = self.ui_scatter.percentage_slider.value()
        if random_percentage == 100:
            return vtx_selection #no work to do
        # random.shuffle(vtx_selection)
        # selection = cmds.ls(selection=True, flatten=True)
        # selected_verts = cmds.polyListComponentConversion(selection,
        #                                                   toVertex=True)
        # selected_verts = cmds.filterExpand(selected_verts, selectionMask=31)
        seed = 453    # change seed: will need to grab value from user input text box, default 453
        seed = int(self.ui_scatter.seed_le.displayText())
        percentage_selection = []
        for idx in range(0, num_vtx - 1):
            random.seed(idx + seed)
            rand_value = random.random()
            if rand_value <= float(random_percentage)/100:   # put slider value here
                percentage_selection.append(vtx_selection[idx])
        # cmds.select(percentage_selection)
        # print(percentage_selection)
        return percentage_selection

    # def align_to_normals(self):
    #     constraint = cmds.normalConstraint('', '') #put vertex and instance
    #     print(constraint)
    #     cmds.delete(constraint)


