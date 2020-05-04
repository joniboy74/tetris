#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame
import random

pygame.font.init()

# Variables importantes
largeur_f = 800
hauteur_f = 700
largeur_adj = 300  
hauteur_adj = 600  
taille_block = 30

maximum_x = (largeur_f - largeur_adj) // 2
maximum_y = hauteur_f - hauteur_adj


# Formes

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

formes = [S, Z, I, O, J, L, T]
couleur_piece = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]



class Piece(object):  
    def __init__(self, x, y, forme):
        self.x = x
        self.y = y
        self.forme = forme
        self.couleur = couleur_piece[formes.index(forme)]
        self.rotation = 0


def creer_grille(coordonees={}):  # *
    grille = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if (j, i) in coordonees:
                c = coordonees[(j,i)]
                grille[i][j] = c
    return grille


def convertir_format_piece(forme):
    positions = []
    format = forme.forme[forme.rotation % len(forme.forme)]

    for i, line in enumerate(format):
        rang = list(line)
        for j, column in enumerate(rang):
            if column == '0':
                positions.append((forme.x + j, forme.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def espace_valide(forme, grille):
    postion_accepte = [[(j, i) for j in range(10) if grille[i][j] == (0,0,0)] for i in range(20)]
    postion_accepte = [j for sub in postion_accepte for j in sub]

    formatted = convertir_format_piece(forme)

    for pos in formatted:
        if pos not in postion_accepte:
            if pos[1] > -1:
                return False
    return True


def game_over(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def app_forme():
    return Piece(5, 0, random.choice(formes))


def draw_text_middle(surface, text, size, couleur):
    police = pygame.font.SysFont("comicsans", size, bold=True)
    texte = police.render(text, 1, couleur)

    surface.blit(texte, (maximum_x + largeur_adj /2 - (texte.get_width()/2), maximum_y + hauteur_adj/2 - texte.get_height()/2))


def dessiner_grille(surface, grille):
    sx = maximum_x
    sy = maximum_y

    for i in range(len(grille)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*taille_block), (sx+largeur_adj, sy+ i*taille_block))
        for j in range(len(grille[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*taille_block, sy),(sx + j*taille_block, sy + hauteur_adj))


def supprimer_rang(grille, locked):

    inc = 0
    for i in range(len(grille)-1, -1, -1):
        rang = grille[i]
        if (0,0,0) not in rang:
            inc += 1
            ind = i
            for j in range(len(rang)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def dessiner_nouvelle_piece(forme, surface):
    police = pygame.font.SysFont('comicsans', 30)
    texte = police.render('Piece suivante', 1, (255,255,255))

    sx = maximum_x + largeur_adj + 50
    sy = maximum_y + hauteur_adj/2 - 100
    format = forme.forme[forme.rotation % len(forme.forme)]

    for i, line in enumerate(format):
        rang = list(line)
        for j, column in enumerate(rang):
            if column == '0':
                pygame.draw.rect(surface, forme.couleur, (sx + j*taille_block, sy + i*taille_block, taille_block, taille_block), 0)

    surface.blit(texte, (sx + 10, sy - 30))


def maj_score(score):
    score = record()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def record():
    with open('scores.txt', 'r') as f:
        lignes = f.readlines()
        score = lignes[0].strip()

    return score


def dessiner_fenetre(surface, grille, score=0, dernier_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    police = pygame.font.SysFont('comicsans', 60)
    texte = police.render('TETRIS ISN', 1, (255, 255, 255))

    surface.blit(texte, (maximum_x + largeur_adj / 2 - (texte.get_width() / 2), 30))

    police = pygame.font.SysFont('comicsans', 30)
    texte = police.render('Score: ' + str(score), 1, (255,255,255))

    sx = maximum_x + largeur_adj + 50
    sy = maximum_y + hauteur_adj/2 - 100

    surface.blit(texte, (sx + 20, sy + 160))
    
    texte = police.render('Record: ' + dernier_score, 1, (255,255,255))

    sx = maximum_x - 200
    sy = maximum_y + 200

    surface.blit(texte, (sx + 20, sy + 160))

    for i in range(len(grille)):
        for j in range(len(grille[i])):
            pygame.draw.rect(surface, grille[i][j], (maximum_x + j*taille_block, maximum_y + i*taille_block, taille_block, taille_block), 0)

    pygame.draw.rect(surface, (255, 0, 0), (maximum_x, maximum_y, largeur_adj, hauteur_adj), 5)

    dessiner_grille(surface, grille)


def main(win):  # *
    dernier_score = record()
    coordonees2 = {}
    grille = creer_grille(coordonees2)

    piece_change = False
    run = True
    piece_selection = app_forme()
    piece_suivante = app_forme()
    clock = pygame.time.Clock()
    chute_temps = 0
    chute_speed = 0.27
    level_temps = 0
    score = 0

    while run:
        grille = creer_grille(coordonees2)
        chute_temps += clock.get_rawtime()
        level_temps += clock.get_rawtime()
        clock.tick()

        if level_temps/1000 > 5:
            level_temps = 0
            if level_temps > 0.12:
                level_temps -= 0.005

        if chute_temps/1000 > chute_speed:
            chute_temps = 0
            piece_selection.y += 1
            if not(espace_valide(piece_selection, grille)) and piece_selection.y > 0:
                piece_selection.y -= 1
                piece_change = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece_selection.x -= 1
                    if not(espace_valide(piece_selection, grille)):
                        piece_selection.x += 1
                if event.key == pygame.K_RIGHT:
                    piece_selection.x += 1
                    if not(espace_valide(piece_selection, grille)):
                        piece_selection.x -= 1
                if event.key == pygame.K_DOWN:
                    piece_selection.y += 1
                    if not(espace_valide(piece_selection, grille)):
                        piece_selection.y -= 1
                if event.key == pygame.K_UP:
                    piece_selection.rotation += 1
                    if not(espace_valide(piece_selection, grille)):
                        piece_selection.rotation -= 1

        forme_pos = convertir_format_piece(piece_selection)

        for i in range(len(forme_pos)):
            x, y = forme_pos[i]
            if y > -1:
                grille[y][x] = piece_selection.couleur

        if piece_change:
            for pos in forme_pos:
                p = (pos[0], pos[1])
                coordonees2[p] = piece_selection.couleur
            piece_selection = piece_suivante
            piece_suivante = app_forme()
            piece_change = False
            score += supprimer_rang(grille, coordonees2) * 10

        dessiner_fenetre(win, grille, score, dernier_score)
        dessiner_nouvelle_piece(piece_suivante, win)
        pygame.display.update()

        if game_over(coordonees2):
            draw_text_middle(win, "GAME OVER", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            maj_score(score)


def main_menu(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((largeur_f, hauteur_f))
pygame.display.set_caption('Tetris')
main_menu(win)