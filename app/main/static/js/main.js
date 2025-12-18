// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Плавная прокрутка для навигационных ссылок
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            window.scrollTo({
                top: targetSection.offsetTop - 80,
                behavior: 'smooth'
            });
        });
    });
    
    // Изменение стиля навигации при прокрутке
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        
        if (window.scrollY > 100) {
            navbar.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
            navbar.style.padding = '10px 0';
        } else {
            navbar.style.backgroundColor = 'rgba(0, 0, 0, 0.6)';
            navbar.style.padding = '10px 0';
        }
    });
    
    // Обработка форм
    const forms = document.querySelectorAll('.contact-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const messageElement = document.getElementById('formMessage');
            const submitButton = this.querySelector('button[type="submit"]');
            
            // Отключаем кнопку во время отправки
            submitButton.disabled = true;
            submitButton.style.opacity = '0.6';
            
            fetch('/submit-application/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                messageElement.style.display = 'block';
                
                if (data.success) {
                    messageElement.style.color = '#28a745';
                    messageElement.textContent = data.message;
                    form.reset();
                } else {
                    messageElement.style.color = '#dc3545';
                    messageElement.textContent = data.message;
                }
            })
            .catch(error => {
                messageElement.style.display = 'block';
                messageElement.style.color = '#dc3545';
                messageElement.textContent = 'Ошибка при отправке заявки. Попробуйте позже.';
                console.error('Error:', error);
            })
            .finally(() => {
                // Включаем кнопку обратно
                submitButton.disabled = false;
                submitButton.style.opacity = '1';
            });
        });
    });

    // Кнопки "Выбрать пакет" - прокрутка к контактам
    const outlineButtons = document.querySelectorAll('.btn-outline');
    
    outlineButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const contactSection = document.querySelector('#contact');
            
            window.scrollTo({
                top: contactSection.offsetTop - 80,
                behavior: 'smooth'
            });
        });
    });

    // Мобильное меню (гамбургер)
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('open');
            this.classList.toggle('active');
        });

        // Закрывать меню при клике на ссылку
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navMenu.classList.contains('open')) {
                    navMenu.classList.remove('open');
                    navToggle.classList.remove('active');
                }
            });
        });
    }
});

// Аккордеон с возможностью открытия нескольких элементов
document.addEventListener('DOMContentLoaded', function() {
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    
    accordionHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const accordionContent = this.nextElementSibling;
            const accordionIcon = this.querySelector('.accordion-icon');
            
            // Переключаем только текущий элемент
            this.classList.toggle('active');
            accordionContent.classList.toggle('open');
            
            // Динамически устанавливаем высоту
            if (accordionContent.classList.contains('open')) {
                accordionContent.style.maxHeight = accordionContent.scrollHeight + 'px';
            } else {
                accordionContent.style.maxHeight = '0';
            }
        });
    });
});