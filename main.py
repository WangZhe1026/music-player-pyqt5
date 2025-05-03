import sys  
from PyQt5.QtWidgets import QApplication  
from src.ui.main_window import MusicPlayerWindow  

def main():  
    app = QApplication(sys.argv)  
    player = MusicPlayerWindow()  
    player.show()  
    sys.exit(app.exec_())  

if __name__ == "__main__":  
    main()  
