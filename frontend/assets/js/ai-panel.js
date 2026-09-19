class AIPanel {
  constructor() {
    this.panel = document.getElementById('aiChatPanel');
    this.history = document.getElementById('aiChatHistory');
    this.input = document.getElementById('aiChatInput');
    this.submitBtn = document.getElementById('aiChatSubmitBtn');
    this.promptsContainer = document.getElementById('aiQuickPrompts');
    
    this.prompts = [
      "Find contradictions",
      "Show timeline",
      "What evidence is missing?"
    ];
    
    this.init();
  }

  init() {
    document.getElementById('navAskAIBtn').addEventListener('click', () => this.toggle());
    document.getElementById('closeAiPanelBtn').addEventListener('click', () => this.close());
    
    this.submitBtn.addEventListener('click', () => this.handleSend());
    this.input.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.handleSend();
      }
    });

    this.renderPrompts();
    this.addMessage("Hi! I'm your AI investigator. Ask me anything about the evidence on the canvas.", 'ai');
  }

  toggle() {
    this.panel.classList.toggle('open');
  }
  close() {
    this.panel.classList.remove('open');
  }

  renderPrompts() {
    this.promptsContainer.innerHTML = this.prompts.map(p => 
      `<button class="text-xs bg-bg border border-panelBorder hover:border-accent px-2 py-1 rounded-full text-muted hover:text-textMain transition-colors quick-prompt">${p}</button>`
    ).join('');
    
    this.promptsContainer.querySelectorAll('.quick-prompt').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.input.value = e.target.textContent;
        this.handleSend();
      });
    });
  }

  handleSend() {
    const text = this.input.value.trim();
    if (!text) return;
    
    this.addMessage(text, 'user');
    this.input.value = '';
    this.showTyping();
    
    // Mock response
    setTimeout(() => {
      this.removeTyping();
      this.addMessage("Based on the evidence, I found that the dates match perfectly in the contract, but there is a slight contradiction in Email #14 regarding the payment terms.", 'ai', [
        { id: '1', title: 'contract-v2.pdf', context: 'Page 4' },
        { id: '2', title: 'Email #14', context: 'June 12' }
      ]);
    }, 1500);
  }

  addMessage(text, sender, sources = []) {
    const el = document.createElement('div');
    el.className = `flex flex-col ${sender === 'user' ? 'items-end' : 'items-start'} mb-4`;
    
    let sourceHtml = '';
    if (sources.length > 0) {
      sourceHtml = `<div class="mt-2 flex flex-wrap gap-1">` + 
        sources.map(s => `<button class="text-[10px] flex items-center gap-1 bg-panels border border-panelBorder hover:border-accent px-1.5 py-0.5 rounded text-accent transition-colors"><i data-lucide="file-text" class="w-3 h-3"></i> ${s.title} - ${s.context}</button>`).join('') +
        `</div>`;
    }

    el.innerHTML = `
      <div class="px-3 py-2 rounded-lg max-w-[90%] text-sm ${sender === 'user' ? 'bg-accent text-white rounded-tr-none' : 'bg-cards border border-panelBorder text-textMain rounded-tl-none'}">
        ${text}
      </div>
      ${sourceHtml}
    `;
    this.history.appendChild(el);
    lucide.createIcons({root: el});
    this.history.scrollTop = this.history.scrollHeight;
  }

  showTyping() {
    this.typingEl = document.createElement('div');
    this.typingEl.className = 'flex items-start mb-4';
    this.typingEl.innerHTML = `<div class="px-3 py-2 rounded-lg bg-cards border border-panelBorder rounded-tl-none flex gap-1"><span class="w-1.5 h-1.5 bg-muted rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-muted rounded-full animate-bounce" style="animation-delay: 0.2s"></span><span class="w-1.5 h-1.5 bg-muted rounded-full animate-bounce" style="animation-delay: 0.4s"></span></div>`;
    this.history.appendChild(this.typingEl);
    this.history.scrollTop = this.history.scrollHeight;
  }

  removeTyping() {
    if (this.typingEl) this.typingEl.remove();
  }
}
