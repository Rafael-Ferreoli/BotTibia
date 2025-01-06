import threading
from time import sleep

import pyautogui as pg
import keyboard
import time
import json
from pynput import keyboard
from constants import FOLDER_NAME, REGION_BATTLE, REGION_LOOT, REGION_MAP

# Evento para parar o bot
global event_th
event_th = threading.Event()
th_run = None  # Garantir que a thread não seja iniciada múltiplas vezes

# Função para verificar monstros na tela
def check_battle():
    try:
        return pg.locateOnScreen('images/battle.png', region=REGION_BATTLE)
    except Exception as e:
        print(f"Erro ao verificar batalha: {e}")
        return None


def check_and_handle_anchor():
    try:
        box = pg.locateOnScreen('images/exit_arbusto.png', confidence=0.8)
        if box:
            print("Âncora encontrada, realizando ações...")
            pg.moveTo(1340, 13)
            sleep(1)
            pg.click()
            pg.moveTo(832, 395)
            sleep(1)
            pg.click()
            # Para o bot ao encontrar a âncora
            event_th.set()
            print("Bot interrompido devido à âncora.")
            return True
        return False
    except Exception as e:
        print(f"Erro ao verificar ou lidar com âncora: {e}")
        return False


# Função para matar monstros
def kill_monster():
    try:
        while check_battle() is None:
            print("Matando monstros...")
            if event_th.is_set():
                return
            pg.press('space')

            while True:
                screenshot = pg.screenshot(region=REGION_BATTLE)
                found = False

                for x in range(screenshot.width):
                    for y in range(screenshot.height):
                        pixel_color = screenshot.getpixel((x, y))
                        if (250 <= pixel_color[0] <= 255) and (pixel_color[1] == 0) and (pixel_color[2] == 0):
                            found = True
                            break
                    if found:
                        break

                if not found:
                    print("Linha vermelha não encontrada. O monstro morreu!")
                    get_loot()
                    break
                else:
                    if event_th.is_set():
                        return
                    print("Esperando o monstro morrer...")
                time.sleep(1)
    except Exception as e:
        print(f"Erro ao matar monstro: {e}")

# Função para coletar loot
def get_loot():
    pg.press('F8')
    print('Pegando loot')

# Função para descer buraco
def hole_down(should_down):
    try:
        if should_down:
            box = pg.locateOnScreen('images/hole.png', confidence=0.8)
            if box:
                x, y = pg.center(box)
                if event_th.is_set():
                    return
                pg.moveTo(x, y)
                pg.click()
                time.sleep(5)
    except Exception as e:
        print(f"Erro ao descer buraco: {e}")

# Função para subir buraco
def hole_up(should_up, img_anchor, plux_x, plux_y):
    try:
        if should_up:
            box = pg.locateOnScreen(img_anchor, confidence=0.8)
            if box:
                x, y = pg.center(box)
                if event_th.is_set():
                    return
                pg.moveTo(x + plux_x, y + plux_y, 5)
                pg.press('F1')
                pg.click()
                time.sleep(5)
    except Exception as e:
        print(f"Erro ao subir buraco: {e}")

def eat_food():
    pg.press('F2')
    print('Comendo comida')
    sleep(1)
    pg.press('F3')
    print('Treinando ML')

# Função para se mover até a flag
def go_to_flag(path, wait):
    try:
        flag = pg.locateOnScreen(path, confidence=0.7, region=REGION_MAP)
        if flag:
            x, y = pg.center(flag)
            if event_th.is_set():
                return
            pg.moveTo(x, y)
            pg.click()
            time.sleep(wait)
    except Exception as e:
        print(f"Erro ao ir até a flag: {e}")

# Função principal
def run():
    try:
        with open(f'{FOLDER_NAME}/infos.json', 'r') as file:
            data = json.loads(file.read())

        print('Data carregada:', data)
        while not event_th.is_set():
            for item in data:
                # Verifica e lida com a âncora, se necessário
                if check_and_handle_anchor():
                    print("Ações da âncora concluídas, continuando...")
                if event_th.is_set():
                    return
                kill_monster()
                if event_th.is_set():
                    return
                time.sleep(1)
                get_loot()
                if event_th.is_set():
                    return
                go_to_flag(item['path'], item['wait'])
                eat_food()
                if event_th.is_set():
                    return
                #hole_down(item['down_hole'])
                #hole_up(item['up_hole'], f'{FOLDER_NAME}/anchor_floor_2.png', 260, 0)
                #hole_up(item['up_hole'], f'{FOLDER_NAME}/anchor_floor_3.png', 80, 80)
    except Exception as e:
        print(f"Erro na execução do bot: {e}")

# Função para capturar teclas
def key_code(key):
    global th_run
    print('Tecla pressionada:', key)
    if key == keyboard.Key.esc:
        event_th.set()
        return False
    if key == keyboard.Key.delete:
        if th_run is None or not th_run.is_alive():
            th_run = threading.Thread(target=run)
            th_run.start()
        else:   
            print("Bot já está em execução!")

# Início do listener de teclado
with keyboard.Listener(on_press=key_code) as listener:
    listener.join()
