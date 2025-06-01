from qtpy.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QFontDialog, QComboBox, QVBoxLayout
from qtpy.Qsci import QsciScintilla, QsciLexerPython
from qtpy.QtGui import QFontMetrics, QColor

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # QScintilla のエディタを作成
        self.editor = QsciScintilla()
        self.editor.linesChanged.connect(self.adjust_margin_width)
        self.setCentralWidget(self.editor)

        lexer = QsciLexerPython()
        lexer.setDefaultPaper(QColor("#2E2E2E"))  # **背景色を変更**
        lexer.setDefaultColor(QColor("#FFFFFF"))  # **テキストの色を変更**
        self.editor.setLexer(lexer)

        # メニューの追加
        self.create_menu()

        # 初期設定
        self.setWindowTitle("QtPy + QScintilla Editor")
        self.resize(800, 600)

    def create_menu(self):
        menu_bar = self.menuBar()

        # ファイルメニュー
        file_menu = menu_bar.addMenu("ファイル(&F)")

        # **開くを追加**
        open_action = QAction("開く(&O)", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # **保存を追加**
        save_action = QAction("保存(&S)", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # **終了を追加**
        exit_action = QAction("終了", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 表示メニュー
        view_menu = menu_bar.addMenu("表示(&F)")

        # **行番号を追加**
        toggle_line_numbers_action = QAction("行番号(&L)", self, checkable=True)
        toggle_line_numbers_action.setChecked(False)
        toggle_line_numbers_action.triggered.connect(self.toggle_line_numbers)
        view_menu.addAction(toggle_line_numbers_action)

        self.editor.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_LINENUMBER, 0xFFFFFF)
        self.editor.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_LINENUMBER, 0x3C3C3C)

        # **フォント変更を追加**
        font_action = QAction("フォント(&F)", self)
        font_action.triggered.connect(self.change_font)

        view_menu.addAction(font_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "ファイルを開く", "", "テキストファイル (*.txt);;すべてのファイル (*.*)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                self.editor.setText(f.read())

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "ファイルを保存", "", "テキストファイル (*.txt);;すべてのファイル (*.*)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.text())

    def adjust_margin_width(self):
        if self.editor.marginWidth(0) != 0:
            line_count = self.editor.lines()
            digit_count = len(str(line_count))
            font_metrics = QFontMetrics(self.editor.font())
            char_width = font_metrics.horizontalAdvance("0")
            margin_width = char_width * (digit_count + 2)
            self.editor.setMarginWidth(0, margin_width)

    def toggle_line_numbers(self):
        if self.editor.marginWidth(0) == 0:
            self.editor.setMarginWidth(0, 40)
            self.adjust_margin_width()
        else:
            self.editor.setMarginWidth(0, 0)

    def change_font(self):
        current_font = self.editor.font()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            self.editor.setFont(font)
            self.adjust_margin_width()

# アプリケーションの実行
app = QApplication([])
# アプリケーションのスタイルを設定
app.setStyleSheet("""
QWidget     { background-color: #2E2E2E; color: #FFFFFF;}
QScintilla  { background-color: #2E2E2E; color: #FFFFFF;}
QFileDialog { background-color: #2E2E2E; color: #FFFFFF;}
QMenuBar::item:selected {background-color: #444444; color: #FFFFFF;}
QMenuBar::item:pressed {background-color: #555555;color: #FFFFFF;}
QMenu { background-color: #444444; color: #FFFFFF; }
QMenu::item:selected { background-color: #555555; color: #FFFFFF; }
QMenu::item:pressed { background-color: #666666; color: #FFFFFF; }
""")
window = TextEditor()
window.show()
app.exec()
