-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------ESPAÑOL------------------------------------------------------------------------------------------------------------------------------------------------------------

CONTENIDO DEL .ZIP:  variability-1.csv, badhabits-1.csv, otherdata-1.csv y un data.xlsx con pestañas(variability, badhabits, otherdata).

DESCRIPCIÓN:

Variabilidad: cada fila son datos de uso de bloques en un proyecto ScratchJr.

	(COLUMNAS)
	--Nombre: nombre del estudiante.
	--Nombre del proyecto: nombre del proyecto.
	--Eventos: cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Eventos / total de bloques distintos que hay en tipo* de bloques Eventos.   
	--Movimiento: cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Movimiento / total de bloques distintos que hay en tipo* de bloques Movimiento. 	
	--Apariencia: cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Apariencia / total de bloques distintos que hay en tipo* de bloques Apariencia.   
	--Control: cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Control / total de bloques distintos que hay en tipo* de bloques Control. 	
	--Sonido: cantidad de bloques distintos usados en el proyecto, del tipo* de bloques Sonido / total de bloques distintos que hay en tipo* de bloques Sonido. 	 
	--Finalización:	cantidad de bloques distintos usados en el proyecto del tipo* de bloques Finalización / total de bloques distintos que hay en tipo* de bloques Finalización. 
	--Total: cantidad de bloques totales de distinto tipo usados en todo el proyecto / total de bloques distintos.

		*TIPO DE BLOQUES:
			'Eventos': ['onflag', 'onclick', 'ontouch', 'message', 'onmessage']
        		'Movimiento': ['forward-back', 'up-down', 'left-right', 'hop', 'home']
        		'Apariencia': ['say', 'grow-shrink', 'same', 'hide-show']
        		'Sonido': ['playsnd', 'playusersnd']
        		'Control': ['wait', 'stopmine', 'repeat', 'setspeed']
        		'Finalización': ['endstack', 'forever', 'gotopage']


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Malos_hábitos: cada fila es una secuencia de bloques con un mal hábito.

	(COLUMNAS).
	--Nombre: nombre del estudiante.
	--Nombre del proyecto: nombre del proyecto.
	--Tipo de mal hábito: opciones Código inacabado/Código muerto/Secuencias con bloques adyacentes.
	--Existen malos hábitos: opciones SI/NO. Si es NO, las demas columnas estaran vacias.
	--Página: número de la página y en el orden en el que aparece en ScratchJr.
	--Persoanje: nombre del personaje, donde hay una secunecia con un mal hábito.
	--Nombre de la secuencia: nombre de la secuencia (no viene definido en ScratchJr)para distinguirlas, donde hay un mal hábito.
	--Secuencia: conjunto de bloques unidos en ScratchJr, donde hay un mal hábito.


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	
Otros_datos: cada fila son datos de un proyecto ScratchJr.
	(COLUMNAS)
	--Nombre: nombre del estudiante.
	--Nombre del proyecto: nombre del proyecto. 	
	--Total de páginas: número de páginas que hay en un proyecto.	
	--Páginas: lista con los nombres de las páginas que hay en un proyecto.	
	--Total de personajes: número de personajes que hay en un proyecto.	
	--Personajes: lista con los nombres de los personajes que hay en un proyecto.	
	--Total de textos: número de textos que hay en un proyecto.	
	--Textos en páginas: listas con una lista por cada texto: ['Pos-page ', 'Nombre del Texto', ['str_txt', 'Cadena de texto'], ['fontsize', Número de fuente]].
	--Total de páginas con fondo sin editar: número de páginas con fondo sin editar que hay en un proyecto.	 
	--Páginas con fondo sin editar: lista con los nombres de las páginas sin editar que hay en un proyecto.	
	--Total de personajes sin editar: número de personajes sin editar que hay en un proyecto.	
	--Personajes sin editar: lista con los nombres de los personajes sin editar que hay en un proyecto.	
	--Personajes en páginas: diccionario con claves Pos-page y con valores una lista de los personajes que hay en la página de la clave. {'Pos-page': ['personaje', 'personaje', ...]}	
	--Personajes con mismo nombre: número de veces que se repite el personaje en una misma pagina. {'Pos-page': {'personaje': número de veces que se repite}}


________________________________________________________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________________________________________________________
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------ENGLISH---------------------------------------------------------------------------------------------------------------------------------

.ZIP CONTENTS: variability-1.csv, badhabits-1.csv, otherdata-1.csv and a tabbed data.xlsx(variability, badhabits, otherdata).

DESCRIPTION:

Variability: each row is block usage data in a ScratchJr project.

	(COLUMNS)
	--Name: name of the student.
	--Project name: name of project.
	--Triggerings: number of distinct blocks used in the project, of block type* Triggerings / total distinct blocks in block type* Triggerings.   
	--Motion: number of distinct blocks used in the project, of block type* Motion / total of distinct blocks in block type* Motion. 	
	--Looks: number of distinct blocks used in the project, of block type* Looks / total number of distinct blocks in block type* Looks.   
	--Control: number of distinct blocks used in the project, of block type* Control / total number of distinct blocks in block type* Control. 	
	--Sound: number of distinct blocks used in the project, of block type* Sound / total number of distinct blocks in block type* Sound. 	 
	--Ends: number of distinct blocks used in the project, of block type* Ends / total number of distinct blocks in block type* Ends. 
	--Total: number of total distinct blocks of different type used in the whole project / total number of distinct blocks.


		*TYPE OF BLOCKS:
			'Triggerings': ['onflag', 'onclick', 'ontouch', 'message', 'onmessage']
        		'Motion': ['forward-back', 'up-down', 'left-right', 'hop', 'home']
        		'Looks': ['say', 'grow-shrink', 'same', 'hide-show']
        		'Sound': ['playsnd', 'playusersnd']
        		'Control': ['wait', 'stopmine', 'repeat', 'setspeed']
        		'Ends': ['endstack', 'forever', 'gotopage']


-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Bad_habits: each row is a sequence of blocks with a bad habit.

	(COLUMNS).
	--Name: name of the student.
	--Project name: project name.
	--Type of bad habit: options Unfinished code/Dead code/Sequences with adjacent blocks.
	--Exist bad habits: options YES/NO. If NO, the other columns will be empty.
	--Page: page number and in the order it appears in ScratchJr.
	--Persoanje: name of the character, where there is a sequence with a bad habit.
	--Sequence name: name of the sequence (not defined in ScratchJr) to distinguish them, where there is a bad habit.
	--Sequence: set of blocks joined in ScratchJr, where there is a bad habit.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	
Other_data: each row is data from a ScratchJr project.

	(COLUMNS)
	--Name: name of the student.
	--Project name: name of the project. 	
	--Total pages: number of pages in a project.	
	--Pages: list with the names of the pages that are in a project.	
	--Total characters: number of characters in a project.	
	--Characters: list with the names of the characters in a project.	
	--Total texts: number of texts in a project.	
	--Texts in pages: lists with a list for each text: ['Pos-page ', 'Text name', ['str_txt', 'Text string'], ['fontsize', Font number]].
	--Total pages with unedited background: number of pages with unedited background in a project.	 
	--Pages with unedited background: list with the names of the unedited pages in a project.	
	--Total unedited characters: number of unedited characters in a project.	
	--Total unedited characters: list with the names of the unedited characters in a project.	
	--Characters in pages: dictionary with Pos-page keys and with values a list of the characters that are in the page of the key. {'Pos-page': ['character', 'character', ...]}	
	--Characters with the same name: number of times the character is repeated in the same page. {'Pos-page': {'character': number of times repeated}}
