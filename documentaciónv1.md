# Arquitectura del Sistema – App Yogaterapy (v1)

El desarrollo de la versión 1 de **App Yogaterapy** se ha estructurado siguiendo el patrón de arquitectura **MVC (Modelo–Vista–Controlador)**, lo cual ha permitido separar de manera clara la lógica del negocio, la interfaz de usuario y el control de flujo de la aplicación.

---

## MODELO (Model)

La capa **Modelo** gestiona la lógica de negocio y el acceso a los datos. Se implementa mediante clases en **Python** utilizando **SQLAlchemy** para definir las entidades y relaciones de la base de datos.

### Entidades principales:

* **User**: Almacena los datos personales y el tipo de usuario (paciente o instructor).
* **Posture**: Representa cada postura terapéutica y su categoría según dolencia.
* **Series / SeriesPosture**: Controlan la estructura de una serie terapéutica y su relación con posturas.
* **Session**: Registra las sesiones realizadas por los pacientes, incluyendo comentarios de feedback.
* **TherapyType**: Define las dolencias o necesidades terapéuticas asociadas a posturas.

La conexión a la base de datos y su inicialización se centralizan en el archivo* `models/database.py`.

---

## VISTA (View)

La capa **Vista** está compuesta por archivos **HTML** que utilizan el motor de plantillas **Jinja2**, permitiendo generar contenido dinámico basado en los datos enviados desde los controladores.

### Vistas según tipo de usuario:

#### Paciente:

* dashboard.html: Vista principal con información resumida.
* execute_series.html: Visualiza paso a paso una serie con cronómetro.
* sessions.html: Historial de sesiones realizadas.
* start_session.html: Inicia una nueva sesión terapéutica.

#### Instructor:

* patients.html: Lista de pacientes registrados.
* add_patient.html, edit_patient.html: Formularios para gestión de pacientes.
* assign_series.html: Asignación de series a pacientes.
* create_series.html: Creación de series mediante selección de posturas.

#### Autenticación:

* login.html, register.html, logout.html: Control de acceso a la aplicación.


---

## CONTROLADOR (Controller)

La capa **Controlador** actúa como puente entre las acciones del usuario y la lógica del sistema. Se implementa principalmente en `routes/patient.py`, donde se definen rutas, validaciones y flujos para manejar la interacción del usuario.

Cada función del controlador responde a eventos HTTP (GET o POST), ejecutando operaciones y renderizando la vista adecuada.

---

### 1. Gestión de navegación basada en roles

El sistema identifica el tipo de usuario al iniciar sesión y redirige al dashboard correspondiente:

* **Pacientes**: Acceden a su panel de inicio para ejecutar series.
* **Instructores**: Gestionan pacientes, posturas y series.

Esto se controla mediante condicionales y sesiones de Flask.

---

### 2. Asignación de series terapéuticas (Instructor)

Ruta: **/assign_series**

Permite seleccionar un paciente y asignarle una serie. Antes de hacerlo:

* Si **no tiene serie activa**, se asigna directamente.
* Si **ya tiene una**, se solicita confirmación para reemplazarla.


---

### 3. Ejecución de series paso a paso (Paciente)

Ruta: **/execute_series**

* Se recuperan las posturas ordenadas de la serie asignada.
* Se guía al paciente con un cronómetro y navegación paso a paso.
* Se registra automáticamente una nueva Session en la base de datos.

---

### 4. Captura de feedback (Paciente)

Tras ejecutar una serie, el sistema redirige al formulario de retroalimentación.

* El controlador valida que el formulario sea completado antes de cerrar la sesión.
* Los datos se guardan y son accesibles por el instructor.


---

### 5. Gestión de pacientes (Instructor)

Rutas: **/add_patient, /edit_patient, /patients**

El instructor puede:

* Registrar nuevos pacientes.
* Editar su información.
* Ver su historial de sesiones.



---

### 6. Visualización del progreso del paciente

Rutas: **/patient_sessions, /view_series**

El instructor puede revisar:

* Total de sesiones completadas.
* Comentarios de feedback.
* Series asignadas y su estado.


---
