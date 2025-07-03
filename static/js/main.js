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

    // Mobile menu toggle - VERSIÓN ACTUALIZADA
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        // Crear overlay dinámicamente
        const navOverlay = document.createElement('div');
        navOverlay.className = 'nav-overlay';
        document.body.appendChild(navOverlay);
        
        menuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mainNav.classList.toggle('active');
            navOverlay.classList.toggle('active');
            document.body.classList.toggle('no-scroll');
        });
        
        // Cerrar menú al hacer clic en overlay
        navOverlay.addEventListener('click', function() {
            menuToggle.classList.remove('active');
            mainNav.classList.remove('active');
            this.classList.remove('active');
            document.body.classList.remove('no-scroll');
        });
        
        // Cerrar menú al hacer clic en enlaces (opcional)
        mainNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                menuToggle.classList.remove('active');
                mainNav.classList.remove('active');
                navOverlay.classList.remove('active');
                document.body.classList.remove('no-scroll');
            });
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