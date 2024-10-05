from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap

class ImageButton(QPushButton):
	def __init__(self, up_image, down_image, parent = None):
		super().__init__(parent)
		self.up_icon = QIcon(up_image)
		self.down_icon = QIcon(down_image)
		self.setIcon(self.up_icon)
		self.setIconSize(QPixmap(up_image).size())
		self.setFixedSize(64, 64)
		self.setStyleSheet("QPushButton { border: none; }")

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.setIcon(self.down_icon)
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.setIcon(self.up_icon)
		super().mouseReleaseEvent(event)
