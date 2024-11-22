import sys
import logging
from PyQt6.QtWidgets import QApplication
from .window import MainWindow
from .store import Store
from .anthropic import AnthropicClient

logging.basicConfig(filename='agent.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    app = QApplication(sys.argv)
    
    app.setQuitOnLastWindowClosed(True)  # Prevent app from quitting when window is closed
    
    store = Store()
    anthropic_client = AnthropicClient()
    
    window = MainWindow(store, anthropic_client)
    window.show()  # Just show normally, no maximize
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()