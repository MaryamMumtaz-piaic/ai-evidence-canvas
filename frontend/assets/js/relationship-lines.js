class RelationshipRenderer {
  constructor(svgId, canvas, manager) {
    this.svg = document.getElementById(svgId);
    this.canvas = canvas;
    this.manager = manager;
    this.relationships = [];
    
    this.colors = {
      supports: '#22d3a0',
      contradicts: '#ef4444',
      mentions: '#4f7cff',
      related: '#94a3b8'
    };
  }

  renderRelationships(rels) {
    this.relationships = rels;
    this.updateLines();
  }

  updateLines() {
    this.svg.innerHTML = '';
    const cards = this.manager.cardManager.cards;
    
    this.relationships.forEach(rel => {
      const source = cards.get(rel.sourceId);
      const target = cards.get(rel.targetId);
      if (!source || !target) return;

      const sRect = source.element.getBoundingClientRect();
      const tRect = target.element.getBoundingClientRect();
      const canvasRect = this.canvas.container.getBoundingClientRect();

      const sx = sRect.left + sRect.width / 2 - canvasRect.left;
      const sy = sRect.top + sRect.height / 2 - canvasRect.top;
      const tx = tRect.left + tRect.width / 2 - canvasRect.left;
      const ty = tRect.top + tRect.height / 2 - canvasRect.top;

      const dist = Math.hypot(tx - sx, ty - sy);
      const controlOffset = dist * 0.3;

      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const d = `M ${sx} ${sy} C ${sx} ${sy + controlOffset}, ${tx} ${ty - controlOffset}, ${tx} ${ty}`;
      
      path.setAttribute('d', d);
      path.setAttribute('fill', 'none');
      path.setAttribute('stroke', this.colors[rel.type] || this.colors.related);
      path.setAttribute('stroke-width', '2');
      path.setAttribute('class', 'transition-all duration-300');
      path.dataset.sourceId = rel.sourceId;
      path.dataset.targetId = rel.targetId;
      path.dataset.id = rel.id;
      
      // Hit area for click
      const hitPath = path.cloneNode();
      hitPath.setAttribute('stroke', 'transparent');
      hitPath.setAttribute('stroke-width', '15');
      hitPath.style.cursor = 'pointer';
      hitPath.style.pointerEvents = 'stroke';
      hitPath.addEventListener('click', () => this.manager.openRelationshipInspector(rel, source.data, target.data));

      this.svg.appendChild(path);
      this.svg.appendChild(hitPath);
      
      // Label
      const mx = (sx + tx) / 2;
      const my = (sy + ty) / 2;
      const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      text.setAttribute('x', mx);
      text.setAttribute('y', my);
      text.setAttribute('fill', '#94a3b8');
      text.setAttribute('font-size', '10px');
      text.setAttribute('text-anchor', 'middle');
      text.setAttribute('background', '#0a0b0f');
      text.textContent = rel.type;
      this.svg.appendChild(text);
    });
  }

  highlightConnections(cardId) {
    Array.from(this.svg.querySelectorAll('path, text')).forEach(el => {
      if (el.tagName === 'text') {
         el.style.opacity = '0.2';
         return;
      }
      if (el.dataset.sourceId === cardId || el.dataset.targetId === cardId) {
        el.setAttribute('stroke-width', '3');
        el.style.opacity = '1';
      } else {
        el.style.opacity = '0.2';
      }
    });
  }

  resetHighlights() {
    Array.from(this.svg.querySelectorAll('path')).forEach(el => {
      if (el.getAttribute('stroke') !== 'transparent') {
        el.setAttribute('stroke-width', '2');
        el.style.opacity = '1';
      }
    });
    Array.from(this.svg.querySelectorAll('text')).forEach(el => el.style.opacity = '1');
  }
}
