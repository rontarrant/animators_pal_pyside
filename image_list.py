from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QProgressDialog, QFileDialog, QHeaderView
from PySide6.QtCore import Qt
import os

class ImageList(QTreeWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.image_files = []
		self.images = []
		self.itemClicked.connect(self.on_item_clicked)
		
		# Set up the tree widget with two columns
		self.setColumnCount(2)
		self.setHeaderLabels(["File Name", "Folder"])
		
		# Adjust column widths
		header = self.header()
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

	def load_images(self, folder, files, overlay_image_on_background):
		all_files = os.listdir(folder)
		new_image_files = [os.path.join(folder, file) for file in files if file.lower().endswith((".jpg", ".png", ".bmp", ".tif"))]
		new_image_files.sort()

		progress = QProgressDialog("Loading images...", "Cancel", 0, len(new_image_files), self)
		progress.setWindowModality(Qt.WindowModal)
		progress.setWindowTitle("Loading Images")

		for i, img_file in enumerate(new_image_files):
			if progress.wasCanceled():
					break
			
			self.image_files.append(img_file)
			processed_img = overlay_image_on_background(img_file)
			self.images.append(processed_img)
			
			# Create a QTreeWidgetItem with two columns
			item = QTreeWidgetItem(self)
			item.setText(0, os.path.basename(img_file))
			item.setText(1, os.path.basename(os.path.dirname(img_file)))
			item.setData(0, Qt.UserRole, img_file)
			
			progress.setValue(i + 1)

		progress.close()

	def on_item_clicked(self, item, column):
		current_row = self.indexOfTopLevelItem(item)
		self.parent.switch_image(current_row)

	def clear_images(self):
		self.clear()
		self.image_files.clear()
		self.images.clear()
