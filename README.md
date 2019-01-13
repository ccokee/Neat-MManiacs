#Acerca de:
Este programa usa la libreria neat-python y el emulador de gameboy PyBoy para, mediante una red neuronal evolutiva, tratar de jugar automaticamente el primer nivel del juego clásico Motocross Maniacs de Game Boy.

#Instalacion:
Primero tendremos que instalar pypy y sus dependencias para poder arrancar pyboy y usar neat-python.

##macOS
	La forma mas sencilla de comenzar es instalando Brew
	
	Una vez instalado Brew, actualizamos e instalamos sus dependencias

	brew update
	brew install git pypy sdl2 sdl2_gfx sdl2_image
	brew link sdl2

	pip_pypy install -r requerimientos.txt

###Ubuntu/Linux
	En Ubuntu (no en todos los linux) tendremos que usar un entorno virtual para arrancar pypy por problemas de compatibilidad con la version de cpython instalada.

	sudo apt update
	sudo apt install git pypy pypy-dev virtualenv libsdl2-dev
	
	Ahora nos vamos a la carpeta del proyecto y creamos el entorno virtual:

	virtualenv . -p $(which pypy)
	source ./bin/activate

	pip install -r requerimientos.txt

###Windows
	Primero, instalar Git, vcredist y VCForPython27:

	https://git-scm.com/download/win
	https://www.microsoft.com/en-us/download/details.aspx?id=5582
	https://www.microsoft.com/en-us/download/details.aspx?id=44266

	Luego, bajar la ultima version construida de  Pypy de 32 bit:

	https://bitbucket.org/pypy/pypy/downloads/

	Descomprimir en algun lugar como: C:\pypy2\

	Busca "Editar variables del sistema" desde el menú de inicio. Añade C:\pypy2; al principio de la variable PATH

	Arranca cmd.exe y ejecuta:

	pypy -m ensurepip
	pypy -m pip install -U pip wheel
	pypy -m pip install -r requerimientos.txt

	Bajar el SDL2 Runtime Binario para windows de 32 bit

	https://www.libsdl.org/download-2.0.php

	Guardalo en C:\pypy2\SDL2.dll. y luego pon la variable de sistema en la consola:

	set PYSDL2_DLL_PATH=C:\pypy2\SDL2.dll

#Uso

Por último solo tendremos que hacer:

pypy Neat-MManiacs-evol.py 

o

pypy Neat-MManiacs-play.py

Para jugar con el genoma con mejor fitness, desde la carpeta del proyecto.
