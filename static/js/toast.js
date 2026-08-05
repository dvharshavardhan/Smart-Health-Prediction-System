/**
 * MedPredict AI - Enterprise Toast Notification Controller
 */

function showToast(message, type = 'info', duration = 3500) {
    let container = document.getElementById('toastContainer');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = '<i class="fa-solid fa-circle-info" style="color: var(--brand-blue);"></i>';
    if (type === 'success') {
        icon = '<i class="fa-solid fa-circle-check" style="color: var(--emerald-accent);"></i>';
    } else if (type === 'error') {
        icon = '<i class="fa-solid fa-circle-exclamation" style="color: var(--rose-accent);"></i>';
    } else if (type === 'warning') {
        icon = '<i class="fa-solid fa-triangle-exclamation" style="color: var(--amber-accent);"></i>';
    }
    
    toast.innerHTML = `${icon} <span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(40px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}
