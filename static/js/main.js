document.addEventListener('DOMContentLoaded', function() {
    // Flash message dismissal
    const closeButtons = document.querySelectorAll('.close-flash');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const flash = this.parentElement;
            flash.style.opacity = '0';
            setTimeout(() => {
                flash.style.display = 'none';
            }, 300);
        });
    });

    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        document.querySelectorAll('.flash').forEach(flash => {
            flash.style.opacity = '0';
            setTimeout(() => {
                flash.style.display = 'none';
            }, 300);
        });
    }, 5000);

    // Mobile menu toggle - VERSIÓN MEJORADA Y RESPONSIVE
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        // Buscar overlay existente o crear uno nuevo
        let navOverlay = document.querySelector('.overlay');
        if (!navOverlay) {
            navOverlay = document.createElement('div');
            navOverlay.className = 'overlay';
            document.body.appendChild(navOverlay);
        }
        
        // Función para abrir menú
        function openMenu() {
            menuToggle.classList.add('active');
            mainNav.classList.add('active');
            navOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
        
        // Función para cerrar menú
        function closeMenu() {
            menuToggle.classList.remove('active');
            mainNav.classList.remove('active');
            navOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }
        
        // Toggle menú al hacer clic en el botón hamburguesa
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (mainNav.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        });
        
        // Cerrar menú al hacer clic en overlay
        navOverlay.addEventListener('click', closeMenu);
        
        // Cerrar menú al hacer clic en enlaces
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                // Solo cerrar en móvil
                if (window.innerWidth <= 768) {
                    closeMenu();
                }
            });
        });
        
        // Cerrar menú al cambiar tamaño de ventana (si pasa a desktop)
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                closeMenu();
            }
        });
        
        // Cerrar menú con tecla ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && mainNav.classList.contains('active')) {
                closeMenu();
            }
        });
        
        // Prevenir propagación de clics dentro del nav
        mainNav.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    // Function to convert newlines to <br> tags
    function nl2br(str) {
        return str.replace(/\n/g, '<br>');
    }
    
    // Apply nl2br to elements with the class 'nl2br'
    document.querySelectorAll('.nl2br').forEach(element => {
        element.innerHTML = nl2br(element.textContent);
    });
});