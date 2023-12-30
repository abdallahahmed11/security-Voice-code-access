from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import wavio as wv
from os import path
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import librosa

# import UI file
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=400, height=300, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=(0.0, 0.0, 0.0, 0.0), tight_layout=True)
        # self.fig.subplots_adjust(left=0.6, right=1.2, bottom=0.05, top=0.95)  # Adjust the padding
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        if parent:
            layout = QVBoxLayout(parent)
            layout.addWidget(self)
            layout.setStretch(0, 1)

        self.axes.clear()
        self.axes.set_facecolor('none')  # Set axes facecolor to transparent
        self.axes.set_xlabel('Time (s)')
        self.axes.set_ylabel('Frequency (Hz)')
        self.axes.set_title('Spectrogram')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_buttons()
        self.similarity_score_arr = [0]*8
        self.tableView = self.findChild(QTableView, 'tableView')
        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)
        self.add_data_to_model(self.similarity_score_arr)
        self.mpl_placeholder = self.findChild(QWidget, 'mplWidget')
        layout = QVBoxLayout(self.mpl_placeholder)
        self.sc = MplCanvas(self.mpl_placeholder, width=5, height=4, dpi=100)
        layout.addWidget(self.sc)
        layout.removeWidget(self.mpl_placeholder)

    def add_data_to_model(self, similarity_score_arr):
        data = [
            ["Mayar", similarity_score_arr[0]],
            ["Mayar", similarity_score_arr[1]],
            ["Mayar", similarity_score_arr[2]],
            ["Mayar", similarity_score_arr[3]],
            ["Mayar", similarity_score_arr[4]],
            ["Mayar", similarity_score_arr[5]],
            ["Mayar", similarity_score_arr[6]],
            ["Mayar", similarity_score_arr[7]]
        ]

        # Set the number of rows and columns in the model
        self.model.setRowCount(len(data))
        self.model.setColumnCount(len(data[0]))
        self.model.setHorizontalHeaderLabels(["Name", "Similarity Score"])
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # Add data to the model
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QStandardItem(str(value))
                self.model.setItem(i, j, item)

    def record_audio(self, duration=2, filename="recording.wav"):
        """
        Records audio for `duration` seconds and saves it to `filename`.
        """
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        wv.write(filename, recording, fs, sampwidth=2)
        self.audio_read(filename)

    def audio_read(self, filename):
        data, sf = librosa.load(filename)
        print("data: ", data)
        self.sc.axes.specgram(data, Fs=sf)
        self.sc.draw()

    def handle_buttons(self):
        self.recordButton.clicked.connect(lambda: self.record_audio(duration=2, filename="recording.wav"))


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    # app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()