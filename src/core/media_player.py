from PyQt5.QtCore import QObject, pyqtSignal, QUrl  
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent  

class MediaPlayer(QObject):  
    position_changed = pyqtSignal(int)  
    duration_changed = pyqtSignal(int)  
    state_changed = pyqtSignal(int)  
    volume_changed = pyqtSignal(int)  # 新增音量变化信号  
    
    # 状态常量  
    PLAYING_STATE = QMediaPlayer.PlayingState  
    PAUSED_STATE = QMediaPlayer.PausedState  
    STOPPED_STATE = QMediaPlayer.StoppedState  
    
    def __init__(self):  
        super().__init__()  
        self.player = QMediaPlayer()  
        self.duration = 0  
        self.connect_signals()  
        self.player.setVolume(50)  # 设置默认音量为50%  
    
    def connect_signals(self):  
        self.player.positionChanged.connect(self.on_position_changed)  
        self.player.durationChanged.connect(self.on_duration_changed)  
        self.player.stateChanged.connect(self.on_state_changed)  
    
    def load_file(self, file_path):  
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_path)))  
    
    def play(self):  
        self.player.play()  
    
    def pause(self):  
        self.player.pause()  
    
    def stop(self):  
        self.player.stop()  
    
    def toggle_play_pause(self):  
        if self.player.state() == QMediaPlayer.PlayingState:  
            self.pause()  
        else:  
            self.play()  
    
    def set_position(self, position):  
        self.player.setPosition(position)  
    
    def on_position_changed(self, position):  
        self.position_changed.emit(position)  
    
    def on_duration_changed(self, duration):  
        self.duration = duration  
        self.duration_changed.emit(duration)  
    
    def on_state_changed(self, state):  
        self.state_changed.emit(state)  

     # 添加音量控制方法  
    def set_volume(self, volume):  
        self.player.setVolume(volume)  
        self.volume_changed.emit(volume)  
    
    def get_volume(self):  
        return self.player.volume()  
    
    def toggle_mute(self):  
        self.player.setMuted(not self.player.isMuted())  
        # 发送当前音量信号 (如果静音则为0)  
        volume = 0 if self.player.isMuted() else self.player.volume()  
        self.volume_changed.emit(volume)  
    
    def is_muted(self):  
        return self.player.isMuted()  
