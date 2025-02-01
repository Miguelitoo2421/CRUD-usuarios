#creacion bbdd
import sqlite3
import sys

import bcrypt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, \
    QMessageBox


def crear_base_datos():
    conexion = sqlite3.connect('usuarios.db') # busca la base de datos usuarios.db para hacer la conexión y si no la encuentra la crea
    cursor = conexion.cursor() # con esto vamos a interactuar con la base de datos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL UNIQUE
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
        cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone() # el resultado será uno ya que cada usuario es unico
        conexion.close()

        if resultado and bcrypt.checkpw(contrasena.encode(), resultado[0]):
            self.bienvenida = WelcomeForm()
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
        #SI NO HAY USUARIO O NO HAY CONTRASEÑA
        if not usuario or not contrasena: # nos saldrá mensaje para indicar que usuario y contraseña so pueden ser nulos
            QMessageBox.warning(self, "ERROR", "Todos los campos son obligatorios")
        else:
            # ENCRIPTAMOS CONTRASEÑA AÑADIENDO UN SALT ALEATORIO
            contrasenia_encriptada = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt())
            try:
                conexion = sqlite3.connect('usuarios.db')
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO usuarios(usuario, contrasena)  VALUES(?,?)", (usuario, contrasenia_encriptada))
                conexion.commit()
                conexion.close()
                QMessageBox.information(self, "Exito", "Usuario registrado")
                self.volver_login()
            except sqlite3.IntegrityError:
                QMessageBox.critical(self, "ERROR", "Usuario existente")

class WelcomeForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bienvenido')
        self.setGeometry(100, 100, 600, 400)



if __name__ == '__main__': # dentro de nuestro modulo llamamos a la función
    crear_base_datos()
    app = QApplication(sys.argv)
    ventana = RegisterForm()
    #ventana = LoginForm()
    #ventana = WelcomeForm()
    ventana.show()
    sys.exit(app.exec())

