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

    // Mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', function() {
            mainNav.classList.toggle('active');
            menuToggle.classList.toggle('active');
            
            if (mainNav.classList.contains('active')) {
                mainNav.style.display = 'block';
            } else {
                setTimeout(() => {
                    mainNav.style.display = '';
                }, 300);
            }
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