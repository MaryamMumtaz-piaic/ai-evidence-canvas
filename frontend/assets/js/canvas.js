class InfiniteCanvas {
  constructor(containerId, worldId) {
    this.container = document.getElementById(containerId);
    this.world = document.getElementById(worldId);
    this.scale = 1;
    this.offsetX = 0;
    this.offsetY = 0;
    this.isDragging = false;
    this.isSpaceDown = false;
    this.lastMouseX = 0;
    this.lastMouseY = 0;
    this.minScale = 0.1;
    this.maxScale = 3;
    this.onTransform = null; // callback for relationship lines
  }

  init() {
    this.container.addEventListener('wheel', this.handleWheel.bind(this), { passive: false });
    this.container.addEventListener('mousedown', this.handleMouseDown.bind(this));
    window.addEventListener('mousemove', this.handleMouseMove.bind(this));
    window.addEventListener('mouseup', this.handleMouseUp.bind(this));
    
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && !this.isSpaceDown && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        this.isSpaceDown = true;
        this.container.classList.add('space-pan');
        e.preventDefault();
      }
    });
    window.addEventListener('keyup', (e) => {
      if (e.code === 'Space') {
        this.isSpaceDown = false;
        this.container.classList.remove('space-pan');
      }
    });

    this.applyTransform();
  }

  applyTransform() {
    this.world.style.transform = `translate(${this.offsetX}px, ${this.offsetY}px) scale(${this.scale})`;
    if (this.onTransform) this.onTransform();
    this.updateZoomLabel();
  }

  updateZoomLabel() {
    const lbl = document.getElementById('zoomLabel');
    if (lbl) lbl.textContent = Math.round(this.scale * 100) + '%';
  }

  handleWheel(e) {
    if (e.ctrlKey || e.metaKey || true) {
      e.preventDefault();
      const zoomSensitivity = 0.001;
      const delta = -e.deltaY * zoomSensitivity;
      const newScale = Math.min(Math.max(this.minScale, this.scale * Math.exp(delta)), this.maxScale);
      
      const rect = this.container.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      this.offsetX = mouseX - (mouseX - this.offsetX) * (newScale / this.scale);
      this.offsetY = mouseY - (mouseY - this.offsetY) * (newScale / this.scale);
      this.scale = newScale;
      this.applyTransform();
    }
  }

  handleMouseDown(e) {
    if (e.button === 1 || e.button === 0 && (e.target === this.container || e.target.id === 'connectionsLayer' || this.isSpaceDown)) {
      this.isDragging = true;
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
      e.preventDefault();
    }
  }

  handleMouseMove(e) {
    if (this.isDragging) {
      const dx = e.clientX - this.lastMouseX;
      const dy = e.clientY - this.lastMouseY;
      this.offsetX += dx;
      this.offsetY += dy;
      this.lastMouseX = e.clientX;
      this.lastMouseY = e.clientY;
      this.applyTransform();
    }
  }

  handleMouseUp() {
    this.isDragging = false;
  }

  screenToWorld(x, y) {
    const rect = this.container.getBoundingClientRect();
    return {
      x: (x - rect.left - this.offsetX) / this.scale,
      y: (y - rect.top - this.offsetY) / this.scale
    };
  }

  setZoom(newScale) {
    const rect = this.container.getBoundingClientRect();
    const cx = rect.width / 2;
    const cy = rect.height / 2;
    newScale = Math.min(Math.max(this.minScale, newScale), this.maxScale);
    
    this.offsetX = cx - (cx - this.offsetX) * (newScale / this.scale);
    this.offsetY = cy - (cy - this.offsetY) * (newScale / this.scale);
    this.scale = newScale;
    this.applyTransform();
  }

  zoomIn() { this.setZoom(this.scale * 1.2); }
  zoomOut() { this.setZoom(this.scale / 1.2); }
  
  fitToScreen(cards) {
    if (!cards || cards.length === 0) {
      this.scale = 1; this.offsetX = 0; this.offsetY = 0;
      this.applyTransform();
      return;
    }
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    cards.forEach(c => {
      minX = Math.min(minX, c.x); minY = Math.min(minY, c.y);
      maxX = Math.max(maxX, c.x + 280); maxY = Math.max(maxY, c.y + 160);
    });
    
    const padding = 100;
    const w = maxX - minX + padding * 2;
    const h = maxY - minY + padding * 2;
    const rect = this.container.getBoundingClientRect();
    
    const scaleX = rect.width / w;
    const scaleY = rect.height / h;
    this.scale = Math.min(Math.max(this.minScale, Math.min(scaleX, scaleY)), 1);
    
    this.offsetX = (rect.width - (maxX - minX) * this.scale) / 2 - minX * this.scale;
    this.offsetY = (rect.height - (maxY - minY) * this.scale) / 2 - minY * this.scale;
    this.applyTransform();
  }
}
