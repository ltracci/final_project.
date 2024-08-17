
from PyQt6.QtWidgets import QApplication
from logic import Logic

def main():
	app = QApplication([])
	window = Logic()
	window.show()
	app.exec()

if __name__ == '__main__':
	main()
