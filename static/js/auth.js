document.addEventListener('DOMContentLoaded', function () {
        const formulario = document.getElementById('formulario_registro');
        const campoContrasena = document.getElementById('contrasena');
        const campoConfirmarContrasena = document.getElementById('confirmar_contrasena');
        const barraFortaleza = document.getElementById('barra_fortaleza');
        const textoFortaleza = document.getElementById('texto_fortaleza');
        const botonEnviar = document.getElementById('boton_enviar');
        const debugStatus = document.getElementById('debug_status');

        // INICIALMENTE EL BOTÓN ESTÁ HABILITADO
        botonEnviar.disabled = false;
        debugStatus.textContent = 'Botón habilitado por defecto';

        // Alternar visibilidad de contraseña
        document.getElementById('alternar_contrasena').addEventListener('click', function () {
            alternarVisibilidadContrasena('contrasena', this);
        });

        document.getElementById('alternar_confirmacion').addEventListener('click', function () {
            alternarVisibilidadContrasena('confirmar_contrasena', this);
        });

        function alternarVisibilidadContrasena(idCampo, boton) {
            const campo = document.getElementById(idCampo);
            const tipo = campo.getAttribute('type') === 'password' ? 'text' : 'password';
            campo.setAttribute('type', tipo);
            boton.textContent = tipo === 'password' ? '👁️' : '🙈';
        }

        // Validación de fortaleza de contraseña
        campoContrasena.addEventListener('input', function () {
            const contrasena = this.value;
            const fortaleza = calcularFortalezaContrasena(contrasena);
            actualizarInterfazFortaleza(fortaleza);
            validarFormularioCompleto();
        });

        // Validación de confirmación de contraseña
        campoConfirmarContrasena.addEventListener('input', function () {
            validarCoincidenciaContrasenas();
            validarFormularioCompleto();
        });

        // Validaciones de otros campos
        document.getElementById('nombre_completo').addEventListener('input', validarNombre);
        document.getElementById('correo_electronico').addEventListener('input', validarCorreo);
        document.getElementById('nombre_usuario').addEventListener('input', validarNombreUsuario);

        function calcularFortalezaContrasena(contrasena) {
            let puntuacion = 0;
            const requisitos = {
                longitud: contrasena.length >= 8,
                mayuscula: /[A-Z]/.test(contrasena),
                minuscula: /[a-z]/.test(contrasena),
                numero: /\d/.test(contrasena),
                especial: /[@$!%*?&]/.test(contrasena)
            };

            // Actualizar indicadores de requisitos
            actualizarRequisito('req_longitud', requisitos.longitud);
            actualizarRequisito('req_mayuscula', requisitos.mayuscula);
            actualizarRequisito('req_minuscula', requisitos.minuscula);
            actualizarRequisito('req_numero', requisitos.numero);
            actualizarRequisito('req_especial', requisitos.especial);

            // Calcular puntuación
            Object.values(requisitos).forEach(req => {
                if (req) puntuacion++;
            });

            // Puntos bonus por longitud
            if (contrasena.length >= 12) puntuacion += 0.5;
            if (contrasena.length >= 16) puntuacion += 0.5;

            return {
                puntuacion: puntuacion,
                requisitos: requisitos,
                esValida: Object.values(requisitos).every(req => req)
            };
        }

        function actualizarRequisito(id, esValido) {
            const elemento = document.getElementById(id);
            elemento.className = `requisito_contrasena ${esValido ? 'valido' : 'invalido'}`;
        }

        function actualizarInterfazFortaleza(fortaleza) {
            const { puntuacion } = fortaleza;

            // Remover clases existentes
            barraFortaleza.className = 'barra_fortaleza_contrasena';

            if (puntuacion <= 2) {
                barraFortaleza.classList.add('fortaleza_debil');
                textoFortaleza.textContent = 'Contraseña débil';
                textoFortaleza.style.color = '#ef5350';
            } else if (puntuacion <= 3) {
                barraFortaleza.classList.add('fortaleza_regular');
                textoFortaleza.textContent = 'Contraseña regular';
                textoFortaleza.style.color = '#ff9800';
            } else if (puntuacion <= 4) {
                barraFortaleza.classList.add('fortaleza_buena');
                textoFortaleza.textContent = 'Contraseña buena';
                textoFortaleza.style.color = '#ffc107';
            } else {
                barraFortaleza.classList.add('fortaleza_fuerte');
                textoFortaleza.textContent = 'Contraseña fuerte';
                textoFortaleza.style.color = '#4caf50';
            }
        }

        function validarCoincidenciaContrasenas() {
            const contrasena = campoContrasena.value;
            const confirmacion = campoConfirmarContrasena.value;
            
            // Si no hay confirmación, no validar aún
            if (confirmacion.length === 0) {
                return true;
            }
            
            const esValida = contrasena === confirmacion;
            mostrarErrorCampo('confirmar_contrasena', !esValida, 'error_confirmacion');
            return esValida;
        }

        function validarNombre() {
            const nombre = document.getElementById('nombre_completo').value.trim();
            if (nombre.length === 0) return true; // No validar si está vacío
            
            const esValido = nombre.length >= 2 && nombre.length <= 120;
            mostrarErrorCampo('nombre_completo', !esValido, 'error_nombre');
            return esValido;
        }

        function validarCorreo() {
            const correo = document.getElementById('correo_electronico').value.trim();
            if (correo.length === 0) return true; // No validar si está vacío
            
            const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const esValido = regexCorreo.test(correo);
            mostrarErrorCampo('correo_electronico', !esValido, 'error_correo');
            return esValido;
        }

        function validarNombreUsuario() {
            const nombreUsuario = document.getElementById('nombre_usuario').value.trim();
            if (nombreUsuario.length === 0) return true; // No validar si está vacío
            
            const regexUsuario = /^[a-zA-Z0-9_]{3,20}$/;
            const esValido = regexUsuario.test(nombreUsuario);
            mostrarErrorCampo('nombre_usuario', !esValido, 'error_usuario');
            return esValido;
        }

        function mostrarErrorCampo(idCampo, tieneError, idError) {
            const campo = document.getElementById(idCampo);
            const grupoFormulario = campo.closest('.grupo_formulario');

            if (tieneError) {
                grupoFormulario.classList.add('con_error');
            } else {
                grupoFormulario.classList.remove('con_error');
            }
        }

        function validarFormularioCompleto() {
            const contrasena = campoContrasena.value;
            const confirmacion = campoConfirmarContrasena.value;
            const nombre = document.getElementById('nombre_completo').value.trim();
            const correo = document.getElementById('correo_electronico').value.trim();
            const usuario = document.getElementById('nombre_usuario').value.trim();
            
            // Calcular fortaleza de contraseña
            const fortaleza = calcularFortalezaContrasena(contrasena);
            
            // Validar cada campo individualmente
            const nombreValido = nombre.length >= 2 && nombre.length <= 120;
            const correoValido = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
            const usuarioValido = /^[a-zA-Z0-9_]{3,20}$/.test(usuario);
            const contrasenaValida = fortaleza.esValida;
            const confirmacionValida = contrasena === confirmacion && confirmacion.length > 0;
            
            // Todos los campos deben estar completos y ser válidos
            const formularioValido = nombreValido && correoValido && usuarioValido && contrasenaValida && confirmacionValida;
            
            // DEBUG: Mostrar estado
            debugStatus.innerHTML = `
                Nombre: ${nombreValido ? '✓' : '✗'} (${nombre.length}) |
                Email: ${correoValido ? '✓' : '✗'} |
                Usuario: ${usuarioValido ? '✓' : '✗'} (${usuario.length}) |
                Contraseña: ${contrasenaValida ? '✓' : '✗'} |
                Confirmación: ${confirmacionValida ? '✓' : '✗'} |
                <strong>Válido: ${formularioValido ? 'SÍ' : 'NO'}</strong>
            `;
            
            // Habilitar/deshabilitar botón
            botonEnviar.disabled = !formularioValido;
            
            if (formularioValido) {
                botonEnviar.classList.remove('btn-debug');
                debugStatus.style.color = '#4caf50';
            } else {
                botonEnviar.classList.add('btn-debug');
                debugStatus.style.color = '#ef5350';
            }
            
            // Mostrar errores de contraseña
            mostrarErrorCampo('contrasena', !contrasenaValida && contrasena.length > 0, 'error_contrasena');
            
            return formularioValido;
        }

        // Envío del formulario
        formulario.addEventListener('submit', function (e) {
            console.log('Formulario enviado');
            
            // Verificar una vez más antes de enviar
            const esValido = validarFormularioCompleto();
            
            if (!esValido) {
                console.log('Formulario no válido, previniendo envío');
                e.preventDefault();
                return false;
            }
            
            // Añadir indicador de carga
            botonEnviar.classList.add('cargando');
            botonEnviar.textContent = 'Registrando...';
            botonEnviar.disabled = true;
            
            console.log('Formulario válido, enviando...');
            return true;
        });
        
        // Validar formulario al cargar página
        setTimeout(() => {
            validarFormularioCompleto();
        }, 100);
    });