from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTableView, QPushButton, QMessageBox, QAction, 
    QDialog, QLineEdit, QFormLayout, QTextEdit, QHBoxLayout
)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
import os
import sys
import webbrowser

# Import my own Python packages
import get_mail

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Email Settings")
        self.resize(400, 175)

        layout = QFormLayout(self)

        self.emailEdit = QLineEdit()
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.imapEdit = QLineEdit()
        self.smtpEdit = QLineEdit()

        layout.addRow("Email:", self.emailEdit)
        layout.addRow("Password:", self.passwordEdit)
        layout.addRow("IMAP Server:", self.imapEdit)
        layout.addRow("SMTP Server:", self.smtpEdit)

        self.load_settings()

        self.saveButton = QPushButton("Save Settings")
        layout.addRow(self.saveButton)
        self.saveButton.clicked.connect(self.save_settings)

    def load_settings(self):
        if os.path.exists("settings.cfg"):
            with open("settings.cfg", "r") as f:
                lines = f.readlines()
                if len(lines) >= 4:
                    self.emailEdit.setText(lines[1].split("email = ")[1].strip())
                    self.passwordEdit.setText(lines[2].split("password = ")[1].strip())
                    self.imapEdit.setText(lines[3].split("imap_server = ")[1].strip())
                    self.smtpEdit.setText(lines[4].split("smtp_server = ")[1].strip())

    def save_settings(self):
        with open("settings.cfg", "w") as file:
            file.write("[EmailSettings]" + "\n")
            file.write("email = " + self.emailEdit.text() + "\n")
            file.write("password = " + self.passwordEdit.text() + "\n")
            file.write("imap_server = " + self.imapEdit.text() + "\n")
            file.write("smtp_server = " + self.smtpEdit.text() + "\n")

        QMessageBox.information(self, "Saved", "Settings saved successfully.")
        self.accept()


class EmailClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScnMsg Email Client")
        self.resize(1000, 800)

        # Set the window icon
        self.setWindowIcon(QIcon("./icons/ScnMsgIconShieldTransparent.png"))

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.receiveButton = QPushButton("Check for Emails")
        self.receiveButton.setFixedWidth(200)
        self.layout.addWidget(self.receiveButton)

        self.tableView = QTableView()
        self.layout.addWidget(self.tableView)

        self.openButton = QPushButton("Open Email")
        self.openReportButton = QPushButton("Open Report")

        

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Sender', 'Subject', 'Date'])
        self.tableView.setModel(self.model)
        self.tableView.setColumnWidth(0, 250)  # Sender column
        self.tableView.setColumnWidth(1, 450)  # Subject column
        self.tableView.setColumnWidth(2, 200)  # Date column
        self.download_and_update_emails()

        self.layout.addWidget(self.openButton)
        self.layout.addWidget(self.openReportButton)

        self.openButton.clicked.connect(self.open_selected_email)
        self.receiveButton.clicked.connect(self.download_and_update_emails)
        self.openReportButton.clicked.connect(self.open_email_report)

        self.setup_menubar()

    def setup_menubar(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("File")
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        settingsMenu = menubar.addMenu("Settings")
        settingsAction = QAction("Email Settings", self)
        settingsAction.triggered.connect(self.open_settings_dialog)
        settingsMenu.addAction(settingsAction)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def open_selected_email(self):
      indexes = self.tableView.selectionModel().selectedIndexes()
      if indexes:
        row = indexes[0].row()
        sender = self.model.item(row, 0).text()
        subject = self.model.item(row, 1).text()
        date = self.model.item(row, 2).text()

        email = get_mail.load_email(sender, subject, date)

        # Email content
        separator = "-------------------------------------------------------------------------------------------"
        email_content = f"From: {sender}\nSubject: {subject}\nDate: {date}\n\n{separator*2}\n\n{email.text}"

        # Create a dialog to show the email content
        email_dialog = QDialog(self)
        email_dialog.setWindowTitle(f"Email: {subject}")
        email_dialog.resize(1000, 800)

        layout = QVBoxLayout(email_dialog)

        # Scrollable text area to show email body
        email_display = QTextEdit()
        email_display.setText(email_content)
        email_display.setReadOnly(True)  # Disable editing the email content
        email_display.setWordWrapMode(True)
        layout.addWidget(email_display)

        # Create buttons at the bottom
        button_layout = QHBoxLayout()
        reply_button = QPushButton("Reply")
        ok_button = QPushButton("OK")

        # Add the buttons to the layout
        button_layout.addWidget(reply_button)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)

        # Reply button behavior
        reply_button.clicked.connect(lambda: self.open_reply_dialog(sender, subject))
        ok_button.clicked.connect(email_dialog.accept)

        email_dialog.exec_()
      else:
        QMessageBox.warning(self, "No Selection", "Select an email first.")


    def open_reply_dialog(self, sender, subject):
      # Create a dialog to type the reply
      reply_dialog = QDialog(self)
      reply_dialog.setWindowTitle(f"Reply to: {subject}")
      reply_dialog.resize(600, 300)

      layout = QVBoxLayout(reply_dialog)

      # Create a text box for the reply body
      reply_body = QTextEdit()
      layout.addWidget(reply_body)

      # Create the "Send Reply" button
      reply_button = QPushButton("Send Reply")
      layout.addWidget(reply_button)

      # Send reply behavior (we pass the original dialog to be closed later)
      reply_button.clicked.connect(lambda: self.send_reply(sender, subject, reply_body.toPlainText(), reply_dialog))

      reply_dialog.exec_()



    def send_reply(self, sender, subject, reply_body, reply_dialog):
      # Simulate sending the reply
      QMessageBox.information(
        self, "Reply Sent",
        f"Your reply to {sender} has been sent.\n\nThis functionality is currently not implemented and being simulated."
      )
      
      # Close both dialogs after sending the reply
      reply_dialog.accept()  # Close the "Reply to" dialog


    def download_and_update_emails(self):
        # Load email settings
        mail_username, mail_password, imap_server, smtp_server = get_mail.load_email_settings()  
        # Download emails from server and save as pickle objects
        get_mail.download_mail_from_server(mail_username, mail_password, imap_server, smtp_server)
        # Create summary of emails for table
        newest_mail, oldest_mail = get_mail.create_summary_of_emails(mail_username)
        # Populate table with emails
        self.populate_emails(newest_mail)

    def populate_emails(self, newest_mail):
        self.model.removeRows(0, self.model.rowCount())
        for email in newest_mail:
            self.model.appendRow([
                QStandardItem(email["sender"]),
                QStandardItem(email["subject"]),
                QStandardItem(email["date"])
            ])

    def load_email_settings(self):
        if not os.path.exists("settings.cfg"):
            QMessageBox.warning(self, "Missing Settings", "Email settings file not found.")
            return None

        with open("settings.cfg", "r") as f:
            lines = f.readlines()
            if len(lines) < 4:
                QMessageBox.warning(self, "Incomplete Settings", "Settings file is incomplete.")
                return None

            return {
                "email": lines[1].strip(),
                "password": lines[2].strip(),
                "imap": lines[3].strip(),
                "smtp": lines[4].strip()
            }

    def open_email_report(self):
        indexes = self.tableView.selectionModel().selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "No Selection", "Please select an email first.")
            return

        row = indexes[0].row()
        sender = self.model.item(row, 0).text()
        subject = self.model.item(row, 1).text()
        date = self.model.item(row, 2).text()

        # Load email settings
        mail_username, mail_password, imap_server, smtp_server = get_mail.load_email_settings()
        newest_mail, oldest_mail = get_mail.create_summary_of_emails(mail_username)

        for email in newest_mail:
            if email['sender'] == sender and email['subject'] == subject and email['date'] == date:
                report_filename = email['report_path']

        if os.path.exists(report_filename):
            webbrowser.open(report_filename)
        else:
            QMessageBox.warning(self, "Report Not Found", f"No report found for: {subject}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailClient()
    window.show()
    sys.exit(app.exec_())
