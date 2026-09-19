class GraphView {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
  }
  
  render(nodes, edges) {
    this.container.innerHTML = `<div class="flex items-center justify-center h-full text-muted flex-col">
      <i data-lucide="network" class="w-16 h-16 mb-4 opacity-50"></i>
      <p>Graph view visualization ready to connect to D3/force-layout engine.</p>
      <p class="text-sm mt-2">Nodes: ${nodes.length}, Edges: ${edges.length}</p>
    </div>`;
    lucide.createIcons({root: this.container});
  }
}
