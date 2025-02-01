#creacion bbdd
import sqlite3
import sys
from base64 import b64encode

import bcrypt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, \
    QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QCheckBox


def crear_base_datos():
    conexion = sqlite3.connect('usuarios.db') # busca la base de datos usuarios.db para hacer la conexión y si no la encuentra la crea
    cursor = conexion.cursor() # con esto vamos a interactuar con la base de datos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL UNIQUE,
        es_admin INTEGER NOT NULL DEFAULT 0
    )
    ''')
    conexion.commit() # hacemos el cambio dentro de la base de datos
    conexion.close() # cerramos conexión

    # por cada interfaz tendremos una clase

class LoginForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inicio de Sesion')
        self.setGeometry(100, 100, 300, 250)


        #   layout diseño en vertical
        main_layout = QVBoxLayout() # layout principal
        title = QLabel('Inicio de Sesion')
        main_layout.addWidget(title)

        #   Entrada de texto para usuario
        self.username_imput = QLineEdit(self)
        self.username_imput.setPlaceholderText("Nombre de usuario")
        main_layout.addWidget(self.username_imput)

        #   entrada texto para contraseña
        self.password_imput = QLineEdit(self)
        self.password_imput.setPlaceholderText("Contraseña")
        #ocultamos la contraseña escrita por seguridad
        self.password_imput.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.password_imput)

        #   boton para inicio de sesion
        login_button = QPushButton('Inicio de Sesion')
        login_button.clicked.connect(self.iniciar_sesion)
        main_layout.addWidget(login_button)


        #   BOTON PARA PASAR A LA VENTANA DE REGISTRO
        register_button = QPushButton('Registrar')
        register_button.clicked.connect(self.volver_registro)
        main_layout.addWidget(register_button)

        # ESTABLECER EL LAYOUT PRINCIPAL
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        ## CONCLUSION:
        # main_layout --> es unicamente la primera ventana (layout/diseño) que organiza los widgets de la interfaz.
        # central_widget = ---> es ese widget donde se coloca el main_layout, y es el que realmente contiene los campos de usuario, contraseña y botones

    def volver_registro(self):
        self.login = RegisterForm()
        self.login.show()
        self.close()

    def iniciar_sesion(self):
        usuario = self.username_imput.text()
        contrasena = self.password_imput.text()

        if not usuario or not contrasena:
            QMessageBox.warning(self, "ERROR", "Todos los campos son obligatorios")

        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()
        # seleccioname todo de usuarios donde usuario sea = a usuario
        cursor.execute("SELECT contrasena, es_admin FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone() # el resultado será uno ya que cada usuario es unico
        conexion.close()

        if resultado and bcrypt.checkpw(contrasena.encode(), resultado[0]):
            self.bienvenida = WelcomeForm(usuario, resultado[1]) # IMPORTANTE, ESTE USUARIO NOS LO LLEVAMOS A WelcomeForm para disponer de el
            self.bienvenida.show()
            self.close()
        else:
            QMessageBox.critical(self, "ERROR", "Usuario o contraseña incorrectos")
            self.username_imput.clear()
            self.password_imput.clear()

class RegisterForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inicio de Sesion')
        self.setGeometry(100, 100, 300, 250)

        #   LAYAUT DISEÑO PRINCIPAL
        main_layout = QVBoxLayout() # layout principal
        title = QLabel('Registro')
        main_layout.addWidget(title)

        #   ENTRADA DE TEXTO PARA USUARIO
        self.username_imput = QLineEdit(self)
        self.username_imput.setPlaceholderText("Nombre de usuario")
        main_layout.addWidget(self.username_imput)

        #   ENTRADA DE TEXTO PARA CONTRASEÑA
        self.password_imput = QLineEdit(self)
        self.password_imput.setPlaceholderText("Contraseña")
        #ocultamos la contraseña escrita por seguridad
        self.password_imput.setEchoMode(QLineEdit.Password)
        main_layout.addWidget(self.password_imput)

        # CHECK BOX PARA MARCAR SI EL USUARIO ES ADMINISTRADOR
        self.admin_checkbox = QCheckBox('¿Es Administrador?')
        main_layout.addWidget(self.admin_checkbox)


        #   BOTON PARA REGISTRO DE USUARIO
        register_button = QPushButton('Registrar')
        register_button.clicked.connect(self.registrar_usuario) #IMPORTANTE, SE COLOCA registrar_usuario SIN () PARA QUE SE EJECUTE EN RESPUESTA A LA SEÑAL DEL BOTON, SI LO COLOCAMOS CON () LA LLAMAMOS INMEDIATAMENTE
        main_layout.addWidget(register_button)

        #   BOTON PARA PASAR A VENTANA LOGIN(INICIO DE SESION)
        back_button = QPushButton('Iniciar sesion')
        back_button.clicked.connect(self.volver_login)
        main_layout.addWidget(back_button)

        # ESTABLECER EL LAYOUT PRINCIPAL
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # FUNCION QUE NOS LLEVA A LA VENTANA DE LOGIN Y CIERRA EN LA QUE ESTABAMOS
    def volver_login(self):
        self.login = LoginForm()
        self.login.show()
        self.close()

    # FUNCION PARA REGISTRO DE USUARIO
    def registrar_usuario(self):
        usuario = self.username_imput.text()
        contrasena = self.password_imput.text()
        es_admin = 1 if self.admin_checkbox.isChecked() else 0

        #SI NO HAY USUARIO O NO HAY CONTRASEÑA
        if not usuario or not contrasena: # nos saldrá mensaje para indicar que usuario y contraseña so pueden ser nulos
            QMessageBox.warning(self, "ERROR", "Todos los campos son obligatorios")
        else:
            # ENCRIPTAMOS CONTRASEÑA AÑADIENDO UN SALT ALEATORIO
            contrasenia_encriptada = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
            try:
                conexion = sqlite3.connect('usuarios.db')
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO usuarios(usuario, contrasena,es_admin)  VALUES(?,?,?)", (usuario, contrasenia_encriptada, es_admin))
                conexion.commit()
                conexion.close()
                QMessageBox.information(self, "Exito", "Usuario registrado")
                self.volver_login()
            except sqlite3.IntegrityError:
                QMessageBox.critical(self, "ERROR", "Usuario existente")

class WelcomeForm(QMainWindow):
    def __init__(self, usuario, es_admin): # este es el usuario que recibimos de la vista LoginForm
        super().__init__()
        self.setWindowTitle('Bienvenido')
        self.setGeometry(100, 100, 600, 400)

        self.usuario = usuario
        self.es_admin = es_admin

        # LAYOUT PRINCIPAL
        main_layout = QVBoxLayout()

        # ETIQUETA PRINCIPAL
        self.welcome_label = QLabel(f'¡Bienvenido,{usuario}!')
        main_layout.addWidget(self.welcome_label)

        # PINTAR TABLA
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Usuario", "Contraseña Encriptada"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows) # al clicar en una selda se selecciona toda la fila
        main_layout.addWidget(self.table)
        self.cargar_usuarios()

        if es_admin == 1:
            # BOTON PARA ELIMINAR CUENTA
            delele_button = QPushButton('Eliminar')
            delele_button.clicked.connect(self.borrar_cuenta)
            main_layout.addWidget(delele_button)

        cerrar_session = QPushButton('Cerrar sesión')
        cerrar_session.clicked.connect(lambda: self.close())
        main_layout.addWidget(cerrar_session)

        # Se crea un widget contenedor (QWidget), que servirá como el contenedor principal de la ventana.
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    #
    def cargar_usuarios(self):
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT usuario, contrasena FROM usuarios") # obtenemos todos los usuarios y contraseñas
        usuarios = cursor.fetchall() #  recupera todos los registros como una lista de tuplas, donde cada tupla es un usuario con su contraseña.
        conexion.close()
        self.table.setRowCount(len(usuarios)) # creamos tabla y le decimos que el numero de filas será la cantidad de usuarios recuperados

        for row, (usuario, contrasena) in enumerate(usuarios):
            self.table.setItem(row, 0, QTableWidgetItem(usuario))
            contrasenia_legible = b64encode(contrasena).decode("utf-8")
            self.table.setItem(row, 1, QTableWidgetItem(contrasenia_legible))


    def borrar_cuenta(self):
        selected_row = self.table.currentRow() #identificamos fila
        if selected_row == -1:
            QMessageBox.warning(self, "ERROR", "Debe seleccionar cuenta para eliminar")
            return

        usuario = self.table.item(selected_row, 0).text()

        if usuario != self.usuario:  # Verificar si el usuario seleccionado es el mismo que el usuario logueado
            QMessageBox.warning(self, "ERROR", "Solo puedes eliminar tu propio usuario")
            return

        respuesta = QMessageBox.question(  # Preguntar confirmación
            self,
            "Confirmar",
            f"¿Está seguro de borrar el usuario '{usuario}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            conexion = sqlite3.connect('usuarios.db')
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario,))
            conexion.commit()
            conexion.close()
            QMessageBox.information(self, "Exito", "Usuario borrado correctamente")
            self.cargar_usuarios()  # Recargar la lista de usuarios

            # COMO SOLO HEMOS CONFIGURADO ELIMINAR NUESTRO PROPIO USUARIO, DESPUES DE HACERLO EL PROGRAMA NOS LLEVA A LA VISTA LoginForm
            self.login = LoginForm()
            self.login.show()
            self.close()




if __name__ == '__main__': # dentro de nuestro modulo llamamos a la función
    crear_base_datos()
    app = QApplication(sys.argv)
    ventana = RegisterForm()
    #ventana = LoginForm()
    #ventana = WelcomeForm()
    ventana.show()
    sys.exit(app.exec())

