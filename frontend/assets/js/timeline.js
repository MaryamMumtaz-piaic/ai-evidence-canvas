class TimelineView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }

  render(evidenceList) {
    const sorted = [...evidenceList].sort((a, b) => new Date(a.date || 0) - new Date(b.date || 0));
    
    let html = `<div class="relative w-max min-w-full h-full flex items-center pt-20 pb-20 px-10">
      <div class="absolute top-1/2 left-0 right-0 h-1 bg-panelBorder -translate-y-1/2"></div>
      <div class="flex gap-16 relative z-10">`;

    sorted.forEach(ev => {
      html += `
        <div class="flex flex-col items-center group cursor-pointer w-48 shrink-0">
          <div class="mb-4 p-3 bg-cards border border-panelBorder rounded-lg shadow-lg group-hover:border-accent transition-colors">
            <h5 class="text-sm font-medium text-textMain truncate mb-1">${ev.title}</h5>
            <p class="text-xs text-muted line-clamp-2">${ev.summary}</p>
          </div>
          <div class="w-4 h-4 bg-accent rounded-full border-4 border-bg relative z-10 mb-2"></div>
          <div class="text-xs font-mono text-muted">${ev.date || 'Unknown'}</div>
        </div>
      `;
    });

    html += `</div></div>`;
    this.container.innerHTML = html;
  }
}
