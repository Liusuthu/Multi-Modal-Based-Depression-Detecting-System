"""
File: config.py
Author: Elena Ryumina and Dmitry Ryumin
Description: Plotting statistical information.
License: MIT License
"""
import matplotlib.pyplot as plt
import numpy as np 

# Importing necessary components for the Gradio app
from config import DICT_EMO, COLORS


def statistics_plot(frames, probs):
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.subplots_adjust(left=0.07, bottom=0.14, right=0.98, top=0.8, wspace=0, hspace=0)
    # Установка параметров left, bottom, right, top, чтобы выделить место для легенды и названий осей
    probs = np.array(probs)
    for i in range(7):
        try:
            ax.plot(frames, probs[:, i], label=DICT_EMO[i], c=COLORS[i]) 
        except Exception:
            return None
            
    ax.legend(loc='upper center', bbox_to_anchor=(0.47, 1.2), ncol=7, fontsize=12) 
    ax.set_xlabel('Frames', fontsize=12)  # Добавляем подпись к оси X
    ax.set_ylabel('Probability', fontsize=12)  # Добавляем подпись к оси Y
    ax.grid(True)
    return plt
