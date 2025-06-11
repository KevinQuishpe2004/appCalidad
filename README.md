# App Yogaterapy (v1) 

Aplicación web desarrollada para facilitar la gestión de terapias de yoga personalizadas entre instructores y pacientes. Proyecto realizado como parte de la asignatura de Calidad de Software.

---

## Características principales

- Asignación de series terapéuticas a pacientes.
- Ejecución guiada paso a paso de series con cronómetro.
- Registro de sesiones y feedback del paciente.
- Gestión de pacientes y visualización de su progreso.
- Control de acceso por tipo de usuario (instructor o paciente).

---

## Tecnologías utilizadas

- Python 3.10
- Flask
- SQLAlchemy
- HTML + CSS (Jinja2 templates)
- SQLite

---

## Integrantes del equipo (Team QualiDepv)

- Oscar Tumbaco – Tester  
- Kevin Quishpe – Desarrollador  
- Juan Naranjo – Tester  
- Sebastián Sánchez – Analista  
- Cesar Pantoja – Desarrollador  

---

## Estructura del proyecto

appCalidad/

              ├── models/ # Clases ORM y conexión a BD

              ├── routes/ # Lógica de control (controllers)

              ├── templates/ # Vistas HTML (Jinja2)
    
              ├── static/ # Archivos CSS y JS

              └── main.py # Punto de entrada de la app


---

## Documentación

> 📄 Puedes consultar la documentación técnica completa aquí:  
> [`DOCUMENTACION_V1.md`](documentaciónv1.md)  

---

## Requisitos para ejecución local

1. **Tener instalado Python 3.10 o superior**  

2. **Clonar el repositorio**

3. **Instalar dependencias**
  pip install -r requerimientos.txt

4. **Ejecutar la aplicación**
  python app.py