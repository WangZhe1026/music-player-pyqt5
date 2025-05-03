import os  
from PyQt5.QtWidgets import QTreeView, QFileSystemModel  
from PyQt5.QtCore import QDir, pyqtSignal, Qt  

class FileBrowser(QTreeView):  
    fileSelected = pyqtSignal(str)  
    
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.setup_ui()  
        
    def setup_ui(self):  
        # 创建文件树模型  
        self.model = QFileSystemModel()  
        self.model.setRootPath(QDir.rootPath())  
        
        # 仅显示常见音频文件类型  
        self.model.setNameFilters(["*.mp3", "*.wav", "*.ogg", "*.flac", "*.m4a"])  
        self.model.setNameFilterDisables(False)  
        
        # 设置树形视图  
        self.setModel(self.model)  
        self.setRootIndex(self.model.index(QDir.homePath()))  
        self.setMinimumWidth(250)  
        self.setAnimated(True)  
        self.setSortingEnabled(True)  
        
        # 隐藏不需要的列  
        for i in range(1, 4):  
            self.hideColumn(i)  
        
        # 连接信号槽  
        self.clicked.connect(self.on_item_clicked)  
    
    def on_item_clicked(self, index):  
        file_path = self.model.filePath(index)  
        if os.path.isfile(file_path) and any(file_path.lower().endswith(ext)   
                                            for ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']):  
            self.fileSelected.emit(file_path)  
    
    def set_root_path(self, path):  
        self.setRootIndex(self.model.index(path))  
