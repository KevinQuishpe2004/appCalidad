# 🧘‍♀️ App YogaTherapy (v2)

**App YogaTherapy** es una plataforma web diseñada para facilitar la prescripción, ejecución y seguimiento de terapias de yoga personalizadas. Instructores pueden asignar series de posturas según el tipo de terapia, y los pacientes realizan sesiones guiadas con retroalimentación sobre su estado físico.

Proyecto desarrollado como parte de la asignatura de **Calidad de Software**.

---

## 🚀 Funcionalidades clave

- 📋 Registro de pacientes por parte del instructor
- 🧩 Asignación de **series terapéuticas** personalizadas
- ⏱️ Ejecución guiada de posturas con cronómetro
- 📈 Registro de sesiones con:
  - Nivel de dolor (inicio/fin)
  - Duración efectiva
  - Número de pausas
  - Comentarios
- 🔐 Autenticación con control de acceso por tipo de usuario (`Instructor` o `Paciente`)
- 📊 Dashboard con historial y progreso visual

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10**
- **Flask** (microframework web)
- **SQLAlchemy** (ORM)
- **HTML + CSS + JavaScript** (con templates Jinja2)
- **SQLite** (base de datos por defecto, puede migrarse)

---

## 👥 Roles y funcionalidades

| Rol        | Acciones habilitadas |
|------------|-----------------------|
| **Instructor** | Crear series, registrar pacientes, asignar series, ver sesiones de pacientes |
| **Paciente**   | Ver su serie asignada, ejecutar sesiones, registrar su nivel de dolor, revisar historial |

---

## 📂 Estructura del proyecto

          ├── models/ # Clases ORM y conexión a BD

          ├── routes/ # Lógica de control (controllers)

          ├── templates/ # Vistas HTML (Jinja2)

          ├── static/ # Archivos CSS y JS

          └── main.py # Punto de entrada de la app


---

## 🧪 Requisitos para ejecución local

1. **Tener instalado Python 3.10 o superior**

2. **Clonar el repositorio**
```bash
git clone https://github.com/KevinQuishpe2004/appCalidad.git
cd appCalidad
```
3. **Instalar las dependencias**
```bash
pip install -r requerimients.txt
```
4. Ejecutar la aplicación
```bash
python main.py
```
   

