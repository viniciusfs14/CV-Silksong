import cv2
import numpy as np
import mss
import win32gui
from ultralytics import YOLO
import time

#  Nome da janela do jogo
JANELA_JOGO = "Silksong"

#  Função para localizar a janela pelo título
def obter_janela(titulo_parcial):
    def callback(hwnd, lista):
        if win32gui.IsWindowVisible(hwnd):
            titulo = win32gui.GetWindowText(hwnd)
            if titulo_parcial.lower() in titulo.lower():
                lista.append(hwnd)
    janelas = []
    win32gui.EnumWindows(callback, janelas)
    return janelas[0] if janelas else None

hwnd = obter_janela(JANELA_JOGO)
if hwnd is None:
    print(f"❌ Janela '{JANELA_JOGO}' não encontrada!")
    exit()

left, top, right, bottom = win32gui.GetWindowRect(hwnd)
width = right - left
height = bottom - top

# 🔹 Carrega o modelo YOLO treinado
model = YOLO("runs/detect/silksong_yolo/weights/best.pt")

# 🔹 Configura captura de tela
sct = mss.mss()
monitor = {"top": top, "left": left, "width": width, "height": height}

# 🔹 Variáveis para suavização e FPS
last_detections = None
prev_time = time.time()

while True:
    # Captura da tela
    frame = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # Ajuste automático de brilho/contraste
    frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=20)

    # Inferência YOLO
    results = model.predict(frame, conf=0.1, imgsz=960, verbose=False)
    boxes = results[0].boxes.data  # coordenadas + conf

    # 🔹 Suavização: mantém últimas detecções se não houver nesta frame
    if len(boxes) > 0:
        last_detections = results[0]
    annotated = last_detections.plot() if last_detections else frame

    # Exibe resultado
    cv2.imshow("Detecção Silksong", annotated)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
