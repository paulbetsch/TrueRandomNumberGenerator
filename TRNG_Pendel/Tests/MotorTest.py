from KameraRaspberryPi import ObjectTracker


def motorTest():
     # Test überprüft ob Koordinaten des Pendels an unterster Stelle ist.
    global MOTOR_RUNNING 
    for i in range(3):
    # Aufruf der Methode NullPointerPendulum() und Speichern des Ergebnisses in der Variable "Coords"
     x = ObjectTracker.XCOORD_LIST[i]
     y = ObjectTracker.YCOORD_LIST[i]

    # Vergleich der neuen Variable "Coords" mit der vorherigen Variable "Coords"
     if y == yOld & x == xOld:
        print("Pendel schwingt nicht")
        MOTOR_RUNNING = False
     else:
        print("Pendel schwingt")
        MOTOR_RUNNING = True

    # Aktualisierung der vorherigen Variable "Coords"
     xOld = x
     yOld = y

    return MOTOR_RUNNING