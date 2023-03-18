import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from GUI.WelcomeGUI import Ui_WelcomeWindow
from GUI.SettingsGUI import Ui_SettingsWindow
from GUI.SignupGUI import Ui_SignupWindow
from Storage import Storage


class SignupWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the UI from the imported class
        self.ui = Ui_SignupWindow()
        self.ui.setupUi(self)
        Storage.load_credentials()
        Storage.load_pokemon()

        # Connect label click events to custom methods
        self.ui.l6_pkmn1.mousePressEvent = lambda event: self.label_clicked(self.ui.l6_pkmn1)
        self.ui.l7_pkmn4.mousePressEvent = lambda event: self.label_clicked(self.ui.l7_pkmn4)
        self.ui.l8_pkmn7.mousePressEvent = lambda event: self.label_clicked(self.ui.l8_pkmn7)

        self.ui.b5_sign_up.clicked.connect(self.load_settings)

    @staticmethod
    def popup(message):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.exec_()

    def label_clicked(self, label):
        # Unset the border for all labels
        for l in [self.ui.l6_pkmn1, self.ui.l7_pkmn4, self.ui.l8_pkmn7]:
            l.setStyleSheet("")

        # Set a border for the clicked label
        label.setStyleSheet("border: 2px solid blue;")

    def load_settings(self):
        user = self.ui.t1_user.text()
        password = self.ui.t2_pass.text()

        # Checks if user exists
        if self.ui.t1_user.text() in Storage.cred.keys():
            print("User already exists")
            self.popup("User already exists!")

        # If user doesn't, then signs up and saves the starter pokemon to a dictionary in Storage.py
        else:
            Storage.cred[user] = password
            Storage.save_credentials()
            self.popup("Signed Up!")
            for l in [self.ui.l6_pkmn1, self.ui.l7_pkmn4, self.ui.l8_pkmn7]:
                if l.styleSheet() == "border: 2px solid blue;":
                    pokemon_name = l.objectName()[-1]
                    Storage.save_pokemon(user, pokemon_name)
        self.parent().parent().show_settings_window()


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None, stacked_widget=None):
        super().__init__(parent)

        # Set up the UI from the imported class
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        # All the button click events
        self.ui.b2_new_game.clicked.connect(lambda: self.new_game(stacked_widget))
        self.ui.b3_load_profile.clicked.connect(self.load_profile)
        self.ui.b4_records.clicked.connect(self.load_records)

    def new_game(self, stacked_widget):
        try:
            signup_window = SignupWindow(self)
            stacked_widget.addWidget(signup_window)
            stacked_widget.setCurrentWidget(signup_window)
        except Exception as e:
            print(f"Error in new_game: {e}")

    @staticmethod
    def load_profile():
        print("Load Game Clicked")

    @staticmethod
    def load_records():
        print("Records Clicked")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Pokemon League")

        # Create a stacked widget and set it as the central widget
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setFixedWidth(608)
        self.stacked_widget.setFixedHeight(391)
        self.setCentralWidget(self.stacked_widget)

        # Set the fixed size of the window
        self.setFixedSize(self.sizeHint())

        # Set up the UI from the imported class for WelcomeWindow
        self.welcome_window = QMainWindow()
        self.ui = Ui_WelcomeWindow()
        self.ui.setupUi(self.welcome_window)
        self.stacked_widget.addWidget(self.welcome_window)

        # Connect the button click events for WelcomeWindow
        self.ui.b1_start_game.clicked.connect(self.show_settings_window)

    def show_settings_window(self):
        # Show the settings window when the start game button is clicked
        self.settings_window = SettingsWindow(self, stacked_widget=self.stacked_widget)
        self.stacked_widget.addWidget(self.settings_window)
        self.stacked_widget.setCurrentWidget(self.settings_window)


if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
