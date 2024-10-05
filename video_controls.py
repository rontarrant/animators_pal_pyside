from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal, QTimer, QSize
from PySide6.QtGui import QIcon, QPixmap
import os

class VideoControls(QWidget):
	image_changed = Signal(int)

	def __init__(self, parent, resource_manager):
		super().__init__(parent)
		self.resource_manager = resource_manager

		self.layout = QHBoxLayout(self)

		self.buttons = {
			'goto_start': ('goto_start_up.png', 'goto_start_down.png', 'Go to frame 1'),
			'step_back': ('reverse_step_up.png', 'reverse_step_down.png', 'Step back one frame'),
			'play_reverse': ('reverse_play_up.png', 'reverse_play_down.png', 'Play in reverse'),
			'bounce': ('bounce_play_up.png', 'bounce_play_down.png', 'Bounce play - forward, then back, repeat'),
			'stop': ('stop_up.png', 'stop_down.png', 'Stop'),
			'play_forward': ('forward_play_up.png', 'forward_play_down.png', 'Play forward'),
			'step_forward': ('forward_step_up.png', 'forward_step_down.png', 'Advance one frame'),
			'goto_end': ('goto_end_up.png', 'goto_end_down.png', 'Go to last frame'),
			'loop': ('loop_off_up.png', 'loop_off_down.png', 'Turn looping on or off')
		}

		self.create_buttons()

		self.current_image = 0
		self.total_images = 0
		self.is_playing = False
		self.is_bouncing = False
		self.is_looping = False
		self.play_direction = 1
		self.framehold = 1
		self.frame_count = 0
		self.fps = 24

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_image)

	def create_buttons(self):
		button_size = QSize(64, 64)
		self.layout.addStretch()
		
		for name, (up_image, down_image, button_tooltip) in self.buttons.items():
			up_image = self.resource_manager.get_resource_path(f"images/{up_image}")
			down_image = self.resource_manager.get_resource_path(f"images/{down_image}")

			button = QPushButton()
			button.setCheckable(True)
			button.setFixedSize(button_size)
			self.set_button_icons(button, up_image, down_image)
			button.setToolTip(button_tooltip)
			setattr(self, f'{name}_button', button)
			self.layout.addWidget(button)

		self.layout.addStretch()
		self.goto_start_button.clicked.connect(self.goto_start)
		self.step_back_button.clicked.connect(self.step_back)
		self.play_reverse_button.clicked.connect(self.play_reverse)
		self.stop_button.clicked.connect(self.stop_playback)
		self.play_forward_button.clicked.connect(self.play_forward)
		self.step_forward_button.clicked.connect(self.step_forward)
		self.goto_end_button.clicked.connect(self.goto_end)
		self.bounce_button.clicked.connect(self.toggle_bounce)
		self.loop_button.clicked.connect(self.toggle_loop)

	def set_button_icons(self, button, up_image, down_image):
		icon = QIcon()
		icon.addPixmap(QPixmap(os.path.join('images', up_image)), QIcon.Normal, QIcon.Off)
		icon.addPixmap(QPixmap(os.path.join('images', down_image)), QIcon.Normal, QIcon.On)
		button.setIcon(icon)
		button.setIconSize(QPixmap(os.path.join('images', up_image)).size())

	def set_total_images(self, total):
		self.total_images = total

	def set_fps(self, fps):
		self.fps = fps
		self.timer.setInterval(1000 // self.fps)

	def set_framehold(self, framehold):
		self.framehold = framehold
		self.frame_count = 0

	def goto_start(self):
		self.current_image = 0
		self.image_changed.emit(self.current_image)

	def step_back(self):
		if self.total_images:
			self.current_image = (self.current_image - 1) % self.total_images
			self.image_changed.emit(self.current_image)

	def play_reverse(self):
		self.play_direction = -1
		self.start_playback()

	def stop_playback(self):
		self.timer.stop()
		self.is_playing = False
		self.is_bouncing = False
		self.frame_count = 0
		self.play_forward_button.setChecked(False)
		self.play_reverse_button.setChecked(False)
		self.bounce_button.setChecked(False)

	def play_forward(self):
		self.play_direction = 1
		self.start_playback()

	def start_playback(self):
		if self.total_images:
			self.is_playing = True
			self.is_bouncing = False
			self.frame_count = 0
			self.timer.start()
			
			if self.play_direction == 1:
					self.play_forward_button.setChecked(True)
					self.play_reverse_button.setChecked(False)
			else:
					self.play_forward_button.setChecked(False)
					self.play_reverse_button.setChecked(True)

	def step_forward(self):
		if self.total_images:
			self.current_image = (self.current_image + 1) % self.total_images
			self.image_changed.emit(self.current_image)

	def goto_end(self):
		if self.total_images:
			self.current_image = self.total_images - 1
			self.image_changed.emit(self.current_image)

	def toggle_bounce(self):
		if self.is_bouncing:
			self.stop_playback()
		else:
			self.is_bouncing = True
			self.is_playing = True
			self.frame_count = 0
			self.timer.start()
			self.bounce_button.setChecked(True)
			self.play_forward_button.setChecked(False)
			self.play_reverse_button.setChecked(False)

	def toggle_loop(self):
		self.is_looping = not self.is_looping
		self.loop_button.setChecked(self.is_looping)
		if self.is_looping:
			self.set_button_icons(self.loop_button, 'loop_on_up.png', 'loop_on_down.png')
		else:
			self.set_button_icons(self.loop_button, 'loop_off_up.png', 'loop_off_down.png')

	def update_image(self):
		if self.is_playing:
			self.frame_count += 1
			if self.frame_count >= self.framehold:
					self.frame_count = 0
					if self.is_bouncing:
						self.current_image += self.play_direction
						if self.current_image >= self.total_images or self.current_image < 0:
							self.play_direction *= -1
							self.current_image += self.play_direction * 2
					else:
						self.current_image = (self.current_image + self.play_direction) % self.total_images
						if self.current_image == 0 and not self.is_looping:
							self.stop_playback()
					self.image_changed.emit(self.current_image)
