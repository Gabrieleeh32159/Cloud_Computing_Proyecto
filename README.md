# Insider_blog_UTEC_DBP10_grupo5
Proyecto 1 del grupo 5 del laboratorio 1.01 del curso DBP. Insider Blog.

# Nombre del proyecto
El nombre del proyecto es "Insider Blog"

# Integrantes
- Gabriel Espinoza
- Kevin Huaman
- Marcelo Zuloeta
- Martín Pérez-Bonany
- Paolo Vásquez

# Descripcion del proyecto
Foro web con la finalidad de conectar universitarios con fines de crear grupos de estudio, resolver problemas específicos y conectar juniors con oportunidades de prácticas laborales.

# Licencia de uso
Este proyecto cuenta con licencia conforme a los términos de la licencia MIT

# Objetivos principales / Mision / Vision
El objetivo principal del proyecto es conectar universitarios de varias casas de estudio en la región.
Nuestra misión es que diversos grupos de universitarios de diferentes universidades puedan conectarse con motivos de estudio o prácticas pre-profesionales.
Nuestra visión es ser el principal portal de conectividad entre universitarios del Perú, ofreciendo un servicio simple pero efectivo y funcional.

## Informacion acerca de las librerias/frameworks/plugins utilizadas en Front-end, Back-end y Base de datos
### VUE.js : Framework en javascript en el que desarrollamos todo el frontend
#### Axios : Nuestra libreria para la comunicacion http y requests ajax
#### Vuex : libreria para almacenar componentes de nuestra app
#### Bootstrap : framework para nuestro frontend que facilita el desarrollo de html y css
#### Router : libreria para manejar nuestras Rutas

## Frontend
-flask : Framework principal con el que hacemos la aplicacion

# Informacion acerca de las librerias/frameworks/plugins utilizadas en Front-end, Back-end y Base de datos
-vue: framework utilizado para la creación del frontend
>>>>>>> f40b0f9f948f1ea5a7780f47a48b2781dee9a60d
-datetime : Para guardar los posts con la fecha de creacion.
-wtforms : Validadores de email, longitud, data requerida, etc para los formularios
-PIL : Para la compresion de imagenes que se usan en los perfiles
-secrets : Para generar una cadena de caracteres aleatorios para serializar
-os : Para usar algunas variables de entorno y unos path para las imagenes

# El nombre del script a ejecutar para iniciar la base de datos con datos
## Backend:
desde la carpeta de INSIDER_BLOG_UTEC_DBP10_grupo5
### CMD: 
cd insider_blog_backend para acceder a la carpeta
set flask_app = server
set flask_env = development
flask run

## Frontend
### CMD:
cd insider_blog_frontend para acceder a la carpeta
npm lint --fix : para realizar un lint en nuestros archivos
yarn serve : para levantar el servidor

# Informacion acerca de los API. Requests y Responses de cada endpoint utilizado en el sistema.
## Rutas del backend:
/users -> GET : Para obtener el json con los usuarios
/signup -> GET, POST : Para añadir un nuevo usuario
/users -> POST : Para añadir un nuevo usuario (version DEPRECADA de prueba para postman)
/user -> GET : Peticion de prueba para validar un token
/login -> GET, POST : Para pasar los datos del usuario y mediante jwt obtener el token
/users/user_id -> PATCH : actualizar la informacion de un usuario
/users/user_id -> DELETE : borrar un usuario
/groups -> POST : Para añadir un nuevo grupo
/groups -> GET : retorna todos lo grupos (lo usamos sobretodo en el frontend para obtener Informacion)
/groups/group_id -> DELETE : borrar un grupo
/groups/group_id -> PATCH : actualizar la informacion de un grupo
/posts -> POST : Crear un post
/posts -> GET : obtener los posts (usando paginacion)
/posts/post_id -> PATCH : actualizar la informacion de un post
/posts/post_id -> DELETE : borrar un post
/user/user_id/group/group_id -> POST : añadir un usuario a un grupo
/user/user_id/group/group_id -> DELETE : borrar un usuario a un grupo
/groupusers -> GET : Retornar los usuarios que pertenezcan a un grupo

## Rutas del frontend:
/ : home = La pagina principal de nuestra pagina
/about : about = Pagina que muestra informacion sobre nosotros y nuestra ubicacion en google maps
/login : login = Pagina con formulario para que los usuarios se puedan logear
/register : register = Pagina con formulario para que los usuarios puedan registrarse
/newpost : newpost = Pagina con formulario para crear una nueva publicacion
/groups/:slug : Groups = Pagina donde aparecen todos los posts de un grupo
/user/:slug : Users = Pagina donde se muestran los posts de un usuario y esta la opcion de editarlo tambien
/newgroup : newgroup = Pagina con formulario para crear un nuevo grupo
/edit/:slug : edit = Pagina con formulario para actualizar los datos de un usuario

# Hosts
Frontend VUE.js : Localhost Puerto: 3000
Backend Flask : Localhost Puerto : 5000
# Forma de autenticacion
Usamos JWT para autenticar a los usuarios. Todos los usuarios son creados con un public_id que es creado usando un identficador universal, en nuestro caso usamos el uuid4, y la clave es hasheada por la libreria werkzeug usando el sha256 el cual es un hash cryptografico bastante popular desarrollado por la seguridad nacional de Estados Unidos. Cuando un usuario se loguea e ingresa tanto su usuario como contraseña, este pasa por el encabezado de autorizacion en la solicitud y nuestro backend primero busca que el usuario exista, luego desencripta la contraseña y comprueba que sea valida para finalmente usando el json web token, retorne un token unico que dura 30 minutos hecho con nuestra secret key. 

Posterior a eso nuestro servidor de frontend almacena el token de manera local usando la funcion localStorage y el usuario se almacena en nuestro "store" usando vuex. Despues cada solicitud que necesite validar al usuario utiliza nuesra funcion "token_required" la cual consiste en pasar en el encabezado el token y usando el algoritmo de decodificacion de jwt con nuestra secret key y el algoritmo utilizado (HS256) este nos retorna el usuario y asi la solicitud continua o retorna un error. 

# Errores HTTP:
- 500: Lo utilizamos para cuando se genera algun error en el servidor
- 404: En caso el cliente trate de acceder a una ruta inexistente
- 403: En caso el cliente trate de acceder a una ruta a la que no tiene permisos para acceder
- 422: El servidor esta recibiendo la peticion sin embargo hay algun error que esta haciendo que la peticion sea improcesable.
- 200: OK (caso de exito)
