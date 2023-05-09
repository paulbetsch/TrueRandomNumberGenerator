# TRNG Live Image Capturing

## About
This repository includes code snippets, which we currently use on capturing live images from a RaspberryPi camera.

## Requirements
- These Scripts can only be run on the Raspberry Pi due to specific libraries

## Scripts
- __ObjectTracker__: startet Motor + Live Captureing --> schreibt Daten dann in jeweilige Files
    - Einstellungen:
        - RGB (l.21 + 22)
        - Mittelpunkt (l. 26 + l. 27)
        - Anzahl Max Bits --> Methoden aufruf (l. 397)
        - Intervall zwischen Motorstößen (l. 129)
        - Wie lange Motorstoß (l. 126 (erstschwung) und l. 130)
        - time.sleep zwischen konturen --> niedriger = schneller samplen (l.192)
        - Zeit Pause (b) (l. 197)
        - Gitter Breite (aktuell 2px) - (l.66) und schleife in (l.69) so anpassen das Range x Schleife = 300
    - Aktuelle Bit generierungs Methoden
        - rangeBits (Pauls Methode, Gitter mit 0 und 1)
        - Lsb von Winkel und Distanz
        - HexBits16 (Lukas Methode mit Halbkreis eingeteilt in 16 abteile (jeweils 1 Hex Ziffer)) --> einmal für oben, einmal für unten
        - HexBits32 gleich wie HexBits16 nur in 32 abteile --> landen alle jeweils auf Desktop
    - Andere output.csv - hält timestamp, x, y, abstand und winkel von allen Punkten