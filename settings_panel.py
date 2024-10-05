from PySide6.QtWidgets import (
	QHBoxLayout, QPushButton, QLabel, QComboBox,
	QSpinBox, QWidget, QVBoxLayout, QGroupBox
)
from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QIcon, QPixmap

## local
from image_button import ImageButton

class SettingsPanel:
	def __init__(self, parent, resource_manager):
		self.parent = parent
		self.resource_manager = resource_manager
		self.layout = QHBoxLayout()
		self.settings = QSettings("YourCompany", "AnimatorsPal")
		
		self.buttons = {
			'add_images': ("images/add_images_up.png", "images/add_images_down.png"),
			'save_video': ("images/save_video_up.png", "images/save_video_down.png"),
			'reset': ("images/reset_framehold_up.png", "images/reset_framehold_down.png"),
			'new': ("images/new_up.png", "images/new_down.png")
		}
		
		self.setup_ui()

	def setup_ui(self):
		## Add Images button set-up
		up_image = self.resource_manager.get_resource_path(f"{self.buttons['add_images'][0]}")
		down_image = self.resource_manager.get_resource_path(f"{self.buttons['add_images'][1]}")
		self.add_images_button = ImageButton(up_image, down_image)
		self.add_images_button.clicked.connect(self.parent.add_images)
		self.add_images_button.setToolTip("Add images to the list")
		self.layout.addWidget(self.add_images_button)
		
		self.layout.addStretch()
		self.setup_combo_boxes()
		self.setup_framehold()
		self.layout.addStretch()

		## Save Video button set-up
		up_image = self.resource_manager.get_resource_path(f"{self.buttons['save_video'][0]}")
		down_image = self.resource_manager.get_resource_path(f"{self.buttons['save_video'][1]}")
		self.save_video_button = ImageButton(up_image, down_image)
		self.save_video_button.clicked.connect(self.parent.save_video)
		self.save_video_button.setToolTip("Save the video file")
		self.layout.addWidget(self.save_video_button)

		self.layout.addStretch()

		## New button set-up
		up_image = self.resource_manager.get_resource_path(f"{self.buttons['new'][0]}")
		down_image = self.resource_manager.get_resource_path(f"{self.buttons['new'][1]}")
		self.new_button = ImageButton(up_image, down_image)
		self.new_button.clicked.connect(self.parent.new_project)
		self.new_button.setToolTip("Clear the image list and start a new project")
		self.layout.addWidget(self.new_button)

	def setup_combo_boxes(self):
		combo_layout = QHBoxLayout()
		self.layout.addLayout(combo_layout)

		self.setup_direction()
		self.setup_fps()
		self.setup_resolution()
		
	def build_group_layout(self, group_name):
		group = QGroupBox(group_name)
		
		group.setStyleSheet("""
			QGroupBox {
					border: 1px solid gray;
					border-radius: 4px;
					margin-top: 1ex;
			}
			QGroupBox::title {
					subcontrol-origin: margin;
					left: 10px;
					padding: 0 3px 0 3px;
			}
		""")
		
		layout = QHBoxLayout(group)
		layout.setContentsMargins(10, 10, 10, 10)
		
		return group, layout

	def setup_resolution(self):
		resolution_group, resolution_layout = self.build_group_layout("Resolution")
		## Resolution widgets
		self.resolution_combo = QComboBox()
		self.resolution_combo.addItems(["720p", "1080p", "4K", "8K"])
		self.resolution_combo.setCurrentText(self.settings.value("resolution", "1080p"))
		self.resolution_combo.currentTextChanged.connect(self.update_settings)

		resolution_layout.addWidget(self.resolution_combo)

		self.layout.addWidget(resolution_group)
		self.layout.addSpacing(10)
		
	def setup_fps(self):
		fps_group, fps_layout = self.build_group_layout("fps")
		## fps widgets
		self.fps_combo = QComboBox()
		self.fps_combo.addItems(["18", "24", "30"])
		self.fps_combo.setCurrentText(self.settings.value("fps", "24"))
		self.fps_combo.currentTextChanged.connect(self.update_settings)

		fps_layout.addWidget(self.fps_combo)

		self.layout.addWidget(fps_group)
		self.layout.addSpacing(10)

	def setup_direction(self):
		direction_group, direction_layout = self.build_group_layout("Direction")
		## Direction widgets
		self.direction_combo = QComboBox()
		self.direction_combo.addItems(["Forward", "Reverse"])
		self.direction_combo.setCurrentText(self.settings.value("direction", "Forward"))
		self.direction_combo.currentTextChanged.connect(self.update_settings)

		direction_layout.addWidget(self.direction_combo)

		self.layout.addWidget(direction_group)
		self.layout.addSpacing(10)

	## Framehold (Shoot on) widgets
	def setup_framehold(self):
		framehold_group, framehold_layout = self.build_group_layout("Framehold")
		
		self.framehold_spin = QSpinBox()
		self.framehold_spin.setRange(1, 9)
		self.framehold_spin.setValue(int(self.settings.value("framehold", 1)))
		self.framehold_spin.valueChanged.connect(self.update_settings)

		up_image = self.resource_manager.get_resource_path(f"{self.buttons['reset'][0]}")
		down_image = self.resource_manager.get_resource_path(f"{self.buttons['reset'][1]}")
		reset_button = ImageButton(up_image, down_image)
		reset_button.setToolTip("Reset framehold to '1'")
		reset_button.clicked.connect(self.reset_framehold)

		framehold_layout.addWidget(self.framehold_spin)
		framehold_layout.addWidget(reset_button)

		self.layout.addWidget(framehold_group)
		self.layout.addSpacing(10)

	def update_settings(self):
		self.settings.setValue("direction", self.direction_combo.currentText())
		self.settings.setValue("fps", self.fps_combo.currentText())
		self.settings.setValue("resolution", self.resolution_combo.currentText())
		self.settings.setValue("framehold", self.framehold_spin.value())
		self.parent.update_settings()

	def reset_framehold(self):
		self.framehold_spin.setValue(1)
		self.update_settings()
