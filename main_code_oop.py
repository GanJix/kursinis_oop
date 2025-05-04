import tkinter as tk
from tkinter import Menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import welch
from scipy.signal.windows import hann

class GraphStrategy:
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        raise NotImplementedError("Subclasses should implement this!")

class XAxisGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        plt.figure(figsize=(8, 6))
        plt.plot(relative_time, acc_x, 'r', linewidth=1.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (G)')
        plt.title('X-axis Acceleration')
        plt.grid(True)
        plt.show()

class YAxisGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        plt.figure(figsize=(8, 6))
        plt.plot(relative_time, acc_y, 'g', linewidth=1.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (G)')
        plt.title('Y-axis Acceleration')
        plt.grid(True)
        plt.show()

class ZAxisGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        plt.figure(figsize=(8, 6))
        plt.plot(relative_time, acc_z, 'b', linewidth=1.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (G)')
        plt.title('Z-axis Acceleration')
        plt.grid(True)
        plt.show()

class AllAxesGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        plt.figure(figsize=(8, 6))
        plt.plot(relative_time, acc_x, 'r', linewidth=1.5)
        plt.plot(relative_time, acc_y, 'g', linewidth=1.5)
        plt.plot(relative_time, acc_z, 'b', linewidth=1.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (G)')
        plt.title('All Axes Acceleration')
        plt.legend(['X-axis', 'Y-axis', 'Z-axis'])
        plt.grid(True)
        plt.show()

class FFTZGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        N = len(acc_z)
        Fs = 1 / np.mean(np.diff(relative_time)) 
        Y = fft(acc_z)
        P2 = np.abs(Y / N)
        P1 = P2[:N // 2 + 1]
        P1[1:-1] = 2 * P1[1:-1]
        f = Fs * np.arange(0, N // 2 + 1) / N
        plt.figure(figsize=(8, 6))
        plt.plot(f, P1, linewidth=1.5)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Amplitude')
        plt.title('FFT of Z-axis Acceleration')
        plt.grid(True)
        plt.show()

class GraphContext:
    def __init__(self, strategy: GraphStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: GraphStrategy):
        self._strategy = strategy

    def plot(self, relative_time, acc_x, acc_y, acc_z):
        self._strategy.plot(relative_time, acc_x, acc_y, acc_z)

class AccelerometerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Accelerometer Data Processor")
        
        self.menu_frame = tk.Frame(master)
        self.menu_frame.pack(side="top", fill="x", pady=10)

        self.btn_x_axis = tk.Button(self.menu_frame, text="X-axis Acc", command=self.plot_x_axis)
        self.btn_x_axis.pack(side="left", padx=5)

        self.btn_y_axis = tk.Button(self.menu_frame, text="Y-axis Acc", command=self.plot_y_axis)
        self.btn_y_axis.pack(side="left", padx=5)

        self.btn_z_axis = tk.Button(self.menu_frame, text="Z-axis Acc", command=self.plot_z_axis)
        self.btn_z_axis.pack(side="left", padx=5)

        self.btn_all_axes = tk.Button(self.menu_frame, text="All Axes Acc", command=self.plot_all_axes)
        self.btn_all_axes.pack(side="left", padx=5)

        self.btn_fft_z = tk.Button(self.menu_frame, text="FFT of Z-axis", command=self.plot_fft_z)
        self.btn_fft_z.pack(side="left", padx=5)

        self.filename = 'MSR457988x_250314_163216.csv'  
        self.data = self.load_data(self.filename)

    def load_data(self, filename):
        data = pd.read_csv(filename, delimiter=';', engine='python', skiprows=4)
        
        time_column = data.columns[0]
        time_str = data[time_column] 
        time_parsed = pd.to_datetime(time_str, format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
        time_seconds = (time_parsed - time_parsed.iloc[0]).dt.total_seconds()

        acc_x = pd.to_numeric(data.iloc[:, 1], errors='coerce')
        acc_y = pd.to_numeric(data.iloc[:, 2], errors='coerce')
        acc_z = pd.to_numeric(data.iloc[:, 3], errors='coerce')

        valid_data = ~acc_x.isna() & ~acc_y.isna() & ~acc_z.isna()
        time_seconds = time_seconds[valid_data]
        acc_x = acc_x[valid_data]
        acc_y = acc_y[valid_data]
        acc_z = acc_z[valid_data]

        return time_seconds, acc_x, acc_y, acc_z

    def plot_x_axis(self):
        context = GraphContext(XAxisGraph())
        context.plot(self.data[0], self.data[1], self.data[2], self.data[3])

    def plot_y_axis(self):
        context = GraphContext(YAxisGraph())
        context.plot(self.data[0], self.data[1], self.data[2], self.data[3])

    def plot_z_axis(self):
        context = GraphContext(ZAxisGraph())
        context.plot(self.data[0], self.data[1], self.data[2], self.data[3])

    def plot_all_axes(self):
        context = GraphContext(AllAxesGraph())
        context.plot(self.data[0], self.data[1], self.data[2], self.data[3])

    def plot_fft_z(self):
        context = GraphContext(FFTZGraph())
        context.plot(self.data[0], self.data[1], self.data[2], self.data[3])


root = tk.Tk()
app = AccelerometerApp(root)
root.geometry("600x400") 
root.mainloop()
