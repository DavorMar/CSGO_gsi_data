from tkinter import *
from tkinter import messagebox
import tkinter.filedialog
from shutil import copy2, rmtree
import json
import os
import pandas
import multiprocessing
from GSI import server
import time
from data_process import DataProcessor
"""
The simplest UI at the moment, just to create the basic options needed to further develop other features. Wanted 
to do it right away, so I dont have to change too much or anything in other classes later on
"""

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title = "CSGO statistics"
        self.root.minsize(400, 300)
        self.root.maxsize(300, 300)
        self.start_frame = LabelFrame(self.root, text="Start a new project or load an existing one?")
        self.button_new_project = Button(self.start_frame, text="New project", command=self.new_project)
        self.button_load_project = Button(self.start_frame, text="Load project", command=self.select_folder)
        self.start_frame.place(relx=.5, rely=.5, anchor=CENTER)
        self.button_new_project.pack()
        self.button_load_project.pack()

    def new_project(self):
        self.start_frame.destroy()
        self.new_project_frame = LabelFrame(self.root, text="New project")
        self.new_project_frame.grid(row=1, column=0, rowspan=2, sticky=NSEW)
        self.project_name_field = Entry(self.new_project_frame, width=15)
        Label(self.new_project_frame, text="Project name:").grid(row=0, column=0)
        self.project_name_field.grid(row=0, column=1)
        save_project_button = Button(self.new_project_frame, text="Save project",
                                     command=self.save_project)
        save_project_button.grid(row=2, column=1)

    def save_project(self):
        main_folder = "Projects"
        project_name = self.project_name_field.get()
        os.mkdir(fr"{main_folder}\{project_name}")
        self.new_project_frame.destroy()
        self.loaded_project(project_name)


    def select_folder(self):
        self.directory = ""
        foldername = tkinter.filedialog.askdirectory(initialdir=r"projects", title="Select a folder")
        self.directory = foldername.split("/")[-1]
        self.start_frame.destroy()
        self.loaded_project(self.directory)

    def loaded_project(self,project_name):
        self.start_frame.destroy()
        self.project_name = project_name
        self.load_project_frame = LabelFrame(self.root, text=f"Project {project_name}")
        self.load_project_frame.grid(row=1, column=0, rowspan=2, sticky=NSEW)
        scan_button = Button(self.load_project_frame, text="Start scan",
                                     command=self.start_scan)
        scan_button.grid(row=0, column=1)


    def start_scan(self):


        data_fetching_process = multiprocessing.Process(target=fetch_data, args=(self.project_name,))
        data_fetching_process.start()


def fetch_data(project_name):
    gsi_server = server.GSIServer(("localhost", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    gsi_server.start_server()

    data_processor = DataProcessor(project_name)
    while True:
        data = gsi_server.get_data()
        if data.game_state:
            print(len(data.payload))
            data_processor.process_data(data)
            print(data_processor.name, data.provider_data.data)
            time.sleep(1)
            # print(data.all_players_data.player_0["name"])
            # print(data.all_players_data.player_5["name"])
        else:
            print("Game has not started yet")
            time.sleep(2)



if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()