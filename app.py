import sys
import openai  # Use OpenAI SDK for DeepSeek API
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel, QLineEdit, QStackedWidget
from PyQt6.QtCore import Qt


class LoginScreen(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter ID")
        layout.addWidget(self.id_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.error_label = QLabel("")
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def check_login(self):
        user_id = self.id_input.text()
        password = self.password_input.text()

        # Replace with actual authentication logic
        if user_id == "admin" and password == "password123":
            self.main_app.setCurrentIndex(1)  # Switch to the main app screen
        else:
            self.error_label.setText("Invalid ID or Password")
            self.error_label.setStyleSheet("color: red;")


class DeepSeekApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DeepSeek AI App")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # File Upload Button
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button)

        # Question Input
        self.question_box = QTextEdit()
        self.question_box.setPlaceholderText("Ask a question...")
        layout.addWidget(self.question_box)
        self.question_box.setFocus()  # Set focus for enter key detection
        self.question_box.installEventFilter(self)  # Enable Enter key event

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)
        layout.addWidget(self.search_button)

        # Response Label
        self.response_label = QLabel("Response will appear here")
        layout.addWidget(self.response_label)

        self.setLayout(layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.response_label.setText(f"File uploaded: {file_path}")

    def perform_search(self):
        query = self.question_box.toPlainText().strip()

        if not query:
            self.response_label.setText("Please enter a question.")
            return

        self.response_label.setText("Searching...")

        # DeepSeek API Configuration using OpenAI SDK
        DEEPSEEK_API_KEY = "xxxx"  # Replace with your API key
        client = openai.OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",  # Adjust model name if needed
                messages=[{"role": "user", "content": query}],
                stream=False
            )

            ai_response = response.choices[0].message.content if response.choices else "No response"
            self.response_label.setText(ai_response)

        except Exception as e:
            self.response_label.setText(f"Error: {str(e)}")

    def eventFilter(self, obj, event):
        """Detect Enter key press inside the question box."""
        if obj == self.question_box and isinstance(event, QKeyEvent):
            if event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_Return:
                self.perform_search()
                return True
        return super().eventFilter(obj, event)


# Run the Application
app = QApplication(sys.argv)
stacked_widget = QStackedWidget()

login_screen = LoginScreen(stacked_widget)
main_app = DeepSeekApp()

stacked_widget.addWidget(login_screen)  # Index 0: Login Screen
stacked_widget.addWidget(main_app)      # Index 1: Main App

stacked_widget.setCurrentIndex(0)  # Show Login Screen First
stacked_widget.show()

sys.exit(app.exec())
