"""Qt style sheet."""

APP_STYLE = """
QMainWindow, QWidget {
    background: #f4f6f9;
    color: #18202a;
    font-family: Segoe UI, Arial, sans-serif;
    font-size: 10pt;
}
QLineEdit, QComboBox {
    background: #ffffff;
    border: 1px solid #ccd5df;
    border-radius: 6px;
    padding: 8px 10px;
    min-height: 22px;
}
QLineEdit:focus, QComboBox:focus {
    border: 1px solid #2f6fed;
}
QPushButton {
    background: #2368d8;
    color: #ffffff;
    border: 0;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 600;
    min-height: 22px;
}
QPushButton:hover {
    background: #1d5fc9;
}
QPushButton:disabled {
    background: #aeb8c4;
    color: #ffffff;
}
QPushButton#secondary {
    background: #ffffff;
    color: #172033;
    border: 1px solid #cbd5e1;
}
QPushButton#secondary:hover {
    background: #f7f9fc;
    border: 1px solid #9fb0c3;
}
QFrame#card {
    background: #ffffff;
    border: 1px solid #d9e1eb;
    border-radius: 8px;
}
QFrame#card:hover {
    border: 1px solid #b8c6d8;
}
QLabel#title {
    font-size: 12pt;
    font-weight: 700;
    color: #111827;
}
QLabel#subtitle {
    color: #5b6778;
    font-size: 9pt;
}
QLabel#description {
    color: #293547;
}
QLabel#badge {
    border-radius: 6px;
    padding: 5px 9px;
    background: #e8eef6;
    color: #24344d;
    font-weight: 600;
}
QLabel#badgeRunning {
    border-radius: 6px;
    padding: 5px 9px;
    background: #dcfce7;
    color: #166534;
    font-weight: 700;
}
QLabel#badgeStarting {
    border-radius: 6px;
    padding: 5px 9px;
    background: #dbeafe;
    color: #1e40af;
    font-weight: 700;
}
QLabel#badgeFailed {
    border-radius: 6px;
    padding: 5px 9px;
    background: #fee2e2;
    color: #991b1b;
    font-weight: 700;
}
QLabel#summary {
    color: #516070;
    padding-left: 8px;
}
"""
