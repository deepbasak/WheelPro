// OnyxForged - Modern Premium Wheel Store JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add a class to body when page is fully loaded for fade-in animations
    document.body.classList.add('page-loaded');

    // Add animation classes to elements as they appear in viewport
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('visible');
            }
        });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll();

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Product image lazy loading
    var images = document.querySelectorAll('img[data-src]');
    var imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(function(img) {
        imageObserver.observe(img);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Removed auto-refresh functionality to prevent interruption of admin forms

    // Enhanced product card and feature card interactions with staggered animations
    var productCards = document.querySelectorAll('.product-card');
    productCards.forEach(function(card, index) {
        // Add animation classes with staggered delays
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
        
        // Mouse interactions
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Feature card animations
    var featureCards = document.querySelectorAll('.feature-icon');
    featureCards.forEach(function(card, index) {
        setTimeout(() => {
            card.classList.add('animate-pulse');
        }, 200 * (index + 1));
    });

    // File upload preview
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var preview = document.getElementById('imagePreview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'imagePreview';
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        input.parentNode.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Quote form enhancements
    var quoteForm = document.querySelector('form[action*="quote"]');
    if (quoteForm) {
        // Auto-format phone number
        var phoneInput = quoteForm.querySelector('input[name="phone"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', function() {
                var value = this.value.replace(/\D/g, '');
                if (value.length >= 6) {
                    value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
                }
                this.value = value;
            });
        }

        // Vehicle year and make dependency
        var vehicleMake = quoteForm.querySelector('select[name="vehicle_make"]');
        var vehicleYear = quoteForm.querySelector('select[name="vehicle_year"]');
        if (vehicleMake && vehicleYear) {
            vehicleMake.addEventListener('change', function() {
                // Could add model suggestions based on make/year in the future
                console.log('Selected make:', this.value);
            });
        }
    }

    // Admin dashboard enhancements
    if (window.location.pathname.includes('/admin/dashboard')) {
        // Auto-update statistics
        var statCards = document.querySelectorAll('.card[class*="bg-"]');
        statCards.forEach(function(card) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', function() {
                // Add click animations or navigation
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            });
        });
    }

    // Search functionality (if needed in the future)
    var searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            var searchTerm = this.value.toLowerCase();
            var productCards = document.querySelectorAll('.product-card');
            
            productCards.forEach(function(card) {
                var productName = card.querySelector('.card-title').textContent.toLowerCase();
                var productDesc = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (productName.includes(searchTerm) || productDesc.includes(searchTerm)) {
                    card.parentElement.style.display = 'block';
                } else {
                    card.parentElement.style.display = 'none';
                }
            });
        });
    }

    // Disable loading states for form buttons to prevent processing issues
    // Forms will handle their own submission feedback

    // Confirmation dialogs for delete actions
    var deleteLinks = document.querySelectorAll('a[href*="delete"]');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Custom cursor effect for modern UI
    const cursor = document.getElementById('cursor');
    if (cursor) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });
        
        // Change cursor size on hoverable elements
        const hoverableElements = document.querySelectorAll('a, button, .btn, .card');
        hoverableElements.forEach(element => {
            element.addEventListener('mouseenter', () => {
                cursor.style.width = '40px';
                cursor.style.height = '40px';
                cursor.style.borderColor = 'var(--accent-color)';
                cursor.style.backgroundColor = 'rgba(255, 60, 48, 0.1)';
            });
            
            element.addEventListener('mouseleave', () => {
                cursor.style.width = '20px';
                cursor.style.height = '20px';
                cursor.style.borderColor = 'var(--primary-color)';
                cursor.style.backgroundColor = 'transparent';
            });
        });
    }

    console.log('Premium Rim Store - JavaScript initialized successfully!');
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).format(new Date(date));
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // Could send error reports to server in production
});

// Performance monitoring
window.addEventListener('load', function() {
    var loadTime = window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart;
    console.log('Page load time:', loadTime + 'ms');
});
