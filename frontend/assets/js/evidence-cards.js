class EvidenceCardManager {
  constructor(canvas, manager) {
    this.canvas = canvas;
    this.manager = manager;
    this.cards = new Map();
    this.selectedId = null;
    this.isDraggingCard = false;
    this.draggedCard = null;
    this.dragOffset = { x: 0, y: 0 };
    
    this.typeColors = {
      pdf: '#ef4444',
      image: '#8b5cf6',
      url: '#06b6d4',
      note: '#f59e0b',
      email: '#22d3a0'
    };

    this.initEvents();
  }

  initEvents() {
    window.addEventListener('mousemove', this.onMouseMove.bind(this));
    window.addEventListener('mouseup', this.onMouseUp.bind(this));
    
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') this.deselectAll();
      if (e.key === 'Delete' && this.selectedId && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        // Mock delete
        this.removeCard(this.selectedId);
      }
    });
  }

  renderCards(evidenceList) {
    this.canvas.world.innerHTML = '';
    this.cards.clear();
    
    if (evidenceList.length === 0) {
      document.getElementById('canvasEmptyState').classList.remove('hidden');
    } else {
      document.getElementById('canvasEmptyState').classList.add('hidden');
    }

    evidenceList.forEach(evidence => {
      this.addCard(evidence);
    });
    this.manager.onCardsUpdated();
  }

  addCard(evidence) {
    const el = document.createElement('div');
    el.className = `absolute w-[280px] bg-cards border border-panelBorder rounded-xl shadow-lg cursor-grab z-10 transition-shadow select-none evidence-card`;
    el.style.left = `${evidence.x || 0}px`;
    el.style.top = `${evidence.y || 0}px`;
    el.style.borderLeft = `4px solid ${this.typeColors[evidence.type] || '#4f7cff'}`;
    el.dataset.id = evidence.id;

    if (evidence.status !== 'READY') {
      el.classList.add('shimmer');
    }

    const titleIcon = this.getIconForType(evidence.type);

    el.innerHTML = `
      <div class="p-3 border-b border-panelBorder flex justify-between items-start pointer-events-none">
        <div class="flex items-center gap-2 overflow-hidden">
          <span class="p-1 rounded bg-panels text-[${this.typeColors[evidence.type]}]">${titleIcon}</span>
          <h4 class="font-medium text-sm truncate text-textMain" title="${evidence.title}">${evidence.title}</h4>
        </div>
        ${evidence.status === 'READY' ? '<i data-lucide="check-circle-2" class="w-4 h-4 text-green-500 shrink-0"></i>' : '<i data-lucide="loader-2" class="w-4 h-4 text-accent animate-spin shrink-0"></i>'}
      </div>
      <div class="p-3 pointer-events-none">
        <p class="text-xs text-muted line-clamp-2 mb-3">${evidence.summary || 'Processing content...'}</p>
        <div class="flex flex-wrap gap-1 mb-2">
          ${(evidence.entities || []).slice(0, 3).map(e => `<span class="text-[10px] bg-panels px-1.5 py-0.5 rounded text-textMain border border-panelBorder">${e}</span>`).join('')}
        </div>
      </div>
      <div class="p-2 border-t border-panelBorder flex justify-between items-center bg-panels rounded-b-xl">
        <span class="text-xs text-muted flex items-center gap-1"><i data-lucide="link-2" class="w-3 h-3"></i> ${evidence.connections || 0}</span>
        <button class="text-xs text-accent hover:underline cursor-pointer pointer-events-auto open-source-btn">View Source</button>
      </div>
    `;

    el.addEventListener('mousedown', (e) => this.onCardMouseDown(e, evidence.id, el));
    
    const viewBtn = el.querySelector('.open-source-btn');
    if (viewBtn) {
      viewBtn.addEventListener('mousedown', e => e.stopPropagation());
      viewBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this.manager.sourceViewer.open(evidence);
      });
    }

    this.canvas.world.appendChild(el);
    this.cards.set(evidence.id, { element: el, data: evidence });
    lucide.createIcons({ root: el });
  }

  getIconForType(type) {
    const icons = { pdf: '<i data-lucide="file-text" class="w-4 h-4"></i>', image: '<i data-lucide="image" class="w-4 h-4"></i>', url: '<i data-lucide="globe" class="w-4 h-4"></i>', note: '<i data-lucide="sticky-note" class="w-4 h-4"></i>', email: '<i data-lucide="mail" class="w-4 h-4"></i>' };
    return icons[type] || '<i data-lucide="file" class="w-4 h-4"></i>';
  }

  onCardMouseDown(e, id, element) {
    if (e.button !== 0 || this.canvas.isSpaceDown) return;
    e.stopPropagation();
    this.isDraggingCard = true;
    this.draggedCard = { id, element };
    element.classList.add('ring-2', 'ring-accent', 'z-20');
    element.style.cursor = 'grabbing';
    
    const worldPos = this.canvas.screenToWorld(e.clientX, e.clientY);
    const cardRect = element.getBoundingClientRect();
    const cardWorld = this.canvas.screenToWorld(cardRect.left, cardRect.top);
    
    this.dragOffset = {
      x: worldPos.x - cardWorld.x,
      y: worldPos.y - cardWorld.y
    };

    this.selectCard(id);
  }

  onMouseMove(e) {
    if (!this.isDraggingCard || !this.draggedCard) return;
    
    const worldPos = this.canvas.screenToWorld(e.clientX, e.clientY);
    const newX = worldPos.x - this.dragOffset.x;
    const newY = worldPos.y - this.dragOffset.y;
    
    this.draggedCard.element.style.left = `${newX}px`;
    this.draggedCard.element.style.top = `${newY}px`;
    
    const cardData = this.cards.get(this.draggedCard.id).data;
    cardData.x = newX;
    cardData.y = newY;

    if (this.canvas.onTransform) this.canvas.onTransform(); // update lines
  }

  onMouseUp(e) {
    if (this.isDraggingCard && this.draggedCard) {
      this.draggedCard.element.style.cursor = 'grab';
      if (this.draggedCard.id !== this.selectedId) {
        this.draggedCard.element.classList.remove('ring-2', 'ring-accent', 'z-20');
      }
      // Mock API save debounce would go here
      this.isDraggingCard = false;
      this.draggedCard = null;
    }
  }

  selectCard(id) {
    if (this.selectedId === id) return;
    this.deselectAll();
    this.selectedId = id;
    
    const card = this.cards.get(id);
    if (card) {
      card.element.classList.add('ring-2', 'ring-accent', 'z-20');
      this.manager.openInspector(card.data);
      this.manager.relationshipRenderer.highlightConnections(id);
      
      // Fade others
      this.cards.forEach((c, cId) => {
        if (cId !== id) c.element.style.opacity = '0.4';
      });
    }
  }

  deselectAll() {
    if (!this.selectedId) return;
    const card = this.cards.get(this.selectedId);
    if (card) {
      card.element.classList.remove('ring-2', 'ring-accent', 'z-20');
    }
    this.selectedId = null;
    
    this.cards.forEach(c => c.element.style.opacity = '1');
    this.manager.closeInspector();
    this.manager.relationshipRenderer.resetHighlights();
  }

  removeCard(id) {
    const card = this.cards.get(id);
    if (card) {
      card.element.remove();
      this.cards.delete(id);
      this.deselectAll();
      this.manager.onCardsUpdated();
    }
  }
}
