import os
import pyautogui
import win32gui
import easyocr
import cv2
import numpy as np
import time


def capture_dofus_window():
    """Capture la fenêtre contenant le mot "Dofus" et la sauvegarde en tant qu'image."""
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            time.sleep(0.5)
            if "Beta" in window_title:
                print(f"Fenêtre trouvée : {window_title}")
                win32gui.SetForegroundWindow(hwnd)
                x, y, x1, y1 = win32gui.GetWindowRect(hwnd)
                screenshot = pyautogui.screenshot(region=(x, y, x1 - x, y1 - y))
                
                # Supprimer l'ancienne capture d'écran si elle existe
                if os.path.exists("dofus_screenshot.png"):
                    os.remove("dofus_screenshot.png")
                    print("Ancienne capture d'écran supprimée.")

                screenshot.save("dofus_screenshot.png")
                print("Capture d'écran sauvegardée sous dofus_screenshot.png")
                return

    win32gui.EnumWindows(winEnumHandler, None)

def detect_text_from_screenshot():
    """Détecte le texte dans la capture d'écran "dofus_screenshot.png"."""
    reader = easyocr.Reader(['fr'])
    result = reader.readtext('dofus_screenshot.png')

    for (bbox, text, prob) in result:
        print(f"Texte détecté : {text} (Probabilité : {prob:.2f})")
        if "Caractéristique" in text:
            print("Texte 'Caractéristique' détecté !")
            
            # Calculer les coordonnées du centre du mot et convertir en entiers
            x_center = int((bbox[0][0] + bbox[2][0]) // 2)
            y_center = int((bbox[0][1] + bbox[2][1]) // 2)

            # Définir la taille de la zone de capture
            width = 700  # Largeur de la zone
            height = 1200  # Hauteur de la zone

            # Définir les valeurs de recentrage
            x_offset = 0  # Décalage horizontal en pixels
            y_offset = 550  # Décalage vertical en pixels

            # Calculer les coordonnées de la zone de capture avec recentrage
            x = int(x_center - width // 2) + x_offset
            y = int(y_center - height // 2) + y_offset

            # Prendre la capture d'écran de la zone
            screenshot = pyautogui.screenshot(region=(x, y, width, height))

            # Convertir en format compatible avec OpenCV
            open_cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Enregistrer la capture d'écran
            cv2.imwrite("capture_caracteristique.png", open_cv_image)
            print("Capture d'écran enregistrée sous capture_caracteristique.png")
            break

if __name__ == "__main__":
    capture_dofus_window()
    detect_text_from_screenshot()