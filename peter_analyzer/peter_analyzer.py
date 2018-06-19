
import logging
import tkinter as tk

class PeterAnalyzer(tk.Frame):
    __log : logging.Logger

    def __init__(self, master=None):
        self.__log = logging.getLogger("PeterAnalyzer")
        self.__log.setLevel(logging.DEBUG)

        fh = logging.FileHandler('peter_analyzer.log')
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.__log.addHandler(fh)
        self.__log.addHandler(ch)

        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        self.__log.info("hi there, everyone!")

if __name__=="__main__":
    root = tk.Tk()
    app = PeterAnalyzer(master=root)
    app.mainloop()