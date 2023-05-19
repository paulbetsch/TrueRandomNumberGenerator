# TRNG Analyse

## About
This Folder contains a few Python Scripts which calculate the behavior of our Tri-Pendulum in an ideal enviroment without any confounding factors.
The behavior of the pendelum is being calculate by geometric derivation.

## Requirements
To run PendelErwartungswerteMitHäufigkeit.py you will need following additional Scripts:
- KoordinatenInBildKonvertierer.py

To run PendelErwartungswerte.py you won´t need any additional Scripts.

## Scripts
- PendelErwartungswerte.py: 
Calculates the movement of the provided Pendulum and shows all possible positions in a plot
- PendelErwartungswerteMitHäufigkeit.py: 
Calculates all possible Positions and tracks their frequencies with a dictionary. 
After the Calculation is completed it passes the dictionary of all possible positions with their frequencies to the
KoordinatenInBildKonvertierer.py Script
- KoordinatenInBildKonvertierer.py:
Turns a dictionary filled with a Tupel of (X-Cord, Y-Cord) as Key and the frequencies of this positions stored in a integer as value, into
a PNG Picture with a grey to white scale.

