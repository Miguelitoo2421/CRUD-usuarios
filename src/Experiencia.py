#creacion bbdd
import sqlite3
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


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
        self.setGeometry(100, 100, 400, 400)


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
        main_layout.addWidget(login_button)

        #   boton para pasar a ventana de registro
        register_button = QPushButton('Registrar')
        main_layout.addWidget(register_button)

        # ESTABLECER EL LAYOUT PRINCIPAL
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        ## CONCLUSION:
        # main_layout --> es unicamente la primera ventana (layout/diseño) que organiza los widgets de la interfaz.
        # central_widget = ---> es ese widget donde se coloca el main_layout, y es el que realmente contiene los campos de usuario, contraseña y botones

class RegisterForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inicio de Sesion')
        self.setGeometry(100, 100, 400, 400)

        #   layout diseño en vertical
        main_layout = QVBoxLayout() # layout principal
        title = QLabel('Registro')
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

        #   boton para registro de usuario
        register_button = QPushButton('Registrar')
        main_layout.addWidget(register_button)

        #   boton para pasar a ventana de registro
        back_button = QPushButton('Iniciar sesion')
        main_layout.addWidget(back_button)

        # ESTABLECER EL LAYOUT PRINCIPAL
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)   #-----------------------> min 50:47

if __name__ == '__main__': # dentro de nuestro modulo llamamos a la función
    crear_base_datos()
    app = QApplication(sys.argv)
    ventana = LoginForm()
    ventana.show()
    sys.exit(app.exec())

