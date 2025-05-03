from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QFileDialog  
from PyQt5.QtCore import QDir  
from src.ui.file_browser import FileBrowser  
from src.ui.player_widget import PlayerWidget  

class MusicPlayerWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        self.setup_ui()  
        self.connect_signals()  
    
    def setup_ui(self):  
        # 设置窗口标题和大小  
        self.setWindowTitle("music-player-pyqt5")  
        self.setGeometry(300, 300, 800, 500)  
        
        # 创建主窗口部件和布局  
        self.central_widget = QWidget()  
        self.setCentralWidget(self.central_widget)  
        self.main_layout = QHBoxLayout(self.central_widget)  
        
        # 创建文件浏览器  
        self.file_browser = FileBrowser()  
        
        # 创建播放器控件  
        self.player_widget = PlayerWidget()  
        
        # 添加组件到主布局  
        self.main_layout.addWidget(self.file_browser)  
        self.main_layout.addWidget(self.player_widget)  
    
    def connect_signals(self):  
        self.file_browser.fileSelected.connect(self.player_widget.play_file)  
        self.player_widget.folder_button.clicked.connect(self.open_folder)  
    
    def open_folder(self):  
        folder = QFileDialog.getExistingDirectory(self, "选择音乐文件夹", QDir.homePath())  
        if folder:  
            self.file_browser.set_root_path(folder)  
