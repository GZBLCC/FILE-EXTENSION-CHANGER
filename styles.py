import tkinter as tk
from tkinter import ttk

def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', font=('Helvetica', 10), foreground='#333333')
    style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
    style.configure('TEntry', font=('Helvetica', 10), padding=5)
