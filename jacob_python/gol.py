# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:52:50 2023

@author: Fatihah
"""
from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import threading
import re
from tkinter import ttk
from abc import ABC
from time import sleep
import tkinter as tk
import datetime as d
import time
from time import sleep
from PIL import Image, ImageTk
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import datetime
from tkinter.simpledialog import askinteger



import mysql.connector



class Generation:
    def __init__(self, mydb):
        self.mc = mydb.cursor()

    def create(self, id_user, id_admin, gene1, gene_stable, nbre_tours):
        query = "INSERT INTO generation (id_user, id_admin, gene1, gene_stable, nbre_tours) VALUES (%s, %s, %s, %s, %s)"
        values = (id_user, id_admin, gene1, gene_stable, nbre_tours)
        self.mc.execute(query, values)
        self.mc.execute("COMMIT")

    def read(self, id_gene):
        query = "SELECT * FROM generation WHERE id_gene = %s"
        value = (id_gene,)
        self.mc.execute(query, value)
        result = self.mc.fetchone()
        return result

    def update(self, id_gene, id_user=None, id_admin=None, gene1=None, gene_stable=None, nbre_tours=None):
        query = "UPDATE generation SET "
        values = []
        if id_user:
            query += "id_user = %s, "
            values.append(id_user)
        if id_admin:
            query += "id_admin = %s, "
            values.append(id_admin)
        if gene1:
            query += "gene1 = %s, "
            values.append(gene1)
        if gene_stable:
            query += "gene_stable = %s, "
            values.append(gene_stable)
        if nbre_tours:
            query += "nbre_tours = %s, "
            values.append(nbre_tours)
        query = query[:-2] + " WHERE id_gene = %s"
        values.append(id_gene)
        self.mc.execute(query, tuple(values))
        self.mc.execute("COMMIT")

    def delete(self, id_gene):
        query = "DELETE FROM generation WHERE id_gene = %s"
        value = (id_gene,)
        self.mc.execute(query, value)
        self.mc.execute("COMMIT")


class Administrateur:
    def __init__(self, mydb):
        self.mc = mydb.cursor()

    def create(self, nom, passnumber):
        query = "INSERT INTO administrateur (nom, passnumber) VALUES (%s, %s)"
        values = (nom, passnumber)
        self.mc.execute(query, values)
        self.mc.execute("COMMIT")

    def read(self, id_admin):
        query = "SELECT * FROM administrateur WHERE id_admin = %s"
        value = (id_admin,)
        self.mc.execute(query, value)
        result = self.mc.fetchone()
        return result

    def update(self, id_admin, nom=None, passnumber=None):
        query = "UPDATE administrateur SET "
        values = []
        if nom:
            query += "nom = %s, "
            values.append(nom)
        if passnumber:
            query += "passnumber = %s, "
            values.append(passnumber)
        query = query[:-2] + " WHERE id_admin = %s"
        values.append(id_admin)
        self.mc.execute(query, tuple(values))
        self.mc.execute("COMMIT")

    def delete(self, id_admin):
        query = "DELETE FROM administrateur WHERE id_admin = %s"
        value = (id_admin,)
        self.mc.execute(query, value)
        self.mc.execute("COMMIT")


class Utilisateur:
    def __init__(self, mydb):
        self.mc = mydb.cursor()

    def create(self, id_admin, nom, passnumber, naiss, email, temps):
        query = "INSERT INTO utilisateur (id_admin, nom, passnumber, naiss, email, temps) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (id_admin, nom, passnumber, naiss, email, temps)
        self.mc.execute(query, values)
        self.mc.execute("COMMIT")

    def read(self, id_user):
        query = "SELECT * FROM utilisateur WHERE id_user = %s"
        value = (id_user,)
        self.mc.execute(query, value)
        result = self.mc.fetchone()
        return result
    def read1(self, name, passnumber):
        query = f"SELECT * FROM utilisateur WHERE nom = '{name}' and passnumber = '{passnumber}'"
        self.mc.execute(query)
        result = self.mc.fetchone()
        return result
    def updatetime(self, nom, passnumber, temps):
        self.mc.execute(f"UPDATE utilisateur SET (temps = '{str(temps)}') where nom = '{nom}' and passnumber = {passnumber}")
        self.mc.execute("COMMIT")

    def update(self, id_user, id_admin=None, nom=None, passnumber=None, naiss=None, email=None, temps=None):
        query = "UPDATE utilisateur SET "
        values = []
        if id_admin:
            query += "id_admin = %s, "
            values.append(id_admin)
        if nom:
            query += "nom = %s, "
            values.append(nom)
        if passnumber:
            query += "passnumber = %s, "
            values.append(passnumber)
        if naiss:
            query += "naiss = %s, "
            values.append(naiss)
        if email:
            query += "email = %s, "
            values.append(email)
        if temps:
            query += "temps = %s, "
            values.append(temps)
        query = query[:-2] + " WHERE id_user = %s"
        values.append(id_user)
        self.mc.execute(query, tuple(values))
        self.mc.execute("COMMIT")

    def delete(self, id_user):
        query = "DELETE FROM utilisateur WHERE id_user = %s"
        value = (id_user,)
        self.mc.execute(query, value)
        self.mc.execute("COMMIT")

mydb = mysql.connector.connect(host="localhost", user="root", password="1234", database="gol")
mc = mydb.cursor()
generation = Generation(mydb)
administrateur = Administrateur(mydb)
utilisateur = Utilisateur(mydb)
utilisateur = Utilisateur(mydb)

global utilisateurs, administrateurs, users
mc.execute("select nom, passnumber, naiss, temps from utilisateur") 
users = mc.fetchall()
utilisateurs = {}
now = d.datetime.now()
for i in users:
    utilisateurs[i[0]] = [i[1], i[3]]
mc.execute("select nom, passnumber from administrateur") 
a = mc.fetchall()
administrateurs = {}
for i in a:
    administrateurs[i[0]] = i[1]





        


class MultiPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
                       
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.border = tk.LabelFrame(self, bg ='white')
        self.border.pack(fill = "both", expand= "yes")
        global imagX
        imagx = Image.open("image.png")
        global imagex
        imagex = imagx.resize((1300, 600), Image.LANCZOS) # Redimensionner l'image 
        global photox
        photox = ImageTk.PhotoImage(imagex)
        global labelx
        labelx = tk.Label(self.border, image=photox)
        labelx.pack(side="top", anchor="n")
        bt3 = tk.Button(self.border, text="Continuer", width=15, fg = "black",command= lambda: controller.show_frame("PageOne"))
        bt3.pack()

class JeuDeLaVie(tk.Frame):
    def __init__(self, master=None, width=1200, height=700, cell_size=40):
        super().__init__(master)
        self.width = width // cell_size
        self.height = height // cell_size
        self.cell_size = cell_size
        self.initiate_board()

        self.canvas = tk.Canvas(self, width=self.width*cell_size, height=self.height*cell_size, bg='white')
        self.canvas.bind('<Button-1>', self.cell_toggle)
        self.canvas.pack()

        self.start_button = tk.Button(self, text='Commencer le jeu', command=self.start_game)
        self.start_button.pack()
        self.pack()
        master.mainloop()

    def initiate_board(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def draw_cell(self, x, y, state):
        color = 'black' if state else 'white'
        self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, (x+1)*self.cell_size, (y+1)*self.cell_size, fill=color, outline="")

    def cell_toggle(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.board[y][x] = 1 - self.board[y][x]
        self.draw_cell(x, y, self.board[y][x])

    def next_gen(self):
        new_board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                neighbours = sum(self.board[(y+i)%self.height][(x+j)%self.width] for i in [-1, 0, 1] for j in [-1, 0, 1]) - self.board[y][x]
                new_board[y][x] = (neighbours == 3) or (neighbours == 2 and self.board[y][x])
                self.draw_cell(x, y, new_board[y][x])
        self.board = new_board
    def start_game(self):
        for _ in range(100):
            self.master.update()
            self.next_gen()
            sleep(0.1)

        
        
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Le jeu de la vie, aussi connu sous le nom de Life, est un automate cellulaire créé par John Horton Conway en 1970. \nIl s'agit d'un jeu à zéro joueur, ce qui signifie que son évolution est déterminée par son état initial et ne nécessite aucune intervention de la part de l'utilisateur. \nLe jeu se déroule sur une grille bidimensionnelle, où chaque case peut être soit vivante, soit morte. \nÀ chaque étape du jeu, l'état de chaque case est mis à jour en fonction de l'état de ses huit voisines. \nLes règles du jeu sont simples, mais peuvent donner lieu à des motifs complexes et fascinants.\nSi vous souhaitez tester le jeu de la vie, vous avez le choix entre trois types d'implémentations :",  width=1300, font=("Arial Bold", 15), bg="white")
        label.pack(side=tk.TOP, anchor=tk.CENTER, pady=30)
        button1 = tk.Button(self, text="démarrage d'une simulation aléatoire",width=35, command=lambda: controller.show_frame("PageTwo"),bg="white")
        button1.pack(pady=20)
        button2 = tk.Button(self, text="choisir la premiere génération",width=35, command=lambda: controller.show_frame(" PageFour1"))
        button2.pack(pady=20)
        button3 = tk.Button(self, text="choisir un prototype de première génération",width=35, command=lambda: controller.show_frame("PageThree"))
        button3.pack(pady=20)
        button4 = tk.Button(self, text="back",width=25, command=lambda: controller.show_frame("StartPage"))
        button4.place(x =0, y = 650)
        
class InitialStateDialog(tk.Toplevel):
    def __init__(self, parent, width, height):
        tk.Toplevel.__init__(self, parent)
        self.title("Sélection de l'état initial")
        self.parent = parent
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.initiate_board()

        self.canvas = tk.Canvas(self, width=self.width*30, height=self.height*30, bg='white')
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.cell_toggle)

        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.BOTTOM)

        validate_button = tk.Button(button_frame, text="Valider", command=self.validate)
        validate_button.pack(side=tk.LEFT)

        cancel_button = tk.Button(button_frame, text="Annuler", command=self.cancel)
        cancel_button.pack(side=tk.RIGHT)

    def initiate_board(self):
        # Initialisation de la grille
        self.board[4][6] = 1
        self.board[4][7] = 1
        self.board[5][6] = 1
        self.board[5][7] = 1
        self.board[2][8] = 1
        self.board[3][8] = 1
        self.board[4][8] = 1
        self.board[5][8] = 1
        self.board[6][8] = 1
        self.board[7][8] = 1
        self.board[8][8] = 1
        self.board[9][8] = 1
        self.board[10][8] = 1

    def draw_cell(self, x, y, state):
        # Dessin de la cellule
        color = 'black' if state else 'white'
        self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill=color, outline="")

    def cell_toggle(self, event):
        # Inversion de l'état de la cellule
        x, y = event.x // 30, event.y // 30
        self.board[y][x] = 1 - self.board[y][x]
        self.draw_cell(x, y, self.board[y][x])

    def validate(self):
        # Validation de l'état initial
        self.parent.set_initial_state(self.board)
        self.destroy()

    def cancel(self):
        # Annulation de la sélection
        self.destroy()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.master = tk.LabelFrame(self, bg ='blue', width=1200, height=630)
        self.master.pack()

        self.canvas = tk.Canvas(self.master, width=1200, height=630, bg='white')
        self.canvas.pack()

        self.width = 30
        self.height = 15
        self.cell_size = 30
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.initiate_board()

        self.canvas.bind('<Button-1>', self.cell_toggle)

        start_button = tk.Button(self.master, text='Commencer le jeu', command=self.start_game)
        start_button.pack()

        return_button = tk.Button(self.master, text="Retour à la page d'accueil", width=35, command=lambda: controller.show_frame("PageOne"))
        return_button.pack(side="bottom")

    def initiate_board(self):
        # Initialisation de la grille
        self.board[4][6] = 1
        self.board[4][7] = 1
        self.board[5][6] = 1
        self.board[5][7] = 1
        self.board[2][8] = 1
        self.board[3][8] = 1
        self.board[4][8] = 1
        self.board[5][8] = 1
        self.board[6][8] = 1
        self.board[7][8] = 1
        self.board[8][8] = 1
        self.board[9][8] = 1
        self.board[10][8] = 1

    def draw_cell(self, x, y, state):
        # Dessin de la cellule
        color = 'black' if state else 'white'
        self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size, (x+1)*self.cell_size, (y+1)*self.cell_size, fill=color, outline="")

    def cell_toggle(self, event):
        # Inversion de l'état de la cellule
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.board[y][x] = 1 - self.board[y][x]
        self.draw_cell(x, y, self.board[y][x])

    def set_initial_state(self, board):
        # Réglage de l'état initial de la grille
        self.board = board
        for y in range(self.height):
            for x in range(self.width):
                self.draw_cell(x, y, self.board[y][x])

    def start_game(self):
        # Lancement du jeu
        initial_state_dialog = InitialStateDialog(self.master, self.width, self.height)
        self.wait_window(initial_state_dialog)
        

class PageFour1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.master = tk.LabelFrame(self, bg ='blue', width=1200, height=630)
        self.master.pack()
        button = tk.Button(self, text="Retour à la page d'accueil", width=35, command=lambda: controller.show_frame("PageOne"))
        button.place(x=0, y=650)
        # Crée un nouveau Frame pour le bouton de sélection de la première génération
        generation_button_frame = tk.Frame(self.master)
        generation_button_frame.pack()
        
        # Crée le bouton dans le nouveau Frame
        generation_button = tk.Button(generation_button_frame, text="Sélectionner la première génération", width=35, command=self.show_generation_window)
        generation_button.pack()

    def show_generation_window(self):
        generation_window = tk.Toplevel(self)
        generation_window.title("Sélection de la première génération")
        generation_frame = JeuDeLaVie(generation_window)
        generation_frame.pack()

        
class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="HORLOGE")
        label.pack(side="top", fill="x", pady=10)
        self.controller = controller
        self.master = tk.LabelFrame(self, bg ='blue', width=1200, height=630)
        self.master.pack()
        button = tk.Button(self, text="Back",width=35, command=lambda: controller.show_frame("PageThree"))
        button.place(x =0, y = 675)
        
        

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="autre")
        label.pack(side="top", fill="x", pady=10)
        self.controller = controller
        self.master = tk.LabelFrame(self, bg ='blue', width=1200, height=630)
        self.master.pack()
        button = tk.Button(self, text="Back",width=35, command=lambda: controller.show_frame("PageThree"))
        button.place(x =0, y = 675)
        
    
        

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.master = tk.LabelFrame(self, bg ='blue', width=1200, height=630)
        self.master.pack()
        button = tk.Button(self, text="Retour à la page d'accueil",width=35, command=lambda: controller.show_frame("PageOne"))
        button.place(x =0, y = 650)
        button1 = tk.Button(self, text="horloge", command=lambda: controller.show_frame("PageFour"))
        button1.place(x =1350, y = 345)
        button2 = tk.Button(self, text="autre", command=lambda: controller.show_frame("PageFive"))
        button2.place(x =1360, y = 380)
        self.init_ui()
        self.running = False

    def init_ui(self):
        self.starting_generations = ["Random", "Glider", "Lightweight spaceship", "Pulsar", "Glider Gun", "Glider Pusher",
                                     "Spaceship", "SpaceRake", "Caterpilla", "QueenBeeShuttle"]
        self.rows = 63
        self.cols = 120
        self.cell_size = 10
        self.cell_color = "black"

        self.canvas = tk.Canvas(self.master, width=1200, height=630, bg="white")
        self.canvas.pack()

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.place(x =300, y = 650)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop)
        self.stop_button.place(x =600, y = 650)

        self.option_menu = ttk.Combobox(self, values=self.starting_generations)
        self.option_menu.set("Random")
        self.option_menu.place(x =900, y = 650)

        self.board = [[0]*self.cols for _ in range(self.rows)]

    def start(self):
        if not self.running:
            self.running = True
            self.fill_starting_board()
            self.draw()
            self.run()

    def stop(self):
        self.running = False

    def fill_starting_board(self):
        gen_name = self.option_menu.get()

        if gen_name == "Random":
            from random import randint
            for i in range(self.rows):
                for j in range(self.cols):
                    self.board[i][j] = randint(0, 1)
        elif gen_name == "Glider":
            self.board[2][1] = 1
            self.board[2][2] = 1
            self.board[2][3] = 1
            self.board[1][3] = 1
            self.board[0][2] = 1
        elif gen_name == "Lightweight spaceship":
            self.board[4][2] = self.board[4][5] = 1
            self.board[3][1] = self.board[3][5] = 1
            self.board[2][5] = 1
            self.board[1][1] = self.board[1][4] = 1
        elif gen_name == "Pulsar":
            points = [(2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12), (4, 2), (5, 2), (6, 2), (10, 2), (11, 2), (12, 2)]
            for point in points:
                x, y = point
                for _ in range(2):
                    self.board[x][y] = 1
                    self.board[y][x] = 1
                    x += 4
        elif gen_name == "Glider Gun":
            coords = [(1, 5), (1, 6), (2, 5), (2, 6), (11, 5), (11, 6), (11, 7), (12, 4), (12, 8), (13, 3), (14, 3), (13, 9), (14, 9), (15, 6), (16, 4), (16, 8), (17, 5), (17, 6), (17, 7), (18, 6), (21, 3), (21, 4), (21, 5), (22, 3), (22, 4), (22, 5), (23, 2), (23, 6), (25, 1), (25, 2), (25, 6), (25, 7), (35, 3), (35, 4), (36, 3), (36, 4)] 
            for x, y in coords:
                self.board[x][y] = 1
        elif gen_name == "Glider Pusher":
            coords =  [(1, 2), (1, 3), (2, 1), (2, 3), (3, 3), (4, 6), (4, 7), (5, 5), (5, 8), (6, 5), (6, 8), (7, 5), (7, 8), (9, 4), (9, 5), (9, 6), (10, 4), (10, 5), (10, 6), (11, 3), (11, 7), (13, 2), (13, 3), (13, 7), (13, 8), (17, 4), (17, 5), (17, 6), (18, 4), (18, 5), (18, 6), (19, 3), (19, 7), (21, 2), (21, 3), (21, 7), (21, 8), (25, 5), (26, 3), (26, 5), (27, 4), (27, 6), (28, 5)]
            for x, y in coords:
                self.board[x][y] = 1
        elif gen_name == "Spaceship":
            coords = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
            for x, y in coords:
                self.board[x][y] = 1
        elif gen_name == "SpaceRake":
            coords = [(0, 5), (1, 5), (1, 6), (2, 6), (3, 7), (3, 8), (3, 9), (4, 8), (5, 6), (6, 6), (6, 7), (9, 7), (10, 7), (10, 8), (11, 10), (11, 11), (12, 9), (12, 10), (13, 9), (14, 8), (15, 8), (15, 9), (16, 6), (16, 7), (17, 6), (17, 7), (18, 6), (19, 7)]
            for x, y in coords:
                self.board[x][y] = 1
        elif gen_name == "Caterpilla":
            self.rows = 126
            self.cols = 240
            self.cell_size = 5
            self.board = [[0]*self.cols for _ in range(self.rows)]
            coords = [(10, 5), (11, 5), (11, 4), (10, 9), (11, 9), (11, 10), (13, 3), (14, 3), (15, 4), (17, 4), (17, 3), (18, 3), (19, 4), (20, 5), (21, 5), (22, 6), (23, 6), (24, 5), (26, 5), (27, 5), (28, 6), (29, 6), (30, 5), (31, 5), (32, 6), (33, 6), (34, 5), (35, 4), (36, 4), (37, 3), (38, 3), (39, 4), (41, 4), (42, 3), (42, 19), (43, 19), (43, 18), (43, 3), (45, 4), (46, 4), (47, 5), (47, 6), (48, 6), (49, 5), (51, 5), (52, 6), (52, 5), (52, 7), (53, 7), (53, 6), (53, 7), (54, 8), (55, 8), (56, 8), (57, 8), (58, 6), (59, 6), (60, 5), (60, 20), (60, 21), (61, 5), (61, 6), (62, 6), (64, 5), (65, 5), (66, 5), (67, 5), (68, 5), (70, 5), (72, 6), (73, 6), (74, 5), (75, 5), (76, 6), (78, 6), (79, 4), (80, 4), (80, 3), (81, 3), (81, 4), (82, 5), (84, 5), (84, 6), (84, 7)]
            for x, y in coords:
                self.board[x][y] = 1
        elif gen_name == "QueenBeeShuttle":
            coords = [(2, 6), (3, 4), (3, 6), (4, 2), (4, 3), (4, 6), (5, 1), (5, 5), (6, 5), (7, 5), (8, 6), (9, 6), (11, 6), (12, 4), (12, 6), (13, 2), (13, 3), (13, 6), (14, 1), (14, 5), (15, 5), (16, 5), (17, 6), (18, 6), (20, 6), (21, 4), (21, 6), (22, 2), (22, 3), (22, 6), (23, 1), (23, 5), (24, 5), (25, 5), (26, 6)]
            for x, y in coords:
                self.board[x][y] = 1
        
        

    def draw(self):
        self.canvas.delete("all")

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j]:
                    self.canvas.create_rectangle(j*self.cell_size, i*self.cell_size, (j+1)*self.cell_size,
                                                 (i+1)*self.cell_size, fill=self.cell_color, width=0)

    def get_neighbors(self, r, c):
        coords = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]
        return [self.board[i][j] for i, j in coords if 0 <= i < self.rows and 0 <= j < self.cols]

    def run(self):
        if self.running:
            new_board = [[0]*self.cols for _ in range(self.rows)]

            for i in range(self.rows):
                for j in range(self.cols):
                    neighbors = self.get_neighbors(i, j)
                    if self.board[i][j] and 2 <= sum(neighbors) <= 3:
                        new_board[i][j] = 1
                    elif not self.board[i][j] and sum(neighbors) == 3:
                        new_board[i][j] = 1

            self.board = new_board
            self.draw()
            self.master.after(100, self.run)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.master = tk.LabelFrame(self, bg ='blue', width=1200, height=630)
        self.master.pack()
        button = tk.Button(self, text="Retour à la page d'accueil",width=35, command=lambda: controller.show_frame("PageOne"))
        button.place(x =0, y = 650)
        self.grid()

        self.cell_size = 10
        self.rows = 63
        self.cols = 120

        self.canvas = tk.Canvas(self.master, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="#ffffff")
        self.canvas.grid(row=0, columnspan=6)

        self.start_button = tk.Button(self, text="Commencer", command=self.start)
        self.start_button.place(x =300, y = 650)

        self.stop_button = tk.Button(self, text="Arrêter", command=self.stop, state=tk.DISABLED)
        self.stop_button.place(x =600, y = 650)

        self.reset_button = tk.Button(self, text="Réinitialiser", command=self.reset, state=tk.DISABLED)
        self.reset_button.place(x =900, y = 650)

        # Initialiser l'état du jeu
        self.current_gen = self.random_gen()
        self.draw()
    def draw(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                if self.current_gen[i][j] == 1:
                    self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                                  j * self.cell_size + self.cell_size,
                                                  i * self.cell_size + self.cell_size, fill="black")

    def start(self):
        self.start_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.NORMAL
        self.reset_button["state"] = tk.NORMAL
        self.update_gen()

    def stop(self):
        self.start_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.DISABLED
        self.reset_button["state"] = tk.NORMAL
        self.after_cancel(self.update_id)

    def reset(self):
        self.current_gen = self.random_gen()
        self.draw()

    def random_gen(self):
        return [[random.randint(0, 1) for j in range(self.cols)] for i in range(self.rows)]

    def update_gen(self):
        new_gen = [[0 for j in range(self.cols)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                neighbors_sum = sum(self.current_gen[i2 % self.rows][j2 % self.cols]
                                    for i2 in range(i-1, i+2)
                                    for j2 in range(j-1, j+2)
                                    if i2 != i or j2 != j)
                if self.current_gen[i][j] == 1 and 2 <= neighbors_sum <= 3:
                    new_gen[i][j] = 1
                elif self.current_gen[i][j] == 0 and neighbors_sum == 3:
                    new_gen[i][j] = 1

        self.current_gen = new_gen
        self.draw()
        self.update_id = self.after(100, self.update_gen)
        

global app
def start_app():
    root.destroy()
    app = MultiPage()
    app.title("Game Of Life")
    app.configure(bg='white')
    app.minsize(width=1400, height=700)
    app.maxsize(width=1400, height=700)
    app.mainloop()
    return app

def decrement_time(username, password, app):
    global utilisateurs, administrateurs
    if username in utilisateurs.keys():
        temps_rest = utilisateurs[username][1].total_seconds()
        temps_restant = datetime.timedelta(seconds=temps_rest)
        maintenant = datetime.datetime.now()
        temps_restant1 = maintenant + temps_restant
        temps_formate = temps_restant1.strftime('%H:%M:%S')
        while True:
            time.sleep(1) 
            if temps_rest <= 0:
                messagebox.showwarning("Temps écoulé", "Votre temps est écoulé, veuillez contacter un administrateur.")
                app.destroy()
                break
            else:
                temps_formate = temps_restant1.strftime('%H:%M:%S')
                mc.execute(f"update utilisateur set temps = '{temps_formate}' where nom = '{username}' and passnumber = {password}")
                mydb.commit()
                mc.execute(f"select temps from utilisateur where nom = '{username}' and passnumber = {password}")
                a = mc.fetchone()[0]
                temps_rest = a.total_seconds()
                temps_restant = datetime.timedelta(seconds=temps_rest)
                maintenant = datetime.datetime.now()
                temps_restant1 = maintenant + temps_restant
                temps_formate = temps_restant1.strftime('%H:%M:%S')
                

def check_credentials():
    global username, password
    username = username_entry.get()
    password = password_entry.get()
    global user1
    user1 = utilisateur.read1(username, password)
    if username in utilisateurs.keys() and utilisateurs[username][0] == int(password) : 
        messagebox.showinfo("Succès", "Authentification réussie!")
        app_thread = threading.Thread(target=start_app)
        app_thread.start()
        decrement_thread = threading.Thread(target=decrement_time, args=(username, password, start_app())) 
    elif username in administrateurs.keys() and administrateurs[username] == int(password):
        root.destroy()
        app = MultiPage()
        app.title("Game Of Life")
        app.configure(bg='white')
        app.minsize(width=1400, height=700)
        app.maxsize(width=1400, height=700)
        app.mainloop()
    else:
        messagebox.showerror("Erreur", "Utilisateur non trouvé!")
    if (username in administrateurs.keys() and administrateurs[username] == int(password)):
        # Création de la fenêtre
        root2 = tk.Tk()
        JeuDeLaVie(root2)
        root1 = tk.Tk()
        root1.title("Administrateur")
        root1.geometry("500x700")
        root1.configure(bg="black")
        
        # Fonction pour ajouter un administrateur
        def add_admin():
            nom = nom_entry.get()
            passnumber = passnumber_entry.get()
            cursor = mydb.cursor()
            sql = "INSERT INTO administrateur (nom, passnumber) VALUES (%s, %s)"
            val = (nom, passnumber)
            cursor.execute(sql, val)
            mydb.commit()
            status_label.config(text="Administrateur ajouté avec succès")
        
        # Fonction pour supprimer un utilisateur
        def delete_user():
            id_user = id_user_entry.get()
            cursor = mydb.cursor()
            sql = "DELETE FROM utilisateur WHERE id_user = %s"
            val = (id_user,)
            cursor.execute(sql, val)
            mydb.commit()
            status_label.config(text="Utilisateur supprimé avec succès")
        
        # Fonction pour modifier le temps d'un utilisateur
        def update_user():
            id_user = id_user_entry.get()
            temps = temps_entry.get()
            cursor = mydb.cursor()
            sql = "UPDATE utilisateur SET temps = %s WHERE id_user = %s"
            val = (temps, id_user)
            cursor.execute(sql, val)
            mydb.commit()
            status_label.config(text="Temps utilisateur modifié avec succès")
        
        # Éléments d'interface utilisateur
        title_label = tk.Label(root1, text="Gestion des utilisateurs et des administrateurs", font=("Arial", 16), fg="green", bg="black")
        title_label.pack(pady=10)
        
        add_admin_label = tk.Label(root1, text="Ajouter un administrateur", font=("Arial", 12), fg="green", bg="black")
        add_admin_label.pack(pady=10)
        
        nom_label = tk.Label(root1, text="Nom:", font=("Arial", 12), fg="green", bg="black")
        nom_label.pack()
        
        nom_entry = tk.Entry(root1, width=30)
        nom_entry.pack()
        
        passnumber_label = tk.Label(root1, text="Passnumber:", font=("Arial", 12), fg="green", bg="black")
        passnumber_label.pack()
        
        passnumber_entry = tk.Entry(root1, width=30)
        passnumber_entry.pack()
        
        add_admin_button = tk.Button(root1, text="Ajouter", font=("Arial", 12), fg="green", bg="black", command=add_admin)
        add_admin_button.pack(pady=10)
        
        delete_user_label = tk.Label(root1, text="Supprimer un utilisateur", font=("Arial", 12), fg="green", bg="black")
        delete_user_label.pack(pady=10)
        
        id_user_label = tk.Label(root1, text="ID utilisateur:", font=("Arial", 12), fg="green", bg="black")
        id_user_label.pack()
        
        id_user_entry = tk.Entry(root1, width=30)
        id_user_entry.pack()
        
        delete_user_button = tk.Button(root1, text="Supprimer", font=("Arial", 12), fg="green", bg="black", command=delete_user)
        delete_user_button.pack(pady=10)
        
        update_user_label = tk.Label(root1, text="Modifier le temps d'un utilisateur", font=("Arial", 12), fg="green", bg="black")
        update_user_label.pack(pady=10)
        
        id_user_label = tk.Label(root1, text="ID utilisateur:", font=("Arial", 12), fg="green", bg="black")
        id_user_label.pack()
        
        id_user_entry = tk.Entry(root1, width=30)
        id_user_entry.pack()
        
        temps_label = tk.Label(root1, text="Temps:", font=("Arial", 12), fg="green", bg="black")
        temps_label.pack()
        
        temps_entry = tk.Entry(root1, width=30)
        temps_entry.pack()
        
        update_user_button = tk.Button(root1, text="Modifier", font=("Arial", 12), fg="green", bg="black", command=update_user)
        update_user_button.pack(pady=10)
        
        status_label = tk.Label(root1, text="", font=("Arial", 12), fg="green", bg="black")
        status_label.pack(pady=10)
        
        root1.mainloop()
def show_register_window():
    register_window = tk.Toplevel(root)  
    register_window.title('Fenêtre d\'inscription')
    register_window.configure(bg = 'white',padx=150, pady=150)
    register_window.geometry('900x900')
    register_window.resizable(0,0)
    label_name = tk.Label(register_window, text='Nom:', font=("Arial", 14), bg = 'white')
    label_name.place(x=190, y=40)
    entry_name = tk.Entry(register_window,width=30)
    entry_name.place(x=300, y=43)
    label_code = tk.Label(register_window, text='passnumber:', font=("Arial", 14), bg = 'white')
    label_code.place(x=190, y=109)
    entry_code = tk.Entry(register_window,width=30)
    entry_code.place(x=300, y=112)
    label_adresse = tk.Label(register_window, text='adressemail:', font=("Arial", 14), bg = 'white')
    label_adresse.place(x=190, y=178)
    entry_adresse = tk.Entry(register_window,width=30)
    entry_adresse.place(x=300, y=181)
    label_naissance = tk.Label(register_window, text='naissance:', font=("Arial", 14), bg = 'white')
    label_naissance.place(x=190, y=250)
    entry_naissance = tk.Entry(register_window,width=30)
    entry_naissance.place(x=300, y=270)
    def validation(objet, patern):
        match = re.match(patern, objet)
        if match:
            return True
        return False
    def save():
        name = entry_name.get()
        fname = entry_code.get()
        adresse = entry_adresse.get()
        naissance = entry_naissance
        if validation(fname, "\d{4}") and validation(naissance, "\d{4}-\d{2}-\d{2}") and validation(adresse, "\w{1,}@\w{1,}.\w{1,}") and(len(entry_name.get()) != 0 and len(entry_code.get()) != 0 and len(entry_adresse.get()) != 0 ):
            register_window.destroy()
            utilisateur.create(0, name, fname, naissance, adresse, "00:00:00")
            messagebox.showinfo("Succès", "Inscription réussie!")
        else:
            messagebox.showerror("Erreur", "Une erreur est survenu. Cela peut etre dù au fait que: \n   -Un ou plusieurs champs n'ont pas été renseignés \n   -Un utilisateur a été détecté \n   -Un champ ne corespond pas au format demandé. \nVeuillez vous referer à la developpeuse pour plus de details.")
            register_window.destroy()
    button_save = tk.Button(register_window, text='Enregistrer', command=save,width=15)
    button_save.pack(side=tk.BOTTOM)
root = tk.Tk()
root.title("Connexion")
root.configure(bg='white', padx=100, pady=150)
root.minsize(width=900, height=600)
root.maxsize(width=900, height=600)
l1 = tk.Label(root, text = "Nom:", font=("Arial", 14), bg = 'white')
l1.place(x=190, y=40)
username_entry = tk.Entry(root,width=30)
username_entry.place(x=300, y=43)

l2 = tk.Label(root, text = "Mot de passe:", font=("Arial", 14), bg = 'white')
l2.place(x=190, y=109)
password_entry = tk.Entry(root,width=30, show="*")
password_entry.place(x=300, y=112)

submit_button = tk.Button(root, text="Connexion", width=15, fg = "black", command=check_credentials)
submit_button.place(x=190, y=200)
register_button = tk.Button(root, text="S'inscrire", width=15, fg = "black", command=show_register_window)
register_button.place(x=390, y=200)
root.mainloop()
