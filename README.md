# **Discord RAT Windows - botConnect**

This project is a **Remote Administration Tool (RAT)** based on **Discord**, which allows commands to be executed remotely on a victim machine via a Discord bot. The bot connects to a user-specified Discord server, and commands are executed via a text channel within the Discord server, making it easy to manage remotely in a controlled environment.

The bot is capable of executing custom commands prefixed with `!`, providing full access to the victim machine and facilitating real-time interaction. The project includes several tools to automate the creation and compilation of an **executable file (EXE)** that can be executed on the victim machine without raising suspicion.

---

## **Project Characteristics**

The project includes the following scripts and functionalities:

### 1. **botConnect.py**

- **Main Function**: This script generates the connection of the Discord bot that connects to a specific server.
- **Commands**:
    - `!myhelp`: Shows a list of available commands.
    - `!geolocate`: Shows the public IP address of the victim machine, plus other information about the location of said IP.
    - **Additional commands**: Custom commands that you can define to interact with the victim machine.

## !myhelp (List)

### 📜 Comandos Disponibles

### Comandos Generales:

- `!message` = Mostrar un cuadro de mensaje con tu texto  
  Sintaxis: `!message ejemplo`

- `!shell` = Ejecutar un comando de shell  
  Sintaxis: `!shell whoami`

- `!voice` = Hacer que una voz diga en voz alta una frase personalizada  
  Sintaxis: `!voice prueba`

- `!admincheck` = Comprobar si el programa tiene privilegios de administrador

- `!cd` = Cambiar de directorio

- `!dir` = Mostrar todos los elementos en el directorio actual

- `!download` = Descargar un archivo desde el ordenador infectado

- `!upload` = Subir un archivo al ordenador infectado  
  Sintaxis: `!upload archivo.png` (con archivo adjunto)

- `!delete` = Eliminar un archivo  
  Sintaxis: `!delete /ruta/del/archivo.txt`

- `!write` = Escribir tu frase deseada en el ordenador

- `!clipboard` = Recuperar el contenido del portapapeles del ordenador infectado

- `!idletime` = Obtener el tiempo de inactividad de los usuarios en el ordenador objetivo

- `!datetime` = Mostrar fecha y hora actuales

- `!currentdir` = Mostrar el directorio actual

---

### Escalado de Privilegios y Control del Sistema:

- `!getadmin` = Solicitar privilegios de administrador a través del aviso UAC

- `!block` = Bloquear el teclado y el ratón del usuario (Se requieren privilegios de administrador)

- `!unblock` = Desbloquear el teclado y el ratón del usuario (Se requieren privilegios de administrador)

- `!screenshot` = Tomar una captura de pantalla de la pantalla actual del usuario

- `!exit` = Salir del programa

- `!kill` = Matar una sesión o proceso  
  Sintaxis: `!kill session-3` o `!kill all`

- `!uacbypass` = Intentar eludir UAC para obtener privilegios de administrador

- `!shutdown` = Apagar el ordenador

- `!restart` = Reiniciar el ordenador

- `!logoff` = Cerrar sesión del usuario actual

- `!bluescreen` = Provocar una pantalla azul (Se requieren privilegios de administrador)

- `!migrateprocess <process_name>` = Migrar un proceso en ejecución a una nueva instancia.  
  Sintaxis: `!migrateprocess ejemplo.exe`

---

### Seguridad y Modificaciones del Sistema:

- `!prockill` = Matar un proceso por nombre  
  Sintaxis: `!prockill proceso`

- `!disabledefender` = Deshabilitar Windows Defender (Se requieren privilegios de administrador)

- `!disablefirewall` = Deshabilitar el Firewall de Windows (Se requieren privilegios de administrador)

- `!critproc` = Convertir el programa en un proceso crítico (Se requieren privilegios de administrador)

- `!uncritproc` = Eliminar el estado de proceso crítico (Se requieren privilegios de administrador)

- `!website` = Abrir un sitio web en el ordenador infectado  
  Sintaxis: `!website www.google.com`

- `!disabletaskmgr` = Deshabilitar el Administrador de Tareas (Se requieren privilegios de administrador)

- `!enabletaskmgr` = Habilitar el Administrador de Tareas (Se requieren privilegios de administrador)

- `!startup` = Agregar el programa al inicio

---

### Geolocalización y Comandos Varios:

- `!geolocate` = Geolocalizar el ordenador usando la latitud y longitud de la IP

- `!listprocess` = Listar todos los procesos

- `!infocounts` = Obtener información de las cuentas del sistema

- `!rootkit` = Lanzar un rootkit (Se requieren privilegios de administrador) [No disponible]

- `!unrootkit` = Eliminar el rootkit (Se requieren privilegios de administrador) [No disponible]

- `!getcams` = Listar los nombres de las cámaras

- `!selectcam` = Seleccionar una cámara para tomar una foto  
  Sintaxis: `!selectcam 1`

- `!webcampic` = Tomar una foto con la cámara web seleccionada

- `!myhelp` = Este menú de ayuda

### 2. **CompilerPYtoEXE.py**

- **Main Function**: Automates the bot configuration and compilation process into an executable **.exe** file.
- **Process**:
    - Requests the user for the **Bot Token** and the **Server ID** (the Discord server ID).
    - Compiles the Python file (`botConnect.py`) to an EXE file that can be executed on the victim machine.

### 3. **guiaAutoextraibleEXE.py**

- **Main Function**: Detailed instructions on how to package the `.exe` file with a `fake_error.vbs` file (which simulates a Windows error), the guide is in the script called `guiaAutoextraibleEXE.py`.
- **Goal**: Make the `.exe` file go unnoticed by packaging it in a **self-extracting** file that simulates a Windows error.

### 4. **ScriptSmartScreen**

- **Main Function**: Scripts that allow you to disable the Windows **SmartScreen** to prevent the executable file from blocking.
- Includes:
    - **DuckyScript**: To disable SmartScreen.
    - **PowerShell script**: To disable SmartScreen automatically on the victim machine.

> NOTE:

For these 2 previous scripts ``social engineering`` would be needed so that somehow the victim user executes at least the ``.ps1`` script and thus deactivates the ``SmartScreen``.
### 5. **ExclusionWindowsDefender (Windows 11)**

- **Main Function**: Tool to prevent **Windows Defender** from detecting the executable file as a threat.
- **Instructions**: Include a file `folderExcludedWindowsDefender.ps1` to create a folder excluded from Windows Defender scans, ensuring that the executable file is not detected.

> NOTA:

Para este script de aqui de la misma forma que antes, habria que hacer algun tipo de ``ingenieria social`` para que el usuario victima ejecute dicho script y asi que se le genere una carpeta que evite el ``Windows Defender`` donde se deposite nuestro ``Troyano``. (En Windows 10 no lo suele detectar como "Malware")

---

## **Requisitos Previos**

Antes de ejecutar este proyecto, asegúrate de tener configurados los siguientes requisitos:

1. **Python 3.x**: Este proyecto está escrito en ``Python3``. Puedes instalarlo desde el siguiente enlace:
    
    - [Descargar Python 3 desde Microsoft Store](https://apps.microsoft.com/detail/9NRWMJP3717K?hl=neutral&gl=ES&ocid=pdpshare)
    
1. **Dependencias**:
    
    - Este proyecto requiere varias bibliotecas ``Python`` que se instalarán automáticamente a través del archivo `requirements.txt`.
    
    Para instalar las dependencias necesarias, simplemente ejecuta el siguiente comando en tu terminal:
	
	```
	pip install -r requirements.txt
	```
    
    Esto instalará todas las bibliotecas necesarias para que el proyecto funcione correctamente.
    

---

## **Uso del Proyecto**

### 1. **Compilación del Bot con `CompilerPYtoEXE.py`**

El script ``CompilerPYtoEXE.py`` automatiza el proceso de configuración del ``bot`` y la compilación del archivo **.exe**.

#### Pasos para ejecutar **CompilerPYtoEXE.py**:

1. **Ejecuta el script `main.py`** haciendo doble clic sobre él.
    
    - **Importante**: **Nunca ejecutes directamente el script `CompilerPYtoEXE.py`**, ya que si lo haces, el proceso de compilación fallará. El script `main.py` se encarga de ejecutar correctamente **CompilerPYtoEXE.py**.
    
2. **Proporciona los datos del bot**:  

    El script abrirá una ventana de configuración donde deberás ingresar el **Bot Token** y el **Server ID**:
    
    - **Bot Token**: Puedes obtener este token desde el ``Discord Developer`` Portal.
    - **Server ID**: Este es el ``ID`` del servidor de ``Discord`` al que el bot se conectará. Para obtenerlo, activa el modo de desarrollador en ``Discord`` y haz clic derecho sobre el servidor para copiar su ``ID``.
    
3. **Selecciona el archivo `botConnect.py`**:

    Una vez configurado el bot, selecciona el archivo `botConnect.py` que deseas usar para compilar.
    
4. **Especifica la ubicación del archivo compilado**:  

    Después de seleccionar el archivo, se te pedirá que elijas la ubicación donde quieres guardar el archivo **.exe** compilado.
    
5. **Espera a que se complete la compilación**:  

    El script generará el archivo **.exe** que podrás ejecutar en la máquina víctima para que el bot se conecte al servidor de ``Discord`` especificado.
    
### Video practico:

https://github.com/user-attachments/assets/d5e40b83-6d99-4d84-95ef-77d46511ccb9

---

### 2. **Evitar el Bloqueo de SmartScreen**

#### 1. **DuckyScript**:

- **Función**: Desactiva el ``SmartScreen`` para que no se bloquee el archivo ``.exe`` al ejecutarlo.
- **Uso**: Simplemente ejecuta el ``DuckyScript`` en el entorno de la víctima para desactivar ``SmartScreen`` con un ``BadUSB``. (Aunque esto requiere tener el PC de la victima a nivel físico)

#### 2. **Script en PowerShell (Carpeta `ScriptSmartScreen`)**:

- Se incluye un script en ``PowerShell`` que desactiva el ``SmartScreen`` de forma automática.
- **Ejecuta el script de PowerShell** para evitar que ``SmartScreen`` bloquee la ejecución del archivo ``.exe`` generado. (Esta técnica habría que realizar una ``ingenieria social`` para ello)

---

### 3. **Evitar la Detección de Windows Defender (Windows 11)**

En algunos casos, **Windows Defender** podría detectar el archivo ejecutable como una amenaza en ``Windows 11``. Para evitar esto, se incluyen herramientas para excluir el archivo ejecutable de los escaneos de ``Windows Defender``.

#### Pasos para evitar la detección de Windows Defender:

1. **Ejecuta el script `carpetaExcluidaWindowsDefender.ps1`**:
    
    - Este script creará una carpeta que será excluida de los escaneos de ``Windows Defender``.
    - **Ejecuta el script con PowerShell** para asegurarte de que la carpeta donde almacenarás el archivo ``EXE`` no sea escaneada por ``Windows Defender``.
    
2. **Mueve el archivo .exe a la carpeta excluida**:
    
    - Después de ejecutar el script, mueve el archivo **.exe** generado a la carpeta que fue excluida de los escaneos de ``Windows Defender``.

---

### 4. **Hacer el Archivo `.exe` Más Realista**

Para que el archivo **.exe** pase desapercibido, se incluye el archivo `guiaAutoextraible.py`, que explica cómo crear un archivo **autoextraíble** con **WinRAR**.

#### Pasos para empaquetar el archivo `.exe` como autoextraíble:

1. **Prepara el archivo `.exe`** generado y el archivo `fake_error.vbs` (que simula un error de Windows).
2. Usa **WinRAR** para empaquetar ambos archivos en un archivo **autoextraíble**.
3. El archivo autoextraíble se ejecutará y simulará un error de ``Windows``, haciendo que el bot pase desapercibido.

### Video practico:

https://github.com/user-attachments/assets/1f287107-ead9-4403-a1e7-63d565a0eddb

---

### 5. **Configuración del Bot de Discord**

Para configurar el bot de Discord:

1. Ejecuta el archivo `DiscordBotPage.bat` para ser redirigido a la página de configuración del bot en el **Discord Developer Portal**.
2. Sigue los pasos en la página para configurar el **Bot Token** y obtener los permisos necesarios para el bot en tu servidor.

---

## **Advertencia y Uso Responsable**

Este proyecto está destinado a fines educativos y para pruebas de penetración en entornos controlados. **No uses este proyecto sin el consentimiento explícito del propietario del sistema que estás controlando.** El uso no autorizado de este tipo de herramientas es ilegal y está en contra de los términos de servicio de Discord, así como de las leyes locales e internacionales.

Este proyecto no debe ser utilizado para actividades maliciosas o para comprometer sistemas sin el consentimiento de las partes involucradas.

---

## **Contribuciones**

Si deseas contribuir al proyecto, por favor, abre un **pull request** o reporta cualquier problema en la sección de **issues** de este repositorio.
