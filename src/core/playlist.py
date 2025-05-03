import os  
import random  
from PyQt5.QtCore import QObject, pyqtSignal  
from src.utils.file_utils import is_audio_file  

class PlaylistMode:  
    """播放列表模式枚举"""  
    SEQUENTIAL = 0  # 顺序播放  
    LOOP = 1        # 循环播放  
    RANDOM = 2      # 随机播放  

class Playlist(QObject):  
    """播放列表管理类"""  
    # 播放列表变化信号  
    playlist_changed = pyqtSignal(list)  # 播放列表内容改变  
    current_index_changed = pyqtSignal(int)  # 当前播放索引改变  
    
    def __init__(self):  
        super().__init__()  
        self.items = []  # 播放列表项目  
        self.current_index = -1  # 当前播放索引  
        self.play_mode = PlaylistMode.SEQUENTIAL  # 默认为顺序播放  
        self.history = []  # 随机播放模式下的历史记录  
    
    def load_from_folder(self, file_path):  
        """从文件所在文件夹加载播放列表"""  
        if not os.path.exists(file_path):  
            return False  
            
        # 获取文件所在文件夹  
        folder = os.path.dirname(file_path)  
        current_file = os.path.basename(file_path)  
        
        # 获取文件夹中所有音频文件  
        files = []  
        for file in os.listdir(folder):  
            full_path = os.path.join(folder, file)  
            if os.path.isfile(full_path) and is_audio_file(full_path):  
                files.append(full_path)  
        
        # 按文件名排序  
        files.sort()  
        
        # 设置播放列表  
        self.items = files  
        
        # 查找当前文件索引  
        try:  
            self.current_index = self.items.index(file_path)  
        except ValueError:  
            self.current_index = 0 if self.items else -1  
        
        # 清空历史  
        self.history = []  
        
        # 发出信号  
        self.playlist_changed.emit(self.items)  
        self.current_index_changed.emit(self.current_index)  
        
        return True  
    
    def set_play_mode(self, mode):  
        """设置播放模式"""  
        if mode in (PlaylistMode.SEQUENTIAL, PlaylistMode.LOOP, PlaylistMode.RANDOM):  
            self.play_mode = mode  
            # 随机模式时重置历史  
            if mode == PlaylistMode.RANDOM:  
                self.history = [self.current_index] if self.current_index >= 0 else []  
    
    def get_current_item(self):  
        """获取当前项目"""  
        if 0 <= self.current_index < len(self.items):  
            return self.items[self.current_index]  
        return None  
    
    def get_next_item(self):  
        """获取下一个播放项目"""  
        if not self.items:  
            return None  
            
        next_index = self.get_next_index()  
        if next_index >= 0:  
            self.current_index = next_index  
            self.current_index_changed.emit(self.current_index)  
            return self.items[self.current_index]  
        
        return None  
    
    def get_previous_item(self):  
        """获取上一个播放项目"""  
        if not self.items:  
            return None  
            
        prev_index = self.get_previous_index()  
        if prev_index >= 0:  
            self.current_index = prev_index  
            self.current_index_changed.emit(self.current_index)  
            return self.items[self.current_index]  
        
        return None  
    
    def get_next_index(self):  
        """根据播放模式获取下一个索引"""  
        if not self.items:  
            return -1  
            
        if self.play_mode == PlaylistMode.RANDOM:  
            return self._get_random_index()  
            
        next_index = self.current_index + 1  
        
        # 如果是循环模式，到达末尾时回到开始  
        if next_index >= len(self.items):  
            if self.play_mode == PlaylistMode.LOOP:  
                next_index = 0  
            else:  
                next_index = -1  
                
        return next_index  
    
    def get_previous_index(self):  
        """根据播放模式获取上一个索引"""  
        if not self.items:  
            return -1  
            
        if self.play_mode == PlaylistMode.RANDOM:  
            # 从历史记录中获取上一个  
            if len(self.history) > 1:  
                self.history.pop()  # 移除当前索引  
                return self.history[-1]  # 返回新的当前索引  
            return self.current_index  
            
        prev_index = self.current_index - 1  
        
        # 如果是循环模式，到达开头时跳到末尾  
        if prev_index < 0:  
            if self.play_mode == PlaylistMode.LOOP:  
                prev_index = len(self.items) - 1  
                
        return prev_index  
    
    def _get_random_index(self):  
        """获取随机索引（不重复）"""  
        if len(self.items) <= 1:  
            return 0 if self.items else -1  
            
        # 如果已经播放了所有歌曲，重新开始  
        if len(self.history) >= len(self.items):  
            self.history = [self.current_index]  
            
        # 选择一个未播放过的索引  
        available_indices = [i for i in range(len(self.items)) if i not in self.history]  
        if not available_indices:  
            return -1  
            
        next_index = random.choice(available_indices)  
        self.history.append(next_index)  
        return next_index  
    
    def get_playlist_items(self):  
        """获取播放列表项目"""  
        return self.items  
    
    def get_item_at(self, index):  
        """获取指定索引的项目"""  
        if 0 <= index < len(self.items):  
            return self.items[index]  
        return None  
    
    def set_current_index(self, index):  
        """设置当前索引"""  
        if 0 <= index < len(self.items):  
            self.current_index = index  
            
            # 随机模式下更新历史  
            if self.play_mode == PlaylistMode.RANDOM:  
                if self.current_index not in self.history:  
                    self.history.append(self.current_index)  
                    
            self.current_index_changed.emit(self.current_index)  
            return self.items[self.current_index]  
        return None  
    
    def clear(self):  
        """清空播放列表"""  
        self.items = []  
        self.current_index = -1  
        self.history = []  
        self.playlist_changed.emit(self.items)  
        self.current_index_changed.emit(self.current_index)