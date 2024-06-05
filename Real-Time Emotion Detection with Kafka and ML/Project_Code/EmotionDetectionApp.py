import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLineEdit,
                             QPushButton, QLabel, QMessageBox, QVBoxLayout, QFormLayout)
from PyQt5.QtCore import Qt
from Emotion_kafka_producer import *

class EmotionDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.user_inputs = []  # List to store user input

    def initUI(self):
        main_layout = QVBoxLayout()  # Main layout
        main_layout.setSpacing(20)  # Equal spacing between all widgets
        
        # Welcome Label
        self.welcome_label = QLabel('Welcome to Emotion Detection', self)
        self.welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2a2a2a;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.welcome_label)

        # Info Label
        self.info_label = QLabel('Understand your emotions by entering your thoughts.\nLet us help you understand your feelings!', self)
        self.info_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.info_label)

        # Textbox
        formLayout = QFormLayout()
        self.textbox = QLineEdit(self)
        formLayout.addRow("Enter Text:", self.textbox)
        main_layout.addLayout(formLayout)
        self.textbox.setFixedWidth(320)

        # Submit Button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3; 
            }
        """)
        self.submit_button.clicked.connect(self.onSubmit)
        main_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        # Privacy Notice
        self.privacy_notice = QLabel('Privacy Assurance: Your emotional insights remain yours alone.\nWe respect your privacy and do not share your entries.', self)
        self.privacy_notice.setAlignment(Qt.AlignCenter)
        self.privacy_notice.setStyleSheet("font-size: 11px; color: #6c757d; padding-top: 10px;")
        main_layout.addWidget(self.privacy_notice)

        self.setLayout(main_layout)
        self.setWindowTitle('Emotion Detection Application')
        self.resize(500, 300)
        self.setFixedSize(500, 280)
        self.show()

    def onSubmit(self):
        text = self.textbox.text()
        self.user_inputs.append(text)
        print("Stored Text:", self.user_inputs)  # Print stored text
        producer = Emotion_kafka_producer()
        producer.send(text)
        #Emotion_kafka_producer.send(self,self.user_inputs)  # Send text to Kafka producer

        msg = QMessageBox()
        msg.setWindowTitle("Notification")
        msg.setText("User Input Stored Successfully!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

        self.textbox.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmotionDetectionApp()
    sys.exit(app.exec_())
