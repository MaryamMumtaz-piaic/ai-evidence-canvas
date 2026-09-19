class WorkspaceManager {
  constructor() {
    this.canvas = new InfiniteCanvas('canvasContainer', 'canvasWorld');
    this.cardManager = new EvidenceCardManager(this.canvas, this);
    this.relationshipRenderer = new RelationshipRenderer('connectionsLayer', this.canvas, this);
    this.aiPanel = new AIPanel();
    this.filterPanel = new FilterPanel(this);
    this.sourceViewer = new SourceViewer();
    this.timelineView = new TimelineView('timelineView');
    this.graphView = new GraphView('graphView');
    
    this.evidenceList = [];
    this.relationshipsList = [];
    
    // Connect canvas transform to update relationship lines
    this.canvas.onTransform = () => this.relationshipRenderer.updateLines();
  }

  init() {
    this.canvas.init();
    this.initUIBindings();
    this.loadMockData();
    
    setInterval(() => this.pollStatus(), 5000);
  }

  initUIBindings() {
    // Toolbar Views
    const views = document.querySelectorAll('.view-toggle');
    views.forEach(btn => {
      btn.addEventListener('click', (e) => {
        views.forEach(b => {
          b.classList.remove('active', 'bg-cards', 'shadow-sm', 'text-textMain', 'font-medium');
          b.classList.add('text-muted');
        });
        const target = e.target;
        target.classList.add('active', 'bg-cards', 'shadow-sm', 'text-textMain', 'font-medium');
        target.classList.remove('text-muted');
        this.switchView(target.dataset.view);
      });
    });

    // Zoom controls
    document.getElementById('zoomInBtn').addEventListener('click', () => this.canvas.zoomIn());
    document.getElementById('zoomOutBtn').addEventListener('click', () => this.canvas.zoomOut());
    document.getElementById('fitCanvasBtn').addEventListener('click', () => this.canvas.fitToScreen(this.evidenceList));

    // Modals
    const addModal = document.getElementById('addEvidenceModal');
    document.getElementById('addEvidenceBtn').addEventListener('click', () => addModal.classList.add('open'));
    addModal.addEventListener('click', () => addModal.classList.remove('open'));
    document.querySelectorAll('.closeModalBtn').forEach(btn => {
      btn.addEventListener('click', () => addModal.classList.remove('open'));
    });
    
    // Toast helper
    window.showToast = (msg, type='info') => {
      const container = document.getElementById('toastContainer');
      const el = document.createElement('div');
      el.className = `px-4 py-2 rounded shadow-lg text-sm font-medium border border-panelBorder transition-all duration-300 opacity-0 translate-x-4 bg-cards text-textMain`;
      if(type==='success') el.classList.add('border-green-500');
      el.textContent = msg;
      container.appendChild(el);
      requestAnimationFrame(() => {
        el.classList.remove('opacity-0', 'translate-x-4');
      });
      setTimeout(() => {
        el.classList.add('opacity-0', 'translate-x-4');
        setTimeout(() => el.remove(), 300);
      }, 3000);
    };
  }

  switchView(view) {
    document.getElementById('canvasContainer').classList.toggle('hidden', view !== 'canvas');
    document.getElementById('timelineView').classList.toggle('hidden', view !== 'timeline');
    document.getElementById('graphView').classList.toggle('hidden', view !== 'graph');
    
    if (view === 'timeline') this.timelineView.render(this.evidenceList);
    if (view === 'graph') this.graphView.render(this.evidenceList, this.relationshipsList);
  }

  loadMockData() {
    this.evidenceList = [
      { id: '1', type: 'pdf', title: 'contract-v2.pdf', summary: 'Agreement between Company A and B regarding SaaS licensing.', x: 100, y: 150, status: 'READY', entities: ['Company A', 'Company B'], date: '2024-01-15' },
      { id: '2', type: 'email', title: 'Fwd: Payment Terms', summary: 'Email from John discussing the delayed Q3 payments.', x: 500, y: 200, status: 'READY', entities: ['John Doe', 'Q3'], date: '2024-06-12' },
      { id: '3', type: 'image', title: 'invoice-scan.jpg', summary: 'Scanned invoice for $15,000.', x: 300, y: 400, status: 'PROCESSING', entities: ['$15,000'], date: '2024-07-01' }
    ];
    
    this.relationshipsList = [
      { id: 'r1', sourceId: '1', targetId: '2', type: 'mentions', confidence: 0.91, desc: 'Both reference Contract #CT-2048' },
      { id: 'r2', sourceId: '2', targetId: '3', type: 'supports', confidence: 0.85, desc: 'Invoice matches email payment amount' }
    ];

    this.cardManager.renderCards(this.evidenceList);
    this.relationshipRenderer.renderRelationships(this.relationshipsList);
    this.updateSidebarList();
    
    setTimeout(() => this.canvas.fitToScreen(this.evidenceList), 100);
  }

  onCardsUpdated() {
    this.relationshipRenderer.updateLines();
    this.updateSidebarList();
  }

  updateSidebarList() {
    const list = document.getElementById('evidenceList');
    list.innerHTML = this.evidenceList.map(ev => `
      <div class="flex items-center gap-3 p-2 rounded hover:bg-cards cursor-pointer border border-transparent hover:border-panelBorder transition-colors" onclick="document.querySelector('.evidence-card[data-id=\\'${ev.id}\\']')?.dispatchEvent(new MouseEvent('mousedown'))">
        <span class="text-[${this.cardManager.typeColors[ev.type]}]">${this.cardManager.getIconForType(ev.type)}</span>
        <div class="flex-1 overflow-hidden">
          <h5 class="text-sm font-medium truncate text-textMain">${ev.title}</h5>
          <p class="text-xs text-muted truncate">${ev.status}</p>
        </div>
      </div>
    `).join('');
    lucide.createIcons({root: list});
  }

  openInspector(data) {
    const panel = document.getElementById('inspectorPanel');
    panel.innerHTML = `
      <div class="p-4 border-b border-panelBorder flex justify-between items-center bg-cards">
        <h3 class="font-semibold text-textMain flex items-center gap-2">${this.cardManager.getIconForType(data.type)} Evidence Details</h3>
        <button class="text-muted hover:text-textMain" onclick="document.getElementById('inspectorPanel').classList.remove('open')"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>
      <div class="p-5 overflow-y-auto flex-1 bg-bg">
        <h2 class="text-lg font-bold text-white mb-1 break-words">${data.title}</h2>
        <p class="text-xs text-muted mb-6">Added: ${data.date || 'Unknown'}</p>
        
        <div class="mb-6">
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wider mb-2">Summary</h4>
          <p class="text-sm bg-cards p-3 rounded-lg border border-panelBorder leading-relaxed text-gray-300">${data.summary}</p>
        </div>
        
        <div class="mb-6">
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wider mb-2">Entities Found</h4>
          <div class="flex flex-wrap gap-2">
            ${(data.entities||[]).map(e => `<span class="text-xs bg-panels border border-panelBorder px-2 py-1 rounded-md text-textMain">${e}</span>`).join('')}
          </div>
        </div>

        <div class="mb-6">
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wider mb-2">Processing Status</h4>
          <div class="space-y-2 text-sm bg-cards p-3 rounded-lg border border-panelBorder">
            <div class="flex items-center justify-between"><span class="text-gray-400">Text Extraction</span> <i data-lucide="check" class="w-4 h-4 text-green-500"></i></div>
            <div class="flex items-center justify-between"><span class="text-gray-400">Entity NER</span> <i data-lucide="check" class="w-4 h-4 text-green-500"></i></div>
            <div class="flex items-center justify-between"><span class="text-gray-400">Vector Embedding</span> ${data.status==='READY'?'<i data-lucide="check" class="w-4 h-4 text-green-500"></i>':'<i data-lucide="loader-2" class="w-4 h-4 text-accent animate-spin"></i>'}</div>
          </div>
        </div>
      </div>
      <div class="p-4 border-t border-panelBorder bg-cards flex gap-2">
        <button class="flex-1 py-2 bg-accent hover:bg-blue-600 text-white rounded-md text-sm transition-colors" onclick="manager.sourceViewer.open(manager.evidenceList.find(e=>e.id==='${data.id}'))">View Source</button>
      </div>
    `;
    lucide.createIcons({root: panel});
    panel.classList.add('open');
  }

  openRelationshipInspector(rel, source, target) {
    const panel = document.getElementById('inspectorPanel');
    panel.innerHTML = `
      <div class="p-4 border-b border-panelBorder flex justify-between items-center bg-cards">
        <h3 class="font-semibold text-textMain flex items-center gap-2"><i data-lucide="link" class="w-4 h-4"></i> Relationship Details</h3>
        <button class="text-muted hover:text-textMain" onclick="document.getElementById('inspectorPanel').classList.remove('open')"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>
      <div class="p-5 overflow-y-auto flex-1 bg-bg">
        <div class="bg-cards border border-panelBorder rounded-lg p-4 mb-6 flex flex-col items-center text-center">
          <div class="text-sm font-medium text-textMain mb-2 truncate w-full">${source.title}</div>
          <div class="text-xs bg-panels border border-panelBorder px-3 py-1 rounded-full text-accent my-2 capitalize flex items-center gap-1"><i data-lucide="arrow-down" class="w-3 h-3"></i> ${rel.type} <i data-lucide="arrow-down" class="w-3 h-3"></i></div>
          <div class="text-sm font-medium text-textMain mt-2 truncate w-full">${target.title}</div>
        </div>
        
        <div class="mb-6">
          <div class="flex justify-between items-center mb-2">
            <h4 class="text-xs font-semibold text-muted uppercase tracking-wider">AI Confidence</h4>
            <span class="text-xs font-mono text-green-400">${Math.round(rel.confidence * 100)}%</span>
          </div>
          <div class="h-1.5 w-full bg-panels rounded-full overflow-hidden">
            <div class="h-full bg-green-500" style="width: ${rel.confidence * 100}%"></div>
          </div>
        </div>
        
        <div class="mb-6">
          <h4 class="text-xs font-semibold text-muted uppercase tracking-wider mb-2">Reasoning</h4>
          <p class="text-sm bg-cards p-3 rounded-lg border border-panelBorder leading-relaxed text-gray-300 italic">"${rel.desc}"</p>
        </div>
      </div>
    `;
    lucide.createIcons({root: panel});
    panel.classList.add('open');
  }

  closeInspector() {
    document.getElementById('inspectorPanel').classList.remove('open');
  }

  pollStatus() {
    let updated = false;
    this.evidenceList.forEach(ev => {
      if (ev.status === 'PROCESSING') {
        ev.status = 'READY'; // mock finish
        updated = true;
        if(window.showToast) window.showToast(`Analyzed: ${ev.title}`, 'success');
      }
    });
    if (updated) {
      this.cardManager.renderCards(this.evidenceList);
      this.relationshipRenderer.renderRelationships(this.relationshipsList);
      this.updateSidebarList();
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.manager = new WorkspaceManager();
  window.manager.init();
});
