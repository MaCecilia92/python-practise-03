import bcrypt

class Usuario:
    def __init__(self, nombre, apellido, email, password):
        self.nombre = nombre.capitalize()
        self.apellido = apellido.capitalize()
        self.email = email
        self.password_plano = password  # Guardamos sin encriptar
        self.password = self.hash_password(password)

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def verificar_password(self, password_plano):
        return bcrypt.checkpw(password_plano.encode("utf-8"), self.password.encode("utf-8"))

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "password": self.password,
            "password_plano": self.password_plano
        }

class Cliente(Usuario):
    def __init__(self, nombre, apellido, email, password, consumos=None):
        super().__init__(nombre, apellido, email, password)
        self.consumos = consumos or []

    def agregar_consumo(self, plato, monto):
        self.consumos.append({"plato": plato, "monto": monto})

    def to_dict(self):
        data = super().to_dict()
        data["consumos"] = self.consumos
        return data
