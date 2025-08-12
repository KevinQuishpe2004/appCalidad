# 🧘‍♀️ App YogaTherapy (v3)

**App YogaTherapy** es una plataforma web diseñada para facilitar la prescripción, ejecución y seguimiento de terapias de yoga personalizadas.  
Los instructores pueden asignar series de posturas según el tipo de terapia, y los pacientes realizan sesiones guiadas con retroalimentación sobre su estado físico.

Proyecto desarrollado como parte de la asignatura de **Calidad de Software**.

---

## 📜 Criterios de uso operativo
- Uso exclusivo por terapeutas/instructores certificados y pacientes registrados.
- La información registrada debe ser veraz y actualizada.
- Cumplir con las políticas de privacidad y manejo de datos personales.

---

## 🖥️ Entorno operativo requerido
- **Sistema operativo:** Windows 10+, macOS 11+, o Linux (distros basadas en Debian).
- **Navegador recomendado:** Google Chrome (v110+) o Mozilla Firefox (v102+).
- **Conexión a Internet:** mínima de 5 Mbps.
- **Hardware:** procesador de 2 GHz, 4 GB RAM, pantalla mínima 1280x720.

---

## 🧩 Herramientas y materiales de apoyo
- Guía de usuario en PDF (incluida en `/docs/guia_usuario.pdf`).
- Manual técnico para administradores.
- Video explicativo (ver sección **🎥 Video guía**).

---

## ⚠️ Advertencias de seguridad
- No compartir credenciales de acceso.
- Cerrar sesión al finalizar el uso.
- Evitar el uso en dispositivos públicos o no seguros.
- Respetar la Ley de Protección de Datos Personales vigente.

---

## 🚀 Funcionalidades clave
- 📋 Registro de pacientes por parte del instructor.
- 🧩 Asignación de **series terapéuticas** personalizadas.
- ⏱️ Ejecución guiada de posturas con cronómetro.
- 📈 Registro de sesiones con:
  - Nivel de dolor (inicio/fin).
  - Duración efectiva.
  - Número de pausas.
  - Comentarios.
- 🔐 Autenticación con control de acceso por tipo de usuario (`Instructor` o `Paciente`).
- 📊 Dashboard con historial y progreso visual.

---

## 👥 Roles y funcionalidades
| Rol        | Acciones habilitadas |
|------------|-----------------------|
| **Instructor** | Crear series, registrar pacientes, asignar series, ver sesiones de pacientes |
| **Paciente**   | Ver su serie asignada, ejecutar sesiones, registrar su nivel de dolor, revisar historial |

---

## 📂 Estructura del proyecto

📂 instance/ → Configuración y datos locales fuera de control de versiones
📂 models/ → Definiciones de entidades y estructuras de datos
📂 routes/ → Controladores y rutas de la aplicación
📂 static/ → Archivos estáticos (imágenes, CSS, JS)
📂 templates/ → Plantillas HTML para la interfaz
📄 .gitignore → Archivos/carpetas ignorados por Git
📄 .runtime.txt → Versión de Python para ejecución
📄 app.py → Punto de entrada principal
📄 documentaciónv3.md → Documentación de esta versión
📄 Procfile → Configuración de despliegue en Heroku u otros
📄 README.md → Descripción general del proyecto
📄 requirements.txt → Lista de dependencias necesarias

## 5. Instrucciones de Instalación y Ejecución

### Requisitos Previos
- Python 3.x
- pip
- Git

### Instalación
```bash
# Clonar repositorio
git clone [URL del repositorio]
cd [carpeta del proyecto]

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```




