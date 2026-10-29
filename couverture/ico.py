"""Assemble des PNG carrés en un fichier .ico (format PNG intégré, lu par tous les navigateurs).

Usage : python3 couverture/ico.py sortie.ico image16.png image32.png ...
"""
import struct
import sys


def taille_png(donnees):
    largeur, hauteur = struct.unpack(">II", donnees[16:24])
    return largeur, hauteur


def main(sortie, *entrees):
    images = [open(chemin, "rb").read() for chemin in entrees]
    entete = struct.pack("<HHH", 0, 1, len(images))
    repertoire = b""
    decalage = 6 + 16 * len(images)
    for donnees in images:
        largeur, hauteur = taille_png(donnees)
        repertoire += struct.pack(
            "<BBBBHHII", largeur % 256, hauteur % 256, 0, 0, 1, 32, len(donnees), decalage
        )
        decalage += len(donnees)
    with open(sortie, "wb") as fichier:
        fichier.write(entete + repertoire + b"".join(images))


if __name__ == "__main__":
    main(*sys.argv[1:])
