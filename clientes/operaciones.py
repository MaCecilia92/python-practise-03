import json
import re
import os

RUTA_ARCHIVO = "clientes.json"

def cargar_clientes():
    if not os.path.exists(RUTA_ARCHIVO):
        return []
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_clientes(clientes):
    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)

def cliente_existente(clientes, email):
    return any(c["email"].lower() == email.lower() for c in clientes)

def actualizar_cliente(clientes, cliente_actualizado):
    for i, c in enumerate(clientes):
        if c["email"].lower() == cliente_actualizado["email"].lower():
            clientes[i] = cliente_actualizado
            return True
    return False

def eliminar_cliente(clientes, email):
    for i, c in enumerate(clientes):
        if c["email"].lower() == email.lower():
            clientes.pop(i)
            print(f"✅ Cliente con email {email} eliminado.")
            return True
    print(f"❌ No se encontró cliente con email {email}.")
    return False

def validar_input(campo):
    while True:
        valor = input(f"Ingrese {campo}: ").strip()
        if valor:
            return valor
        else:
            print(f"❌ El campo {campo} no puede estar vacío.")

def validar_email(clientes):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    while True:
        email = input("Ingrese email: ").strip()
        if not re.match(pattern, email):
            print("❌ Email inválido. Intente de nuevo.")
            continue
        if any(c["email"].lower() == email.lower() for c in clientes):
            print("❌ Email ya registrado. Intente con otro.")
            continue
        return email

def validar_password():
    while True:
        password = input("Ingrese contraseña (mínimo 4 caracteres): ").strip()
        if len(password) < 4:
            print("❌ La contraseña debe tener al menos 4 caracteres.")
        else:
            return password