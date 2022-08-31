from pathlib import Path
from tkinter.ttk import Progressbar

import librosa
import numpy
from project import Project
import soundfile

from PyQt6.QtCore import QObject, QRunnable, pyqtSlot, pyqtSignal

from preferences import PREFERENCES

class WorkerSignals(QObject):
    finished = pyqtSignal(Project)
    progress = pyqtSignal(int)
    current_task = pyqtSignal(str)

class AnalysisWorker(QRunnable):
    def __init__(self, project_name:str, filepath:Path):
        super(AnalysisWorker, self).__init__()
        self.signals = WorkerSignals()
        
        self.project_name = project_name
        self.filepath = filepath
    
    @pyqtSlot()
    def run(self):
        
        self.signals.current_task.emit("Loading audio...")
        channel_data, samplerate = soundfile.read(self.filepath)
        self.signals.progress.emit(25)
        y, sr = librosa.load(self.filepath)
        self.signals.progress.emit(50)
        
        self.signals.current_task.emit("Analysing audio...")
        tempo, beat_samples = librosa.beat.beat_track(y=y, sr=sr, units="samples")
        silent_sample_count = beat_samples[0]
        samples_per_beat = samplerate * 60 / tempo
        self.signals.progress.emit(70)
        
        self.signals.current_task.emit("Synchronising audio...")
        channel_count = numpy.shape(channel_data)[1]
        start_rest_duration = PREFERENCES.start_rest_duration
        sample_count_difference = silent_sample_count - round(
            start_rest_duration * samples_per_beat
        )
        if sample_count_difference < 0:
            channel_data = channel_data[2 - sample_count_difference :]
        else:
            frames_offset = numpy.zeros([sample_count_difference, channel_count])
            channel_data = numpy.append(frames_offset, channel_data, axis=0)
        self.signals.progress.emit(90)
    
        self.signals.current_task.emit("Saving data...")
        project = Project(self.project_name)
        project.metadata.set("tempo", tempo)
        project.metadata.save()
        project.write_audio("song.wav", channel_data, samplerate)
        self.signals.progress.emit(100)
        self.signals.finished.emit(project)