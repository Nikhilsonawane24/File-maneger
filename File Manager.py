import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QInputDialog

class FolderManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Folder Manager")
        self.setGeometry(100, 100, 600, 500)

        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()

        self.main_folder_name_label = QLabel("Main Folder Name:")
        self.main_folder_name_entry = QLineEdit()
        layout.addWidget(self.main_folder_name_label)
        layout.addWidget(self.main_folder_name_entry)

        self.subfolder_name_label = QLabel("Subfolder Name(s):")
        self.subfolder_name_entry = QLineEdit()
        layout.addWidget(self.subfolder_name_label)
        layout.addWidget(self.subfolder_name_entry)

        self.create_main_folder_button = QPushButton("Create Main Folder with Subfolders")
        self.create_main_folder_button.clicked.connect(self.create_main_folder_with_subfolders)
        layout.addWidget(self.create_main_folder_button)

        self.spacer_label = QLabel()  # Spacer label
        layout.addWidget(self.spacer_label)

        self.rename_files_button = QPushButton("Rename Files")
        self.rename_files_button.clicked.connect(self.rename_files)
        layout.addWidget(self.rename_files_button)

        self.classify_files_button = QPushButton("Classify Files")
        self.classify_files_button.clicked.connect(self.classify_files)
        layout.addWidget(self.classify_files_button)

        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def create_main_folder_with_subfolders(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Folder to Create Main Folder In")
        main_folder_name = self.main_folder_name_entry.text()
        subfolder_names = self.subfolder_name_entry.text()

        if not selected_folder:
            self.status_label.setText("Please select a folder where you want to create the main folder.")
            return

        if not main_folder_name:
            self.status_label.setText("Please enter a name for the main folder.")
            return

        subfolder_names = subfolder_names.split(",")
        subfolder_names = [name.strip() for name in subfolder_names if name.strip()]  # Filter out empty and whitespace names

        if not subfolder_names:
            self.status_label.setText("No valid subfolder names provided.")
            return

        main_folder_path = os.path.join(selected_folder, main_folder_name)
        os.mkdir(main_folder_path)

        for subfolder_name in subfolder_names:
            current_folder = main_folder_path
            subfolder_parts = subfolder_name.split("/")
            
            for part in subfolder_parts:
                current_folder = os.path.join(current_folder, part)
                os.mkdir(current_folder)

        self.status_label.setText(f"Created main folder: {main_folder_name} with subfolders.")

    def rename_files(self):
        selected_files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Rename")

        if not selected_files:
            self.status_label.setText("No files selected.")
            return

        renaming_option, ok = QInputDialog.getItem(self, "Select Renaming Option", "Choose an option:",
                                                   ["Add Prefix", "Add Suffix", "Change Name"], 0, False)

        if ok:
            if renaming_option == "Add Prefix":
                prefix, ok = QInputDialog.getText(self, "Add Prefix", "Enter the prefix:")
                if ok:
                    self.rename_files_with_prefix(selected_files, prefix)
            elif renaming_option == "Add Suffix":
                suffix, ok = QInputDialog.getText(self, "Add Suffix", "Enter the suffix:")
                if ok:
                    self.rename_files_with_suffix(selected_files, suffix)
            elif renaming_option == "Change Name":
                new_name, ok = QInputDialog.getText(self, "Change Name", "Enter the new name:")
                if ok:
                    self.rename_files_with_new_name(selected_files, new_name)

    def rename_files_with_prefix(self, selected_files, prefix):
        for i, file_path in enumerate(selected_files):
            file_dir, file_name = os.path.split(file_path)
            name, ext = os.path.splitext(file_name)
            new_name = f"{prefix} {name}{ext}"
            os.rename(file_path, os.path.join(file_dir, new_name))

        self.status_label.setText("Renamed selected files with a prefix.")

    def rename_files_with_suffix(self, selected_files, suffix):
        for i, file_path in enumerate(selected_files):
            file_dir, file_name = os.path.split(file_path)
            name, ext = os.path.splitext(file_name)
            new_name = f"{name} {suffix}{ext}"
            os.rename(file_path, os.path.join(file_dir, new_name))

        self.status_label.setText("Renamed selected files with a suffix.")

    def rename_files_with_new_name(self, selected_files, new_name):
        for i, file_path in enumerate(selected_files):
            file_dir, file_name = os.path.split(file_path)
            _, ext = os.path.splitext(file_name)
            new_file_name = f"{new_name} {i:02d}{ext}"
            os.rename(file_path, os.path.join(file_dir, new_file_name))

        self.status_label.setText("Renamed selected files with a new name.")

    def classify_files(self):
        selected_files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Classify")

        if not selected_files:
            self.status_label.setText("No files selected.")
            return
file_classification = {
    "Images": (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff"),
    "Videos": (".mov", ".mp4", ".avi", ".mkv", ".wmv"),
    "Audio": (".mp3", ".wav", ".flac", ".aac"),
    "Documents": (".doc", ".docx", ".pdf", ".txt", ".rtf", ".ppt", ".pptx", ".xls", ".xlsx")
}

        for file_path in selected_files:
            file_extension = os.path.splitext(file_path)[1].lower()
            for folder_name, extensions in file_classification.items():
                if file_extension in extensions:
                    selected_folder = os.path.dirname(file_path)
                    destination_folder = os.path.join(selected_folder, folder_name)
                    os.makedirs(destination_folder, exist_ok=True)
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(destination_folder, file_name)
                    os.rename(file_path, destination_path)

        self.status_label.setText("Files classified and moved to respective folders.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderManagerApp()
    ex.show()
    sys.exit(app.exec_())
