import os  
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,   
                           QLabel, QSlider, QStyle)  
from PyQt5.QtCore import Qt, QTime, pyqtSlot  
from src.core.media_player import MediaPlayer  

class PlayerWidget(QWidget):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.media_player = MediaPlayer()  
        self.setup_ui()  
        self.connect_signals()  
        
    def setup_ui(self):  
        # 创建布局  
        self.layout = QVBoxLayout(self)  
        
        # 创建当前播放信息标签  
        self.current_file_label = QLabel("未选择文件")  
        self.current_file_label.setAlignment(Qt.AlignCenter)  
        
        # 创建时间显示标签  
        self.time_label = QLabel("00:00 / 00:00")  
        self.time_label.setAlignment(Qt.AlignCenter)  
        
        # 创建进度条  
        self.progress_slider = QSlider(Qt.Horizontal)  
        self.progress_slider.setRange(0, 100)  
        
        # 创建控制按钮布局  
        self.controls_layout = QHBoxLayout()  
        
        # 创建播放/暂停按钮  
        self.play_button = QPushButton()  
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))  
        
        # 创建停止按钮  
        self.stop_button = QPushButton()  
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))  
        
        # 创建选择文件夹按钮  
        self.folder_button = QPushButton("选择文件夹")  
        
        # 将控制按钮添加到布局  
        self.controls_layout.addWidget(self.play_button)  
        self.controls_layout.addWidget(self.stop_button)  
        self.controls_layout.addWidget(self.folder_button)  
        
        # 将组件添加到主布局  
        self.layout.addWidget(self.current_file_label)  
        self.layout.addWidget(self.time_label)  
        self.layout.addWidget(self.progress_slider)  
        self.layout.addLayout(self.controls_layout)  
    
    def connect_signals(self):  
        # 连接UI事件  
        self.play_button.clicked.connect(self.play_pause)  
        self.stop_button.clicked.connect(self.stop)  
        self.progress_slider.sliderMoved.connect(self.media_player.set_position)  
        
        # 连接媒体播放器信号  
        self.media_player.position_changed.connect(self.update_position)  
        self.media_player.duration_changed.connect(self.update_duration)  
        self.media_player.state_changed.connect(self.update_player_state)  
    
    def play_file(self, file_path):  
        self.media_player.load_file(file_path)  
        self.current_file_label.setText(os.path.basename(file_path))  
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))  
        self.media_player.play()  
    
    def play_pause(self):  
        self.media_player.toggle_play_pause()  
    
    def stop(self):  
        self.media_player.stop()  
    
    @pyqtSlot(int)  
    def update_position(self, position):  
        self.progress_slider.setValue(position)  
        current_time = QTime(0, 0).addMSecs(position)  
        duration_time = QTime(0, 0).addMSecs(self.media_player.duration)  
        self.time_label.setText(f"{current_time.toString('mm:ss')} / {duration_time.toString('mm:ss')}")  
    
    @pyqtSlot(int)  
    def update_duration(self, duration):  
        self.progress_slider.setRange(0, duration)  
    
    @pyqtSlot(int)  
    def update_player_state(self, state):  
        if state == MediaPlayer.PLAYING_STATE:  
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))  
        else:  
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))  
