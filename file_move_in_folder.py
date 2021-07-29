#!/usr/bin/python
import os
import shutil
import argparse


def parse_args() -> tuple:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--src", default="./files", help="Путь до файлов")
    ap.add_argument("-d", "--dst", default="/.folder", help="Путь до папок")
    return ap.parse_args()

args = parse_args()

for filename in os.listdir(args.src): #Папка с файлами
    name = filename.split('.')[0]
    for foldername in os.listdir(args.dst): #Папка с папкми =)       
        if name == foldername:
            shutil.move(f"{args.src}\{filename}", f"{args.dst}\{foldername}")
            print(f"Файл {filename} перенесен в папку {foldername} ")

            



    





    

