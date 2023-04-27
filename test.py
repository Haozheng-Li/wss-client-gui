import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtMultimediaWidgets import QVideoWidget

class VideoPlayer(QMainWindow):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Player')
        self.setGeometry(300, 300, 800, 600)
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.setCentralWidget(self.video_widget)
        self.media_player.setVideoOutput(self.video_widget)
        self.open_button = QPushButton('Open Video', self)
        self.open_button.clicked.connect(self.open_video)
        self.statusBar().addPermanentWidget(self.open_button)

    def open_video(self):
        video_path, _ = QFileDialog.getOpenFileName(self, 'Open Video', '', 'Video Files (*.avi *.mp4 *.mkv);;All Files (*)')
        if video_path:
            self.media_player.setMedia(QMediaContent(video_path))
            self.media_player.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec_())