import os
import re

class File:
    def __init__(self,) -> None:
        self.lines      = []
        self.dict_lines = {}
        self.lines_no_t = []

    def read(self,path):

        try:
            
            # print(os.path.abspath(os.path.join("Compilador","source",path)))
            f = open(os.path.abspath(os.path.join(".","source",path)), "r")

            for line in f.readlines():
                self.lines.append(line)
                if "END" in line:
                    break

            # self.lines = f.readlines()
            f.close()
            # print(self.lines_no_t)
            
            for i in range(0,len(self.lines)):
                self.lines[i] = self.lines[i].rstrip()

        except FileNotFoundError:
            print(KeyError)
            print("Could not open/read file: ", path)
            

    @staticmethod
    def write_file(path,content):

        try:
            f = open(os.path.abspath(os.path.join(".","source",path)), "w")

            for line in content:
                f.write(line)
            
            f.close()
        except FileNotFoundError:
            print("Could not open/read file: ", path)

    def get_lines(self):
        return self.lines
    