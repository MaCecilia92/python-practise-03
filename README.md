# 📘 Sistema de Gestión de Clientes

Este proyecto permite gestionar clientes, almacenar sus datos y registrar consumos asociados.  
Los datos se guardan en un archivo JSON para su persistencia.

---

## 🛠 Funcionalidades

### Gestión de Clientes
- ✅ Agregar nuevo cliente  
- ✅ Actualizar cliente existente  
- ✅ Eliminar cliente  
- ✅ Listar clientes con sus datos  
- ✅ Total global de consumos acumulados  

### Sistema de Autenticación
- 🔐 Iniciar sesión con email y contraseña  
- 🔐 Verificación de contraseña con hash seguro (bcrypt)  

### Gestión de Consumos
- 🍽 Agregar consumos desde un listado de platos disponibles  
- 📄 Ver lista de consumos por cliente autenticado  
- 💰 Ver el total de consumos personales  
- 📊 Ver el total global de consumos acumulados entre todos los clientes  
- 📆 **Nuevo:** Ver consumos agrupados por fecha  

### 🧪 Validaciones
- Verificación de formato de email  
- Validación de contraseña con requisitos mínimos  
- Validación de entradas en menús  

---

## 💾 Persistencia

Los datos de clientes y consumos se guardan en un archivo `clientes.json`.

El archivo incluye:  
- Lista de clientes  
- Contraseña en hash y en texto plano (para propósitos educativos)  
- Consumos por cliente  
- Total de consumos global  

---

## 🧱 Estructura del JSON

```json
{
  "clientes": [
    {
      "nombre": "Juan",
      "apellido": "Pérez",
      "email": "juan@example.com",
      "password": "$2b$12$...",
      "password_plano": "123456",
      "consumos": [
        {
          "plato": "Pizza",
          "monto": 1200,
          "fecha": "2025-06-09"
        },
        {
          "plato": "Bebida",
          "monto": 500,
          "fecha": "2025-06-09"
        }
      ]
    }
  ],
  "total_consumos": 1700
}

Paquete bcrypt:

pip install bcrypt
