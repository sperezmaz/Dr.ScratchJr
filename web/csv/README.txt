-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------ESPAÑOL------------------------------------------------------------------------------------------------------------------------------------------------------------

CONTENIDO DEL .ZIP:  variability-1.csv, badhabits-1.csv, otherdata-1.csv y un data.xlsx con pestañas(variability, badhabits, otherdata).

DESCRIPCIÓN:

Variabilidad: Cada fila son datos de uso de bloques en un proyecto ScratchJr.

	(COLUMNAS)
	--Nombre: Nombre del estudiante.
	--Nombre del proyecto: Nombre del proyecto.
	--Eventos: Cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Eventos / total de bloques distintos que hay en tipo* de bloques Eventos.   
	--Movimiento: Cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Movimiento / total de bloques distintos que hay en tipo* de bloques Movimiento. 	
	--Apariencia: Cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Apariencia / total de bloques distintos que hay en tipo* de bloques Apariencia.   
	--Control: Cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Control / total de bloques distintos que hay en tipo* de bloques Control. 	
	--Sonido: Cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Sonido / total de bloques distintos que hay en tipo* de bloques Sonido. 	 
	--Finalización:	Cantidad de bloques distintos usados en el proyecto del tipo* de bloques Finalización / total de bloques distintos que hay en tipo* de bloques Finalización. 
	--Total: Cantidad de bloques totales de distinto tipo usados en todo el proyecto / total de bloques distintos.

		*TIPO DE BLOQUES:
			'Eventos': ['onflag', 'onclick', 'ontouch', 'message', 'onmessage']
        		'Movimiento': ['forward-back', 'up-down', 'left-right', 'hop', 'home']
        		'Apariencia': ['say', 'grow-shrink', 'same', 'hide-show']
        		'Sonido': ['playsnd', 'playusersnd']
        		'Control': ['wait', 'stopmine', 'repeat', 'setspeed']
        		'Finalización': ['endstack', 'forever', 'gotopage']


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Malos_hábitos: Cada fila es una secuencia de bloques con un mal hábito.

	(COLUMNAS).
	--Nombre: Nombre del estudiante.
	--Nombre del proyecto: Nombre del proyecto.
	--Tipo de mal hábito: Opciones Código inacabado/Código muerto/Secuencias con bloques adyacentes.
	--Existen malos hábitos: Opciones SI/NO. Si es NO, las demas columnas estaran vacias.
	--Página: Número de la página y en el orden en el que aparece en ScratchJr.
	--Persoanje: Nombre del personaje, donde hay una secunecia con un mal hábito.
	--Nombre de la secuencia: Nombre de la secuencia (no viene definido en ScratchJr)para distinguirlas, donde hay un mal hábito.
	--Secuencia: Conjunto de bloques unidos en ScratchJr, donde hay un mal hábito.


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	
Otros_datos: Cada fila son datos de un proyecto ScratchJr.
	(COLUMNAS)
	--Nombre: Nombre del estudiante.
	--Nombre del proyecto: Nombre del proyecto. 	
	--Total de páginas: Número de páginas que hay en un proyecto.	
	--Páginas: Lista con los nombres de las páginas que hay en un proyecto.	
	--Total de personajes: Número de personajes que hay en un proyecto.	
	--Personajes: Lista con los nombres de los personajes que hay en un proyecto.	
	--Total de textos: Número de textos que hay en un proyecto.	
	--Textos en páginas: Listas con una lista por cada texto: ['Pos-page ', 'Nombre del Texto', ['str_txt', 'Cadena de texto'], ['fontsize', Número de fuente]].
	--Total de páginas con fondo sin editar: Número de páginas con fondo sin editar que hay en un proyecto.	 
	--Páginas con fondo sin editar: Lista con los nombres de las páginas sin editar que hay en un proyecto.	
	--Total de personajes sin editar: Número de personajes sin editar que hay en un proyecto.	
	--Personajes sin editar: Lista con los nombres de los personajes sin editar que hay en un proyecto.	
	--Personajes en páginas: Diccionario con claves Pos-page y con valores una lista de los personajes que hay en la página de la clave. {'Pos-page': ['personaje', 'personaje', ...]}	
	--Personajes con mismo nombre: Número de veces que se repite el personaje en una misma pagina. {'Pos-page': {'personaje': número de veces que se repite}}


________________________________________________________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________________________________________________________
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------ENGLISH---------------------------------------------------------------------------------------------------------------------------------

.ZIP CONTENTS: variability-1.csv, badhabits-1.csv, otherdata-1.csv and a tabbed data.xlsx(variability, badhabits, otherdata).

DESCRIPTION:

Variability: Each row is block usage data in a ScratchJr project.

	(COLUMNS)
	--Name: Name of the student.
	--Project name: Name of project.
	--Triggerings: Number of distinct blocks used in the project, of block type* Triggerings / total distinct blocks in block type* Triggerings.   
	--Motion: Number of distinct blocks used in the project, of block type* Motion / total of distinct blocks in block type* Motion. 	
	--Looks: Number of distinct blocks used in the project, of block type* Looks / total number of distinct blocks in block type* Looks.   
	--Control: Number of distinct blocks used in the project, of block type* Control / total number of distinct blocks in block type* Control. 	
	--Sound: Number of distinct blocks used in the project, of block type* Sound / total number of distinct blocks in block type* Sound. 	 
	--Ends: Number of distinct blocks used in the project, of block type* Ends / total number of distinct blocks in block type* Ends. 
	--Total: Number of total distinct blocks of different type used in the whole project / total number of distinct blocks.


		*TYPE OF BLOCKS:
			'Triggerings': ['onflag', 'onclick', 'ontouch', 'message', 'onmessage']
        		'Motion': ['forward-back', 'up-down', 'left-right', 'hop', 'home']
        		'Looks': ['say', 'grow-shrink', 'same', 'hide-show']
        		'Sound': ['playsnd', 'playusersnd']
        		'Control': ['wait', 'stopmine', 'repeat', 'setspeed']
        		'Ends': ['endstack', 'forever', 'gotopage']


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Bad_habits: Each row is a sequence of blocks with a bad habit.

	(COLUMNS).
	--Name: Name of the student.
	--Project name: Project name.
	--Type of bad habit: Options Unfinished code/Dead code/Sequences with adjacent blocks.
	--Exist bad habits: Options YES/NO. If NO, the other columns will be empty.
	--Page: Page number and in the order it appears in ScratchJr.
	--Persoanje: Name of the character, where there is a sequence with a bad habit.
	--Sequence name: Name of the sequence (not defined in ScratchJr) to distinguish them, where there is a bad habit.
	--Sequence: Set of blocks joined in ScratchJr, where there is a bad habit.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	
Other_data: Each row is data from a ScratchJr project.

	(COLUMNS)
	--Name: Name of the student.
	--Project name: Name of the project. 	
	--Total pages: Number of pages in a project.	
	--Pages: List with the names of the pages that are in a project.	
	--Total characters: Number of characters in a project.	
	--Characters: List with the names of the characters in a project.	
	--Total texts: Number of texts in a project.	
	--Texts in pages: Lists with a list for each text: ['Pos-page ', 'Text name', ['str_txt', 'Text string'], ['fontsize', Font number]].
	--Total pages with unedited background: Number of pages with unedited background in a project.	 
	--Pages with unedited background: List with the names of the unedited pages in a project.	
	--Total unedited characters: Number of unedited characters in a project.	
	--Total unedited characters: List with the names of the unedited characters in a project.	
	--Characters in pages: Dictionary with Pos-page keys and with values a list of the characters that are in the page of the key. {'Pos-page': ['character', 'character', ...]}	
	--Characters with the same name: Number of times the character is repeated in the same page. {'Pos-page': {'character': number of times repeated}}
