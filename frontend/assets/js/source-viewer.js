class SourceViewer {
  constructor() {
    this.modal = document.getElementById('sourceViewerModal');
    this.title = document.getElementById('sourceViewerTitle');
    this.content = document.getElementById('sourceViewerContent');
    
    this.modal.querySelectorAll('.closeModalBtn').forEach(btn => {
      btn.addEventListener('click', () => this.close());
    });
  }

  open(evidence) {
    const icon = this.getIcon(evidence.type);
    this.title.innerHTML = `${icon} <span class="text-textMain">${evidence.title}</span>`;
    
    let html = '';
    if (evidence.type === 'pdf') {
      html = `<div class="bg-cards border border-panelBorder rounded-lg p-8 shadow-inner min-h-[500px] font-serif text-gray-300 leading-relaxed">
        <h2 class="text-2xl font-bold mb-4 text-white">${evidence.title}</h2>
        <p class="whitespace-pre-wrap">${evidence.content || evidence.summary}</p>
        <p class="mt-8 text-sm text-muted">[End of document extracted text]</p>
      </div>`;
    } else if (evidence.type === 'image') {
      html = `<div class="flex items-center justify-center h-full"><div class="bg-panels border border-panelBorder p-2 rounded-xl inline-block max-w-full"><img src="https://via.placeholder.com/800x600/1a1d26/4f7cff?text=Image+Preview" class="max-w-full max-h-[70vh] rounded-lg object-contain"></div></div>`;
    } else {
      html = `<div class="bg-cards border border-panelBorder rounded-lg p-6 shadow-inner"><pre class="whitespace-pre-wrap text-sm text-gray-300 font-mono">${evidence.content || evidence.summary}</pre></div>`;
    }
    
    this.content.innerHTML = html;
    this.modal.classList.add('open');
    lucide.createIcons({root: this.title});
  }

  close() {
    this.modal.classList.remove('open');
  }

  getIcon(type) {
    const icons = { pdf: '<i data-lucide="file-text" class="w-5 h-5 text-red-500"></i>', image: '<i data-lucide="image" class="w-5 h-5 text-purple-500"></i>', url: '<i data-lucide="globe" class="w-5 h-5 text-cyan-500"></i>', note: '<i data-lucide="sticky-note" class="w-5 h-5 text-yellow-500"></i>', email: '<i data-lucide="mail" class="w-5 h-5 text-emerald-500"></i>' };
    return icons[type] || '<i data-lucide="file" class="w-5 h-5 text-gray-400"></i>';
  }
}
