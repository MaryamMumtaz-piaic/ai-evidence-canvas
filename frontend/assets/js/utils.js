function getToastContainer() {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  return container;
}

export function showToast(message, type = 'info') {
  const container = getToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  
  const icons = {
    info: 'info',
    success: 'check-circle',
    error: 'x-circle',
    warning: 'alert-triangle'
  };
  
  const iconColor = {
    info: 'text-accent',
    success: 'text-success',
    error: 'text-danger',
    warning: 'text-warning'
  };
  
  toast.innerHTML = `
    <i data-lucide="${icons[type] || 'info'}" class="w-5 h-5 ${iconColor[type] || 'text-text-primary'}"></i>
    <span class="text-sm font-medium text-text-primary">${message}</span>
  `;
  
  container.appendChild(toast);
  if (window.lucide) lucide.createIcons({ root: toast });
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px) translateX(20px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

export function formatDate(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diffSec = Math.floor((now - date) / 1000);
  
  if (diffSec < 60) return 'Just now';
  if (diffSec < 3600) return `${Math.floor(diffSec / 60)} mins ago`;
  if (diffSec < 86400) return `${Math.floor(diffSec / 3600)} hours ago`;
  
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined 
  });
}

export function getEvidenceIcon(type) {
  const icons = {
    pdf: 'file-text',
    image: 'image',
    url: 'link',
    note: 'sticky-note',
    email: 'mail',
    'text-file': 'file'
  };
  return icons[type] || 'file';
}

export function getEvidenceColor(type) {
  const colors = {
    pdf: 'var(--pdf)',
    image: 'var(--image)',
    url: 'var(--url)',
    note: 'var(--note)',
    email: 'var(--email)',
    'text-file': 'var(--text-file)'
  };
  return colors[type] || 'var(--text-secondary)';
}

export function getStatusBadge(status) {
  const normalized = (status || 'active').toLowerCase();
  const badges = {
    active: 'bg-success/10 text-success border-success/20',
    archived: 'bg-text-muted/10 text-text-secondary border-text-muted/20',
    processing: 'bg-warning/10 text-warning border-warning/20 animate-pulse',
    error: 'bg-danger/10 text-danger border-danger/20'
  };
  const classes = badges[normalized] || badges.active;
  return `<span class="px-2.5 py-0.5 text-[10px] uppercase tracking-wider font-semibold rounded-full border ${classes}">${normalized}</span>`;
}

export function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

export function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

export function showModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    const panel = modal.querySelector('.modal-panel');
    if (panel) {
      setTimeout(() => {
        panel.style.opacity = '1';
        panel.style.transform = 'scale(1) translateY(0)';
      }, 10);
    }
  }
}

export function hideModal(id) {
  const modal = document.getElementById(id);
  if (modal) {
    const panel = modal.querySelector('.modal-panel');
    if (panel) {
      panel.style.opacity = '0';
      panel.style.transform = 'scale(0.95) translateY(10px)';
    }
    setTimeout(() => {
      modal.classList.add('hidden');
      modal.classList.remove('flex');
    }, 200);
  }
}

export function confirm(message, title = 'Confirm Action') {
  return new Promise((resolve) => {
    const id = 'confirm-dialog-' + Date.now();
    const html = \`
      <div id="\${id}" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm transition-opacity duration-200">
        <div class="modal-panel bg-bg-secondary border border-border rounded-xl shadow-2xl p-6 max-w-sm w-full mx-4 transition-all duration-200" style="opacity:0; transform:scale(0.95)">
          <h3 class="text-lg font-semibold text-text-primary mb-2 flex items-center gap-2">
            <i data-lucide="alert-triangle" class="w-5 h-5 text-warning"></i> \${title}
          </h3>
          <p class="text-text-secondary text-sm mb-6 ml-7">\${message}</p>
          <div class="flex justify-end gap-3">
            <button id="\${id}-cancel" class="px-4 py-2 rounded-lg text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-bg-tertiary transition-colors">Cancel</button>
            <button id="\${id}-confirm" class="px-4 py-2 rounded-lg text-sm font-medium bg-danger hover:bg-red-500 text-white transition-colors">Confirm</button>
          </div>
        </div>
      </div>
    \`;
    
    document.body.insertAdjacentHTML('beforeend', html);
    if (window.lucide) lucide.createIcons({ root: document.getElementById(id) });
    
    setTimeout(() => {
      const panel = document.querySelector(\`#\${id} .modal-panel\`);
      if(panel) {
          panel.style.opacity = '1';
          panel.style.transform = 'scale(1)';
      }
    }, 10);
    
    const cleanup = (result) => {
      const panel = document.querySelector(\`#\${id} .modal-panel\`);
      if(panel) {
          panel.style.opacity = '0';
          panel.style.transform = 'scale(0.95)';
      }
      setTimeout(() => {
        document.getElementById(id).remove();
        resolve(result);
      }, 200);
    };

    document.getElementById(\`\${id}-cancel\`).onclick = () => cleanup(false);
    document.getElementById(\`\${id}-confirm\`).onclick = () => cleanup(true);
  });
}

export function setLoading(element, isLoading, text = 'Processing...') {
  if (isLoading) {
    element.dataset.originalHtml = element.innerHTML;
    element.disabled = true;
    element.innerHTML = \`<i data-lucide="loader-2" class="w-4 h-4 mr-2 animate-spin inline-block"></i> \${text}\`;
    if (window.lucide) lucide.createIcons({ root: element });
  } else {
    element.disabled = false;
    element.innerHTML = element.dataset.originalHtml || element.innerHTML;
    if (window.lucide) lucide.createIcons({ root: element });
  }
}
