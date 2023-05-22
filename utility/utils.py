"""
Module containing utility functions and classes.

This module provides various utility functions and classes that can be used in other parts of the application.

Functions:
    log_exec_time(f): A decorator that logs the execution time of a function and any exceptions that occur.
    EntryWithPlaceholder: A custom entry widget with a placeholder.
"""

from functools import wraps
import time
import logging
import tkinter as tk

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s', filemode='w')

class EntryWithPlaceholder(tk.Entry):
    """
    Custom entry widget with a placeholder.

    This class inherits from `tk.Entry` and adds a placeholder functionality to the entry widget. It displays a
    placeholder text when the widget is empty and loses focus, then removes the placeholder text when the widget gains
    focus or receives user input.

    :param master: The parent widget.
    :param placeholder: The placeholder text to display.
    :param color: The color of the placeholder text.
    """

    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        """
        Initialize the EntryWithPlaceholder widget.

        :param master: The parent widget.
        :param placeholder: The placeholder text to display when the widget is empty.
        :param color: The color of the placeholder text.
        """
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']


        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def log_exec_time(f):
    """
    A decorator for logging function execution time, calls information
    and exceptions info, if any occurs.

    :param f: Function to be decorated.
    :return: Decorated function.
    """
    @wraps(f)
    def time_count_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = f(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logging.info(f'fuction {f.__name__} executed in {total_time:.4} seconds')
            logging.info(f"Function {f.__name__} called with args: {args} and kwargs: {kwargs}")
            return result
        except Exception as e:
            logging.error(f'Function {f.__name__} raised exception {type(e).__name__}: {str(e)}')
            raise e
    return time_count_wrapper


