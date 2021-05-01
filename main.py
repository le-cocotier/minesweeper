import tkinter
from tkinter import messagebox
import random


class Menu:
    def __init__(self):
        self.difficulty = 0
        self.taille = []
        self.fen = tkinter.Tk()
        self.canvas = tkinter.Canvas(width=400, height=400)
        self.fond = tkinter.PhotoImage(file="menu.png")
        self.text_1 = tkinter.Label(self.fen, text="Entrez le le % de bombes")
        self.choice_1 = tkinter.Entry(self.fen, width=30)
        self.text_2 = tkinter.Label(self.fen, text="Entrez la taille de la grille (width, height)")
        self.choice_2 = tkinter.Entry(self.fen, width=30)

    def get_entry(self, event):
        decoupe = self.choice_2.get().split(',')
        self.taille = [int(decoupe[0]), int(decoupe[1])]
        self.difficulty = int(self.choice_1.get())
        self.fen.destroy()

    def affiche(self):
        self.canvas.grid(row=0, rowspan=4, column=0, columnspan=3)
        self.canvas.create_image(0, 0, anchor=tkinter.NW, image=self.fond)
        self.canvas.create_text(200, 40, text="Démineur", font=('Arial', 30, 'bold', 'roman'))
        self.canvas.create_text(200, 100, text="Entrez le pourcentage de bombes")
        self.choice_1.grid(row=1, column=1)
        self.canvas.create_text(200, 300, text="Entrez la taille de la grille (width, height)")
        self.choice_2.grid(row=3, column=1)

        self.fen.bind("<Return>", self.get_entry)

        self.fen.mainloop()


class Grille:

    def __init__(self):
        self.width = menu.taille[0]
        self.height = menu.taille[1]
        self.bomb = tkinter.PhotoImage(file="bombe_2.png")
        self.tableau = []
        self.nb_bomb = 0
        self.taille_case = 40

    def create_tab(self):
        for v in range(self.height):
            self.tableau.append([])
            for h in range(self.width):
                self.tableau[v].append(0)

    def draw_grid(self):
        for v in range(self.width + 1):
            canvas.create_line(self.taille_case * v, 0, self.taille_case * v, self.height * self.taille_case, fill="#000")
        for h in range(self.height + 1):
            canvas.create_line(0, self.taille_case * h, self.width * self.taille_case, self.taille_case * h, fill="#000")

    def place_bomb(self):
        self.nb_bomb = self.width * self.height * menu.difficulty // 100
        for i in range(self.nb_bomb):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.tableau[y][x] != 1:
                self.tableau[y][x] = 1
            else:
                i -= 1

    def revele_bomb(self):
        for colonne in range(len(self.tableau)):
            for ligne in range(len(self.tableau[colonne])):
                if self.tableau[colonne][ligne] == 1:
                    canvas.create_image(ligne * self.taille_case + 1, colonne * self.taille_case + 1, anchor=tkinter.NW, image=self.bomb)
        tkinter.messagebox.showinfo("game over", "Vous avez fait exploser une bombe!")
        fen.destroy()

    def set_up(self):
        self.create_tab()
        self.place_bomb()
        self.draw_grid()

    def win(self):
        limite = self.width * self.height - self.nb_bomb
        if len(player.deja_affiche) == limite:
            tkinter.messagebox.showinfo("Win", "Vous avez trouvé toutes les bombes")
            fen.destroy()


class Player:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.flag = tkinter.PhotoImage(file="flag.png")
        self.couleur = {0: '#D0D0D0', 1: 'blue', 2: 'green', 3: 'red', 4: 'purple', 5: 'brown', 6: 'orange', 7: 'yellow', 8: 'black'}
        self.case_a_tester = []
        self.case_visite = []
        self.deja_affiche = []

    def affiche_indice(self, nombre):
        canvas.create_rectangle(self.x * grille.taille_case + 1, self.y * grille.taille_case + 1, (self.x + 1) * grille.taille_case - 1, (self.y + 1) * grille.taille_case - 1, fill='#D0D0D0', outline='#D0D0D0')
        canvas.create_text((self.x + 0.5) * grille.taille_case, (self.y + 0.5) * grille.taille_case, text=str(nombre), fill=self.couleur[nombre], font=("Arial", 20))
        if self.is_visite(self.x, self.y, self.deja_affiche) == False:
            self.deja_affiche.append((self.y, self.x))

    def deminage(self, event):
        self.get_rect(event)
        if grille.tableau[self.y][self.x] == 0:
            self.test_large()
            self.test_list()
        else:
            grille.revele_bomb()
        grille.win()
        self.overflow()

    def drapeau(self, event):
        self.get_rect(event)
        drap = canvas.find_enclosed(self.x * grille.taille_case, self.y * grille.taille_case, (self.x + 1) * grille.taille_case , (self.y + 1) * grille.taille_case)
        if len(drap) == 0:
            canvas.create_image(self.x * grille.taille_case, self.y * grille.taille_case, anchor=tkinter.NW, image=self.flag)
        elif len(drap) == 1:
            canvas.delete(drap[-1])

    def get_rect(self, event):
        self.x = event.x // grille.taille_case
        self.y = event.y // grille.taille_case
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

    def is_visite(self, x, y, liste):
        similaire = 0
        for i in range(len(liste)):
            if liste[i] == (y, x):
                similaire += 1
        if similaire == 0:
            return False
        else:
            return True

    def limite(self, x, y):
        """revoir True si les coordonée sonr cohérentes"""
        if x >= grille.width:
            return False
        elif y >= grille.height:
            return False
        elif x < 0:
            return False
        elif y < 0:
            return False
        else:
            return True

    def overflow(self):
        couches = canvas.find_enclosed(self.y * grille.taille_case, self.x * grille.taille_case, (self.y + 1) * grille.taille_case, (self.x + 1) * grille.taille_case)
        if len(couches) > 2:
            while(len(couches) >= 2):
                canvas.delete(couches[-1])
                couches = canvas.find_enclosed(self.y * grille.taille_case, self.x * grille.taille_case, (self.y + 1) * grille.taille_case, (self.x + 1) * grille.taille_case)

    def test_adjacent(self):
        """retourne le nombre de bombe sur les cases aux alentours et ajoute les case sans bombes a une liste"""
        bomb_adjacentes = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if self.limite(self.x + j, self.y + i):
                    if grille.tableau[self.y + i][self.x + j] == 1:
                        bomb_adjacentes += 1
        return bomb_adjacentes

    def test_large(self):
        var = self.test_adjacent()
        if var == 0:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if self.is_visite(self.x + j, self.y + i, self.case_visite) == False:
                        if self.limite(self.x + j, self.y + i):
                            self.case_a_tester.append((self.y + i, self.x + j))
                            self.case_visite.append((self.y + i, self.x + j))
        self.affiche_indice(var)

    def test_list(self):
        for i in self.case_a_tester:
            self.y = self.case_a_tester[self.case_a_tester.index(i)][0]
            self.x = self.case_a_tester[self.case_a_tester.index(i)][1]
            self.test_large()


menu = Menu()
menu.affiche()

fen = tkinter.Tk()
fen.title = 'demineur'

grille = Grille()
player = Player()

canvas = tkinter.Canvas(fen, background='#616361', width=grille.width * grille.taille_case, height=grille. height * grille.taille_case)  # création de la zone de dessin
canvas.pack()

grille.set_up()

fen.bind("<Button-3>", player.drapeau)
fen.bind("<Button-1>", player.deminage)

fen.mainloop()
