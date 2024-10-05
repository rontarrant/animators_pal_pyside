## Python standard
import sys
import os
import io
import tempfile

stream = io.StringIO()
sys.stdout = stream
sys.stderr = stream

## PySide6
from PySide6.QtWidgets import (
	QApplication, QMainWindow, QLabel, QVBoxLayout,
	QHBoxLayout, QWidget, QFileDialog,
	QProgressDialog, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QSettings
from PySide6.QtGui import QPixmap, QImage, QPainter, QIcon

## non-standard
from moviepy.editor import ImageSequenceClip

## local
from video_controls import VideoControls
from settings_panel import SettingsPanel
from image_display import ImageDisplay
from image_list import ImageList
from resource_manager import ResourceManager

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Animator's Pal")
		self.settings = QSettings("Ron Tarrant", "AnimatorsPal")
		
		## resource path so PyInstaller can find and include images
		## It's set up here, not just because it's used for the window
		## icon, but also so it can be injected into the SettingsPanel
		## and VideoControls objects.
		base_path = os.path.abspath(os.path.dirname(__file__))
		self.resource_manager = ResourceManager(base_path)
		
		self.setup_ui()
		self.load_settings()
		self.current_image = 0
		self.setup_timer()
		self.update_settings()
		
		## add the Animator's Pal custom icon to the titlebar
		icon = QIcon()
		image = self.resource_manager.get_resource_path("images/bobby_bowtie_icon60x.png")
		icon.addPixmap(QPixmap(image))
		self.setWindowIcon(icon)

	def setup_ui(self):
		main_widget = QWidget()
		self.setCentralWidget(main_widget)
		main_layout = QVBoxLayout(main_widget)
		self.setup_content_area(main_layout)

	def setup_content_area(self, main_layout):
		content_layout = QHBoxLayout()
		main_layout.addLayout(content_layout)

		self.image_list = ImageList(self)
		content_layout.addWidget(self.image_list)

		right_container = QWidget()
		right_layout = QVBoxLayout(right_container)
		content_layout.addWidget(right_container)

		self.settings_panel = SettingsPanel(self, self.resource_manager)
		right_layout.addLayout(self.settings_panel.layout)

		self.image_display = ImageDisplay()
		right_layout.addWidget(self.image_display)

		self.video_controls = VideoControls(self, self.resource_manager)
		self.video_controls.image_changed.connect(self.on_image_changed)
		right_layout.addWidget(self.video_controls)

	def setup_timer(self):
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.switch_image)
		self.fps = 24
		self.timer.setInterval(1000 // self.fps)

	def update_settings(self):
		if self.settings_panel.direction_combo.currentText() == "Forward":
			self.video_controls.play_direction = 1
		else:
			self.video_controls.play_direction = -1
			
		self.fps = int(self.settings_panel.fps_combo.currentText())
		self.timer.setInterval(1000 // self.fps)
		self.video_controls.set_fps(self.fps)

		resolution = self.settings_panel.resolution_combo.currentText()
		
		if resolution == "720p":
			self.video_width, self.video_height = 1280, 720
		elif resolution == "1080p":
			self.video_width, self.video_height = 1920, 1080
		elif resolution == "4K":
			self.video_width, self.video_height = 3840, 2160
		elif resolution == "8K":
			self.video_width, self.video_height = 7680, 4320

		framehold = self.settings_panel.framehold_spin.value()
		self.video_controls.set_framehold(framehold)

	def reload_images(self):
		if self.image_list.image_files:
			self.image_list.clear_images()
			
			for img in self.image_list.image_files:
					processed_img = self.overlay_image_on_background(img)
					self.image_list.images.append(processed_img)
					
			self.switch_image()

	def overlay_image_on_background(self, image_path):
		original_image = QImage(image_path)
		background = QImage(self.video_width, self.video_height, QImage.Format_RGB32)
		background.fill(Qt.black)
		painter = QPainter(background)
		scaled_image = original_image.scaled(self.video_width, self.video_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		x = (self.video_width - scaled_image.width()) // 2
		y = (self.video_height - scaled_image.height()) // 2
		painter.drawImage(x, y, scaled_image)
		painter.end()
		return QPixmap.fromImage(background)

	def add_images(self):
		last_dir = self.settings.value("last_image_dir", os.getcwd())
		
		files, _ = QFileDialog.getOpenFileNames(self, "Select Images", last_dir, "Image Files (*.png *.jpg *.bmp, *.tif)")
		
		if files:
			self.settings.setValue("last_image_dir", os.path.dirname(files[0]))

			self.image_list.load_images(os.path.dirname(files[0]), files, self.overlay_image_on_background)
			
			if self.image_list.topLevelItemCount() > 0:
					self.current_image = 0
					self.video_controls.set_total_images(self.image_list.topLevelItemCount())
					self.switch_image()

	def save_video(self):
		if self.image_list.topLevelItemCount() == 0:
			return
		
		last_dir = self.settings.value("last_video_dir", os.getcwd())
		file_path, _ = QFileDialog.getSaveFileName(self, "Save Video", last_dir, "MP4 Files (*.mp4)")
		
		if file_path:
			self.settings.setValue("last_video_dir", os.path.dirname(file_path))
			
			if not file_path.lower().endswith('.mp4'):
					file_path += '.mp4'
					
			self.create_video(file_path)

	def switch_image(self, index = None):
		if index is not None:
			self.current_image = index
		
		if self.image_list.topLevelItemCount() > 0:
			self.current_image = min(self.current_image,
									self.image_list.topLevelItemCount() - 1)
			
			self.image_display.switch_image(self.image_list.images[self.current_image])
			current_item = self.image_list.topLevelItem(self.current_image)
			self.image_list.setCurrentItem(current_item)

	def on_image_changed(self, index):
		self.current_image = index
		self.switch_image(self.current_image)

	def create_video(self, output_filename):
		if self.image_list.topLevelItemCount() == 0:
			return

		progress = QProgressDialog("Saving video. Please wait.", "Cancel", 0, self.image_list.topLevelItemCount(), self)
		progress.setWindowModality(Qt.WindowModal)
		progress.setWindowTitle("Saving Video")

		try:
			with tempfile.TemporaryDirectory() as tmpdirname:
				scaled_image_files = []
				
				if self.settings_panel.direction_combo.currentText() == "Reverse":
						image_sequence = reversed(self.image_list.images)
				else:
						image_sequence = self.image_list.images

				for i, img in enumerate(image_sequence):
						if progress.wasCanceled():
							return
						
						# Scale the image to the correct resolution
						scaled_img = img.scaled(self.video_width, self.video_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
						
						for _ in range(self.video_controls.framehold):
							temp_file = os.path.join(tmpdirname, 
											f"scaled_image_{len(scaled_image_files):04d}.png")
							
							# Save the scaled image
							scaled_img.save(temp_file, "PNG")
							scaled_image_files.append(temp_file)
						
						progress.setValue(i + 1)

				progress.setLabelText("Encoding video...")
				clip = ImageSequenceClip(scaled_image_files, fps=self.fps)
				clip.write_videofile(output_filename, codec='libx264')
				progress.setValue(self.image_list.topLevelItemCount())
		except Exception as e:
			QMessageBox.critical(self, "Error", f"An error occurred while saving the video: {str(e)}")
		finally:
			progress.close()

	def new_project(self):
		self.image_list.clear_images()
		self.image_display.create_black_background()

	def closeEvent(self, event):
		self.save_settings()
		super().closeEvent(event)

	def load_settings(self):
		geometry = self.settings.value("geometry")
		
		if geometry:
			self.restoreGeometry(geometry)
		else:
			self.setGeometry(100, 100, 1600, 900)

		screen = QApplication.primaryScreen().availableGeometry()
		
		if not screen.contains(self.frameGeometry()):
			self.move(screen.topLeft())

	def save_settings(self):
		self.settings.setValue("geometry", self.saveGeometry())

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())
