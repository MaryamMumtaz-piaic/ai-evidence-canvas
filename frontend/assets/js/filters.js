class FilterPanel {
  constructor(manager) {
    this.manager = manager;
    this.panel = document.getElementById('filterPanel');
    this.btn = document.getElementById('navFiltersBtn');
    this.badge = document.getElementById('filterBadge');
    
    this.filters = {
      types: new Set(),
    };
    
    this.init();
  }

  init() {
    this.btn.addEventListener('click', () => this.toggle());
    document.getElementById('closeFilterPanelBtn').addEventListener('click', () => this.close());
    
    const container = this.panel.querySelector('.p-4.flex-1');
    container.innerHTML = `
      <div class="mb-6">
        <h4 class="text-xs font-semibold text-muted uppercase tracking-wider mb-3">Evidence Type</h4>
        <div class="space-y-2">
          ${['pdf', 'image', 'url', 'note', 'email'].map(type => `
            <label class="flex items-center gap-2 text-sm cursor-pointer hover:text-white transition-colors">
              <input type="checkbox" value="${type}" class="filter-type rounded bg-bg border-panelBorder text-accent focus:ring-accent accent-accent">
              <span class="capitalize">${type}</span>
            </label>
          `).join('')}
        </div>
      </div>
      <button id="clearFiltersBtn" class="w-full py-2 bg-panels border border-panelBorder rounded-md text-sm text-muted hover:text-white transition-colors">Clear All</button>
    `;

    container.querySelectorAll('.filter-type').forEach(cb => {
      cb.addEventListener('change', (e) => {
        if (e.target.checked) this.filters.types.add(e.target.value);
        else this.filters.types.delete(e.target.value);
        this.apply();
      });
    });

    container.querySelector('#clearFiltersBtn').addEventListener('click', () => {
      this.filters.types.clear();
      container.querySelectorAll('.filter-type').forEach(cb => cb.checked = false);
      this.apply();
    });
  }

  toggle() { this.panel.classList.toggle('open'); }
  close() { this.panel.classList.remove('open'); }

  apply() {
    const activeCount = this.filters.types.size;
    if (activeCount > 0) this.badge.classList.remove('hidden');
    else this.badge.classList.add('hidden');
    
    // Tell manager to filter
    // Simple filter: if types is empty, show all, else check type
    const allCards = Array.from(this.manager.cardManager.cards.values());
    allCards.forEach(c => {
      if (this.filters.types.size === 0 || this.filters.types.has(c.data.type)) {
        c.element.style.display = 'block';
      } else {
        c.element.style.display = 'none';
      }
    });
    this.manager.canvas.applyTransform(); // trigger line update
  }
}
