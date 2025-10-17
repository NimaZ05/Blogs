// Enhanced Blog Features JavaScript
class BlogEnhancements {
    constructor() {
        this.init();
    }

    init() {
        this.setupScrollAnimations();
        this.setupImageLightbox();
        this.setupToastNotifications();
        this.setupEnhancedSearch();
        this.setupSocialSharing();
        this.setupLazyLoading();   
        this.setupSkeletonHandling();
        this.setupTouchGestures();
        this.setupFormEnhancements();
        this.setupAccessibility();
    }

    // Scroll-triggered animations
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe all elements with animate-on-scroll class
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });

        // Add staggered animation to post cards
        document.querySelectorAll('.post-row').forEach((el, index) => {
            el.style.animationDelay = `${index * 0.1}s`;
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
    }

    // Image lightbox modal
    setupImageLightbox() {
        // Create modal if it doesn't exist
        if (!document.getElementById('image-modal')) {
            const modal = document.createElement('div');
            modal.id = 'image-modal';
            modal.className = 'modal';
            modal.innerHTML = `
                <span class="modal-close">&times;</span>
                <img class="modal-content" id="modal-image">
            `;
            document.body.appendChild(modal);
        }

        const modal = document.getElementById('image-modal');
        const modalImg = document.getElementById('modal-image');
        const closeBtn = document.querySelector('.modal-close');

        // Add click handlers to all images
        document.querySelectorAll('img').forEach(img => {
            img.style.cursor = 'pointer';
            img.addEventListener('click', () => {
                modal.style.display = 'block';
                modalImg.src = img.src;
                modalImg.alt = img.alt;
                document.body.style.overflow = 'hidden';
            });
        });

        // Close modal handlers
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });

        // ESC key to close
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.style.display === 'block') {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        });
    }

    // Toast notification system
    setupToastNotifications() {
        // Create toast container if it doesn't exist
        if (!document.getElementById('toast-container')) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
    }

    showToast(message, type = 'info', duration = 5000) {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icon = this.getToastIcon(type);
        toast.innerHTML = `
            <div class="toast-icon">${icon}</div>
            <div class="toast-message">${message}</div>
            <button class="toast-close">&times;</button>
        `;

        container.appendChild(toast);

        // Auto remove after duration
        setTimeout(() => {
            this.removeToast(toast);
        }, duration);

        // Manual close
        toast.querySelector('.toast-close').addEventListener('click', () => {
            this.removeToast(toast);
        });

        return toast;
    }

    removeToast(toast) {
        toast.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    getToastIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    }


    // Enhanced search with debouncing
    setupEnhancedSearch() {
        const searchInput = document.querySelector('input[name="search"]');
        if (!searchInput) return;

        let searchTimeout;
        const searchBar = searchInput.closest('.search-bar');
        
        // Create suggestions container
        const suggestions = document.createElement('div');
        suggestions.className = 'search-suggestions';
        searchBar.appendChild(suggestions);

        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const query = e.target.value.trim();
            
            if (query.length < 2) {
                suggestions.style.display = 'none';
                return;
            }

            searchTimeout = setTimeout(() => {
                this.performSearch(query, suggestions);
            }, 300);
        });

        // Hide suggestions when clicking outside
        document.addEventListener('click', (e) => {
            if (!searchBar.contains(e.target)) {
                suggestions.style.display = 'none';
            }
        });
    }

    async performSearch(query, suggestionsContainer) {
        try {
            // This would typically make an AJAX request to your Django backend
            // For now, we'll simulate with local content
            const suggestions = this.getLocalSuggestions(query);
            this.displaySuggestions(suggestions, suggestionsContainer);
        } catch (error) {
            console.error('Search error:', error);
        }
    }

    getLocalSuggestions(query) {
        // This would be replaced with actual AJAX search
        const allTitles = Array.from(document.querySelectorAll('h2, h3')).map(h => h.textContent);
        return allTitles.filter(title => 
            title.toLowerCase().includes(query.toLowerCase())
        ).slice(0, 5);
    }

    displaySuggestions(suggestions, container) {
        container.innerHTML = '';
        
        if (suggestions.length === 0) {
            container.style.display = 'none';
            return;
        }

        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'search-suggestion';
            item.textContent = suggestion;
            item.addEventListener('click', () => {
                document.querySelector('input[name="search"]').value = suggestion;
                container.style.display = 'none';
                // Trigger search
                document.querySelector('.search-bar form').submit();
            });
            container.appendChild(item);
        });

        container.style.display = 'block';
    }

    // Social sharing functionality
    setupSocialSharing() {
        // Add social sharing to post pages
        const postContent = document.querySelector('.post-body');
        if (postContent) {
            const shareButtons = document.createElement('div');
            shareButtons.className = 'social-share';
            shareButtons.innerHTML = `
                <button class="share-btn twitter" data-platform="twitter">Twitter</button>
                <button class="share-btn linkedin" data-platform="linkedin">LinkedIn</button>
                <button class="share-btn facebook" data-platform="facebook">Facebook</button>
                <button class="share-btn copy" data-platform="copy">Copy Link</button>
            `;
            
            postContent.appendChild(shareButtons);

            shareButtons.addEventListener('click', (e) => {
                if (e.target.classList.contains('share-btn')) {
                    this.sharePost(e.target.dataset.platform);
                }
            });
        }
    }

    sharePost(platform) {
        const url = window.location.href;
        const title = document.title;
        const text = document.querySelector('.post-intro')?.textContent || title;

        switch (platform) {
            case 'twitter':
                window.open(`https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`);
                break;
            case 'linkedin':
                window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`);
                break;
            case 'facebook':
                window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`);
                break;
            case 'copy':
                navigator.clipboard.writeText(url).then(() => {
                    this.showToast('Link copied to clipboard!', 'success');
                });
                break;
        }
    }

    // Lazy loading for images
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    // Skeleton removal when images/text load
    setupSkeletonHandling() {
        const containers = document.querySelectorAll('.skeleton-container');

        containers.forEach(container => {
            const img = container.querySelector('img');
            const skeletons = container.querySelectorAll('.skeleton');

            const cleanup = () => {
                container.classList.remove('is-loading');
                skeletons.forEach(s => s.classList.add('skeleton-hidden'));
                if (img) img.style.opacity = '1';
            };

            if (img) {
                // If image is already cached/complete
                if (img.complete && img.naturalWidth > 0) {
                    cleanup();
                } else {
                    img.addEventListener('load', cleanup, { once: true });
                    img.addEventListener('error', cleanup, { once: true });
                }
            } else {
                // No image, remove skeletons immediately
                cleanup();
            }
        });
    }

    // Touch gestures for mobile
    setupTouchGestures() {
        let startX, startY, endX, endY;
        
        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            
            const diffX = startX - endX;
            const diffY = startY - endY;
            
            // Swipe left/right for navigation
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) {
                    // Swipe left - go to next post
                    this.navigateToNext();
                } else {
                    // Swipe right - go to previous post
                    this.navigateToPrevious();
                }
            }
        });
    }

    navigateToNext() {
        const nextLink = document.querySelector('.pagination .page-btn:last-child');
        if (nextLink && !nextLink.classList.contains('disabled')) {
            nextLink.click();
        }
    }

    navigateToPrevious() {
        const prevLink = document.querySelector('.pagination .page-btn:first-child');
        if (prevLink && !prevLink.classList.contains('disabled')) {
            prevLink.click();
        }
    }

    // Form enhancements
    setupFormEnhancements() {
        // Add loading states to forms
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', (e) => {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="loading-spinner"></span> Processing...';
                    submitBtn.disabled = true;
                    form.classList.add('form-loading');
                }
            });
        });

        // Enhanced password validation
        const passwordInputs = document.querySelectorAll('input[type="password"]');
        passwordInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                this.validatePassword(e.target);
            });
        });
    }

    validatePassword(input) {
        const password = input.value;
        const hint = input.nextElementSibling;
        
        if (!hint || !hint.classList.contains('form-hint')) return;

        if (password.length < 8) {
            hint.textContent = 'Must be at least 8 characters long';
            hint.style.color = '#ef4444';
        } else if (password.length >= 8 && password.length < 12) {
            hint.textContent = 'Good password';
            hint.style.color = '#f59e0b';
        } else {
            hint.textContent = 'Strong password';
            hint.style.color = '#10b981';
        }
    }

    // Accessibility enhancements
    setupAccessibility() {

        // Enhanced focus management
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // ARIA labels for interactive elements
        document.querySelectorAll('button, a, input').forEach(el => {
            if (!el.getAttribute('aria-label') && !el.textContent.trim()) {
                el.setAttribute('aria-label', el.className || 'Interactive element');
            }
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new BlogEnhancements();
});

// Add CSS for keyboard navigation
const style = document.createElement('style');
style.textContent = `
    .keyboard-navigation *:focus {
        outline: 2px solid var(--accent-primary) !important;
        outline-offset: 2px !important;
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
