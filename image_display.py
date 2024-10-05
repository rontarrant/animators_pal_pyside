from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class ImageDisplay(QLabel):
	def __init__(self):
		super().__init__()
		self.setFixedSize(1280, 720)
		self.create_black_background()

	def create_black_background(self):
		black_image = QImage(1280, 720, QImage.Format_RGB32)
		black_image.fill(Qt.black)
		self.black_background = QPixmap.fromImage(black_image)
		self.setPixmap(self.black_background)

	def switch_image(self, pixmap):
		scaled_pixmap = pixmap.scaled(
			self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.setPixmap(scaled_pixmap)
