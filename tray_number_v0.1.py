import pystray
from PIL import Image, ImageDraw, ImageFont
import threading
import time
import sys
import capturar_numero as cn

def criar_icone(numero, tamanho_fonte=24):
    # Criar imagem quadrada
    img = Image.new('RGB', (24, 24), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Desenhar círculo de fundo
    if numero > 60:
        draw.ellipse((0, 0, 24, 24), fill=(255, 0, 0))

    # Carregar fonte (pode usar qualquer .ttf do sistema)
    try:
        fonte = ImageFont.truetype("arial.ttf", tamanho_fonte)
    except:
        # fallback se não encontrar a fonte
        fonte = ImageFont.load_default()

    # Escrever número
    draw.text((0, 0), str(numero), font=fonte, fill=(255, 255, 255))

    return img

# Função que atualiza o ícone a cada 12 segundos
def atualizar_icone(icone):
    numero = 0
    while True:
        numero =  int(cn.capturar_temp())
        icone.icon = criar_icone(numero, tamanho_fonte=20)
        icone.title = f"Carga CPU: {numero}"
        icone.update_menu()   # atualiza menu se necessário
        time.sleep(3)

def sair(icone):
     print('\nusuario solicitou fechar...\n')
     icone.stop() # encerra o ícone
     sys.exit(0) # força saída do programa inteiro 

# Criar ícone inicial
icone = pystray.Icon("numero", criar_icone(0, tamanho_fonte=20), title=f"Número: 0")
icone.menu = pystray.Menu(pystray.MenuItem("Ocultar", lambda: sair(icone)))

# Rodar thread de atualização
threading.Thread(target=atualizar_icone, args=(icone,), daemon=True).start()

icone.run()
