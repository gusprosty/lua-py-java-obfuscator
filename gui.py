import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QComboBox, QLabel, 
                             QFileDialog, QMessageBox, QProgressBar,
                             QSplitter, QGroupBox, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from obfuscators.lua_obfuscator import LuaObfuscator
from obfuscators.python_obfuscator import PythonObfuscator
from obfuscators.java_obfuscator import JavaObfuscator

class ObfuscationThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, language, code, options):
        super().__init__()
        self.language = language
        self.code = code
        self.options = options

    def run(self):
        try:
            if self.language == "Lua":
                obfuscator = LuaObfuscator()
            elif self.language == "Python":
                obfuscator = PythonObfuscator()
            elif self.language == "Java":
                obfuscator = JavaObfuscator()
            else:
                self.error.emit("Unsupported language")
                return

            self.progress.emit(30)
            obfuscated_code = obfuscator.obfuscate(self.code, self.options)
            self.progress.emit(100)
            self.finished.emit(obfuscated_code)
            
        except Exception as e:
            self.error.emit(str(e))

class ObfuscatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Multi-Language Obfuscator")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Lua", "Python", "Java"])
        controls_layout.addWidget(QLabel("Language:"))
        controls_layout.addWidget(self.language_combo)
        
        self.load_btn = QPushButton("Load File")
        self.load_btn.clicked.connect(self.load_file)
        controls_layout.addWidget(self.load_btn)
        
        self.obfuscate_btn = QPushButton("Obfuscate")
        self.obfuscate_btn.clicked.connect(self.obfuscate_code)
        controls_layout.addWidget(self.obfuscate_btn)
        
        self.save_btn = QPushButton("Save Result")
        self.save_btn.clicked.connect(self.save_result)
        controls_layout.addWidget(self.save_btn)
        
        layout.addLayout(controls_layout)
        
        # Options group
        options_group = QGroupBox("Obfuscation Options")
        options_layout = QHBoxLayout()
        
        self.rename_vars = QCheckBox("Rename Variables")
        self.rename_vars.setChecked(True)
        options_layout.addWidget(self.rename_vars)
        
        self.obfuscate_strings = QCheckBox("Obfuscate Strings")
        self.obfuscate_strings.setChecked(True)
        options_layout.addWidget(self.obfuscate_strings)
        
        self.encrypt_code = QCheckBox("Encrypt Code")
        options_layout.addWidget(self.encrypt_code)
        
        self.remove_comments = QCheckBox("Remove Comments")
        self.remove_comments.setChecked(True)
        options_layout.addWidget(self.remove_comments)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Splitter for code editors
        splitter = QSplitter(Qt.Horizontal)
        
        # Input code editor
        self.input_editor = QTextEdit()
        self.input_editor.setPlaceholderText("Enter your code here or load from file...")
        
        # Output code editor
        self.output_editor = QTextEdit()
        self.output_editor.setPlaceholderText("Obfuscated code will appear here...")
        self.output_editor.setReadOnly(True)
        
        splitter.addWidget(self.input_editor)
        splitter.addWidget(self.output_editor)
        splitter.setSizes([600, 600])
        
        layout.addWidget(splitter)
        
        # Status labels
        status_layout = QHBoxLayout()
        self.input_size_label = QLabel("Input size: 0 characters")
        self.output_size_label = QLabel("Output size: 0 characters")
        status_layout.addWidget(self.input_size_label)
        status_layout.addStretch()
        status_layout.addWidget(self.output_size_label)
        
        layout.addLayout(status_layout)
        
        # Connect signals
        self.input_editor.textChanged.connect(self.update_input_size)
        
    def update_input_size(self):
        size = len(self.input_editor.toPlainText())
        self.input_size_label.setText(f"Input size: {size} characters")
        
    def update_output_size(self, size):
        self.output_size_label.setText(f"Output size: {size} characters")
        
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", 
            "All Files (*);;Lua Files (*.lua);;Python Files (*.py);;Java Files (*.java)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_editor.setPlainText(content)
                    
                    # Auto-detect language from file extension
                    ext = os.path.splitext(file_path)[1].lower()
                    if ext == '.lua':
                        self.language_combo.setCurrentText("Lua")
                    elif ext == '.py':
                        self.language_combo.setCurrentText("Python")
                    elif ext == '.java':
                        self.language_combo.setCurrentText("Java")
                        
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
                
    def save_result(self):
        obfuscated_code = self.output_editor.toPlainText()
        if not obfuscated_code:
            QMessageBox.warning(self, "Warning", "No obfuscated code to save")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Obfuscated Code", "", 
            "All Files (*);;Lua Files (*.lua);;Python Files (*.py);;Java Files (*.java)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(obfuscated_code)
                QMessageBox.information(self, "Success", "File saved successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                
    def obfuscate_code(self):
        code = self.input_editor.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "Warning", "Please enter code to obfuscate")
            return
            
        language = self.language_combo.currentText()
        
        options = {
            'rename_variables': self.rename_vars.isChecked(),
            'obfuscate_strings': self.obfuscate_strings.isChecked(),
            'encrypt_code': self.encrypt_code.isChecked(),
            'remove_comments': self.remove_comments.isChecked()
        }
        
        self.progress_bar.setVisible(True)
        self.obfuscate_btn.setEnabled(False)
        
        self.thread = ObfuscationThread(language, code, options)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.on_obfuscation_finished)
        self.thread.error.connect(self.on_obfuscation_error)
        self.thread.start()
        
    def on_obfuscation_finished(self, result):
        self.output_editor.setPlainText(result)
        self.update_output_size(len(result))
        self.progress_bar.setVisible(False)
        self.obfuscate_btn.setEnabled(True)
        QMessageBox.information(self, "Success", "Code obfuscated successfully")
        
    def on_obfuscation_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.obfuscate_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", f"Obfuscation failed: {error_message}")