// Simple interactions for the frontend
document.addEventListener('DOMContentLoaded', function() {
    // Like button toggle
    document.querySelectorAll('.btn-like').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            if (this.classList.contains('active')) {
                this.innerHTML = '<i class="bi bi-hand-thumbs-up-fill"></i> معجب به';
            } else {
                this.innerHTML = '<i class="bi bi-hand-thumbs-up"></i> إعجاب';
            }
        });
    });
    
    // Story hover effect
    document.querySelectorAll('.story-item').forEach(story => {
        story.addEventListener('mouseenter', function() {
            this.querySelector('img').style.transform = 'scale(1.02)';
        });
        story.addEventListener('mouseleave', function() {
            this.querySelector('img').style.transform = 'scale(1)';
        });
    });
    
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            document.querySelector('.mobile-menu').classList.toggle('show');
        });
    }
});