from clientes.cliente import Cliente
from clientes.operaciones import (
    cliente_existente, actualizar_cliente, eliminar_cliente, validar_input, validar_email, validar_password
)
import bcrypt
import json
from datetime import datetime

ARCHIVO = "clientes.json"

def calcular_total_consumos(clientes):
    total = 0
    for cliente in clientes:
        consumos = cliente.get("consumos", [])
        total += sum(c["monto"] for c in consumos)
    return total

def cargar_datos():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("clientes", []), data.get("total_consumos", 0)
    except FileNotFoundError:
        return [], 0

def guardar_datos(clientes):
    total_consumos = calcular_total_consumos(clientes)
    data = {
        "clientes": clientes,
        "total_consumos": total_consumos
    }
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def mostrar_menu_principal():
    print("\n--- Menú Principal ---")
    print("1. Agregar nuevo cliente")
    print("2. Actualizar cliente")
    print("3. Mostrar clientes")
    print("4. Eliminar cliente")
    print("5. Iniciar sesión")
    print("6. Salir")

def mostrar_menu_consumo():
    print("\n--- Menú de Consumo ---")
    print("1. Agregar consumos")
    print("2. Ver consumos")
    print("3. Cerrar sesión")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- Agregar cliente ---")
            clientes, _ = cargar_datos()
            nombre = validar_input("nombre")
            apellido = validar_input("apellido")
            email = validar_email(clientes)
            password = validar_password()

            cliente = Cliente(nombre, apellido, email, password)
            clientes.append(cliente.to_dict())
            guardar_datos(clientes)
            print("✅ Cliente agregado exitosamente.")

        elif opcion == "2":
            print("\n--- Actualizar cliente ---")
            clientes, _ = cargar_datos()
            email = validar_input("email")
            if not cliente_existente(clientes, email):
                print("❌ Cliente no encontrado.")
                continue

            nombre = validar_input("nuevo nombre")
            apellido = validar_input("nuevo apellido")
            password = validar_password()

            cliente = Cliente(nombre, apellido, email, password)
            if actualizar_cliente(clientes, cliente.to_dict()):
                guardar_datos(clientes)
                print("✅ Cliente actualizado exitosamente.")

        elif opcion == "3":
            print("\n--- Lista de Clientes ---")
            clientes, total_consumos = cargar_datos()
            for c in clientes:
                print(c)
            print(f"\nTotal consumos global: ${total_consumos}")

        elif opcion == "4":
            print("\n--- Eliminar cliente ---")
            clientes, _ = cargar_datos()
            email = validar_input("email del cliente a eliminar")
            if eliminar_cliente(clientes, email):
                guardar_datos(clientes)
                print("✅ Cliente eliminado.")

        elif opcion == "5":
            print("\n--- Iniciar sesión ---")
            clientes, _ = cargar_datos()
            email = validar_input("email")
            password = validar_input("contraseña")

            cliente_data = next((c for c in clientes if c["email"].lower() == email.lower()), None)

            if cliente_data and bcrypt.checkpw(password.encode("utf-8"), cliente_data["password"].encode("utf-8")):
                print(f"✅ Bienvenido {cliente_data['nombre']} {cliente_data['apellido']}!")

                cliente_obj = Cliente(
                    cliente_data["nombre"],
                    cliente_data["apellido"],
                    cliente_data["email"],
                    cliente_data["password_plano"],
                    cliente_data.get("consumos", [])
                )

                while True:
                    mostrar_menu_consumo()
                    op_cons = input("Seleccione opción: ")

                    if op_cons == "1":
                        print("\n--- Agregar consumos ---")
                        platos = [
                            {"plato": "Pizza", "precio": 12000},
                            {"plato": "Hamburguesa", "precio": 1500},
                            {"plato": "Ensalada", "precio": 800},
                            {"plato": "Bebida", "precio": 500},
                            {"plato": "Postre", "precio": 900},
                        ]

                        print("Opciones de platos:")
                        for i, p in enumerate(platos, start=1):
                            print(f"{i}. {p['plato']} - ${p['precio']}")

                        print("Ingrese los números de los platos que desea agregar separados por coma (ejemplo: 1,3,5), o '0' para cancelar:")
                        seleccion = input("> ").strip()

                        if seleccion == "0":
                            print("No se agregaron consumos.")
                            continue

                        indices = seleccion.split(",")
                        validos = []
                        for ind in indices:
                            ind = ind.strip()
                            if ind.isdigit():
                                num = int(ind)
                                if 1 <= num <= len(platos):
                                    validos.append(num)
                                else:
                                    print(f"⚠️ Número fuera de rango ignorado: {ind}")
                            else:
                                print(f"⚠️ Entrada inválida ignorada: {ind}")

                        if not validos:
                            print("❌ No se seleccionaron platos válidos.")
                            continue

                        for idx in validos:
                            plato_sel = platos[idx-1]
                            cliente_obj.agregar_consumo(plato_sel["plato"], plato_sel["precio"])
                            cliente_obj.consumos[-1]["fecha"] = datetime.now().strftime("%Y-%m-%d")

                        if actualizar_cliente(clientes, cliente_obj.to_dict()):
                            guardar_datos(clientes)
                            print(f"✅ Se agregaron {len(validos)} consumos.")

                    elif op_cons == "2":
                        print("\n--- Ver consumos ---")
                        if not cliente_obj.consumos:
                            print("No hay consumos registrados.")
                            continue

                        print("¿Querés filtrar por fecha? (formato YYYY-MM-DD). Dejá vacío para ver todos.")
                        fecha_filtro = input("Fecha: ").strip()

                        total = 0
                        encontrados = 0

                        for c in cliente_obj.consumos:
                            if not fecha_filtro or c.get("fecha") == fecha_filtro:
                                print(f"{c.get('fecha', 'Sin fecha')} - {c['plato']} - ${c['monto']}")
                                total += c["monto"]
                                encontrados += 1

                        if encontrados:
                            print(f"\nTotal consumido en esta vista: ${total}")
                        else:
                            print("❌ No se encontraron consumos para esa fecha.")

                    elif op_cons == "3":
                        print("Cerrando sesión...")
                        break

                    else:
                        print("❌ Opción inválida.")

            else:
                print("❌ Email o contraseña incorrectos.")

        elif opcion == "6":
            print("👋 Saliendo del programa.")
            break

        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()