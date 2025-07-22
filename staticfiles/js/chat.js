// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-resize textarea
    function autoResize(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

    // Format timestamps
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    // Smooth scrolling
    function smoothScrollTo(element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'end'
        });
    }

    // Copy text to clipboard
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function() {
            // Show success feedback
            showToast('Copied to clipboard!', 'success');
        });
    }

    // Show toast notification
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(toast);

        // Auto remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add copy buttons to code blocks
    document.querySelectorAll('pre').forEach(function(pre) {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-secondary position-absolute';
        button.style.cssText = 'top: 5px; right: 5px; font-size: 0.75rem;';
        button.innerHTML = '<i class="fas fa-copy"></i>';
        button.onclick = function() {
            copyToClipboard(pre.textContent);
        };

        pre.style.position = 'relative';
        pre.appendChild(button);
    });

    // Session switching
    document.querySelectorAll('.session-item').forEach(function(item) {
        item.addEventListener('click', function() {
            const sessionId = this.dataset.sessionId;
            if (sessionId) {
                window.location.href = `/chatbot/session/${sessionId}/`;
            }
        });
    });

    // Add loading state to buttons
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
                submitBtn.disabled = true;

                // Re-enable after 5 seconds as fallback
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });

    // Enhanced message formatting
    window.formatMessageContent = function(content) {
        return content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
    };

    // Agent type styling
    window.getAgentStyles = function(agentType) {
        const styles = {
            'supervisor': { icon: '🎯', color: 'bg-danger', name: 'Supervisor' },
            'researcher': { icon: '🔍', color: 'bg-info', name: 'Researcher' },
            'analyst': { icon: '📊', color: 'bg-primary', name: 'Analyst' },
            'writer': { icon: '✍️', color: 'bg-success', name: 'Writer' },
            'user': { icon: '👤', color: 'bg-secondary', name: 'User' },
            'system': { icon: '🤖', color: 'bg-dark', name: 'System' }
        };
        return styles[agentType] || styles['system'];
    };

    console.log('Chat.js loaded successfully!');
});