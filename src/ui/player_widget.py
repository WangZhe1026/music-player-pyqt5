import os  
from PyQt5.QtMultimedia import QMediaPlayer  
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,   
                           QLabel, QSlider, QStyle)  
from PyQt5.QtCore import Qt, QTime, pyqtSlot  
from src.core.media_player import MediaPlayer  
from src.core.playlist import Playlist, PlaylistMode  # 添加这一行导入

class PlayerWidget(QWidget):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.media_player = MediaPlayer()  
        self.playlist = Playlist()  # 创建播放列表实例
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
        
        # 添加播放列表控制按钮
        self.playlist_controls_layout = QHBoxLayout()
        
        # 上一曲按钮
        self.prev_button = QPushButton()
        self.prev_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prev_button.setToolTip("上一曲")
        
        # 创建播放/暂停按钮  
        self.play_button = QPushButton()  
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))  
        
        # 下一曲按钮
        self.next_button = QPushButton()
        self.next_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_button.setToolTip("下一曲")
        
        # 创建停止按钮  
        self.stop_button = QPushButton()  
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))  
        
        # 播放模式按钮 - 初始为顺序播放
        self.mode_button = QPushButton()
        self.mode_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.mode_button.setToolTip("播放模式: 顺序播放")
        
        # 创建选择文件夹按钮  
        self.folder_button = QPushButton("选择文件夹")  
        
        # 将按钮添加到布局
        self.playlist_controls_layout.addWidget(self.prev_button)
        self.playlist_controls_layout.addWidget(self.play_button)
        self.playlist_controls_layout.addWidget(self.next_button)
        self.playlist_controls_layout.addWidget(self.stop_button)
        self.playlist_controls_layout.addWidget(self.mode_button)
        self.playlist_controls_layout.addWidget(self.folder_button)
        
        # 替换原来的controls_layout
        self.layout.addWidget(self.current_file_label)  
        self.layout.addWidget(self.time_label)  
        self.layout.addWidget(self.progress_slider)  
        self.layout.addLayout(self.playlist_controls_layout)
        
        # 创建音量控制布局  
        self.volume_layout = QHBoxLayout()  
        
        # 创建音量图标按钮  
        self.mute_button = QPushButton()  
        self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))  
        self.mute_button.setToolTip("静音")  
        self.mute_button.setFixedSize(32, 32)  
        
        # 创建音量滑块  
        self.volume_slider = QSlider(Qt.Horizontal)  
        self.volume_slider.setRange(0, 100)  
        self.volume_slider.setValue(50)  # 默认音量  
        self.volume_slider.setToolTip("音量")  
        self.volume_slider.setFixedWidth(100)  
        
        # 将音量控件添加到布局  
        self.volume_layout.addWidget(self.mute_button)  
        self.volume_layout.addWidget(self.volume_slider)  
        
        # 将音量控制布局添加到播放列表控制布局中  
        self.playlist_controls_layout.addStretch(1)  # 添加弹性空间，让音量控制靠右  
        self.playlist_controls_layout.addLayout(self.volume_layout)  
    
    def connect_signals(self):  
        # 连接UI事件  
        self.play_button.clicked.connect(self.play_pause)  
        self.stop_button.clicked.connect(self.stop)  
        self.progress_slider.sliderMoved.connect(self.media_player.set_position)  
        
        # 连接媒体播放器信号  
        self.media_player.position_changed.connect(self.update_position)  
        self.media_player.duration_changed.connect(self.update_duration)  
        self.media_player.state_changed.connect(self.update_player_state)  
        
        # 添加播放列表控制信号连接
        self.prev_button.clicked.connect(self.play_previous)
        self.next_button.clicked.connect(self.play_next)
        self.mode_button.clicked.connect(self.toggle_play_mode)
        
        # 连接媒体播放结束信号，自动播放下一首
        self.media_player.player.mediaStatusChanged.connect(self.on_media_status_changed)
        
        # 连接播放列表信号
        self.playlist.current_index_changed.connect(self.update_current_track_info)
        
        # 连接音量控制信号  
        self.volume_slider.valueChanged.connect(self.media_player.set_volume)  
        self.mute_button.clicked.connect(self.toggle_mute)  
        self.media_player.volume_changed.connect(self.update_volume_ui)  

    # 添加音量控制相关方法  
    def toggle_mute(self):  
        self.media_player.toggle_mute() 
        
    @pyqtSlot(int)  
    def update_volume_ui(self, volume):  
        # 更新滑块位置  
        if not self.volume_slider.isSliderDown():  # 防止滑块正在拖动时被更新  
            self.volume_slider.setValue(volume)  
        
        # 更新静音按钮图标  
        if volume == 0 or self.media_player.is_muted():  
            self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))  
        else:  
            self.mute_button.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))  
            
    # 新增方法: 播放上一首
    def play_previous(self):
        previous_file = self.playlist.get_previous_item()
        if previous_file:
            self.play_file(previous_file)
            
    # 新增方法: 播放下一首
    def play_next(self):
        next_file = self.playlist.get_next_item()
        if next_file:
            self.play_file(next_file)
    
    # 新增方法: 切换播放模式
    def toggle_play_mode(self):
        current_mode = self.playlist.play_mode
        
        # 循环切换模式: 顺序 -> 循环 -> 随机 -> 顺序
        if current_mode == PlaylistMode.SEQUENTIAL:
            self.playlist.set_play_mode(PlaylistMode.LOOP)
            self.mode_button.setToolTip("播放模式: 循环播放")
            self.mode_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        elif current_mode == PlaylistMode.LOOP:
            self.playlist.set_play_mode(PlaylistMode.RANDOM)
            self.mode_button.setToolTip("播放模式: 随机播放")
            self.mode_button.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        else:  # RANDOM
            self.playlist.set_play_mode(PlaylistMode.SEQUENTIAL)
            self.mode_button.setToolTip("播放模式: 顺序播放")
            self.mode_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
    
    # 新增方法: 处理媒体状态变化
    def on_media_status_changed(self, status):
        # 当前曲目播放结束时，播放下一首
        if status == QMediaPlayer.EndOfMedia:
            self.play_next()
    
    # 新增方法: 更新当前播放曲目信息
    def update_current_track_info(self, index):
        if index >= 0:
            current_file = self.playlist.get_current_item()
            if current_file:
                self.current_file_label.setText(os.path.basename(current_file))
    
    # 修改原有的play_file方法，集成播放列表功能
    def play_file(self, file_path):
        # 加载文件所在文件夹作为播放列表
        self.playlist.load_from_folder(file_path)
        
        # 播放当前文件
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
