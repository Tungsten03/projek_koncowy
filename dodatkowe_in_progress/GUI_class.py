import tkinter as tk
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Przykład podmiany okien")

        # Tworzenie kontenera dla ramek
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}  # Słownik przechowujący ramki

        # Tworzenie różnych ramek
        frame1 = StartPage(self.container, self)
        frame2 = PageOne(self.container, self)
        frame3 = PageTwo(self.container, self)

        # Dodawanie ramek do słownika
        self.frames[StartPage] = frame1
        self.frames[PageOne] = frame2
        self.frames[PageTwo] = frame3

        # Wyświetlanie startowej ramki
        self.show_frame(StartPage)

    def show_frame(self, frame_class):
        # Wyświetlanie ramki o podanej klasie
        frame = self.frames[frame_class]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # etykieta
        label = ttk.Label(self, text="Wybierz stronę", font=("TkDefaultFont", 16))
        label.pack(pady=10)

        # przyciski
        button1 = ttk.Button(self, text="Strona 1",
                             command=lambda: controller.show_frame(PageOne))
        button2 = ttk.Button(self, text="Strona 2",
                             command=lambda: controller.show_frame(PageTwo))
        button1.pack(pady=5)
        button2.pack(pady=5)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Strona 1")
        label.pack(pady=10, padx=10)

        # Przycisk do powrotu do strony startowej
        button = tk.Button(self, text="Powrót do strony startowej", command=lambda: controller.show_frame(StartPage))
        button.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Strona 2")
        label.pack(pady=10, padx=10)

        # Przycisk do powrotu do strony startowej
        button = tk.Button(self, text="Powrót do strony startowej", command=lambda: controller.show_frame(StartPage))
        button.pack()


app = StartPage(Tk,ttk)
app.mainloop()