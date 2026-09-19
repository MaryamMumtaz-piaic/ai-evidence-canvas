const API_BASE = 'http://localhost:8000/api';

async function fetchAPI(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      let errorMsg = `Error ${response.status}`;
      try {
        const errorData = await response.json();
        errorMsg = errorData.message || errorData.error || errorMsg;
      } catch (e) {
        errorMsg = await response.text() || errorMsg;
      }
      return { data: null, error: errorMsg };
    }
    
    if (response.status === 204) {
      return { data: true, error: null };
    }
    
    const data = await response.json();
    return { data, error: null };
  } catch (err) {
    return { data: null, error: 'Network error. Make sure the API is running.' };
  }
}

const api = {
  workspaces: {
    list: () => fetchAPI('/workspaces'),
    get: (id) => fetchAPI(`/workspaces/${id}`),
    create: (data) => fetchAPI('/workspaces', { method: 'POST', body: JSON.stringify(data) }),
    update: (id, data) => fetchAPI(`/workspaces/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`/workspaces/${id}`, { method: 'DELETE' }),
    analyze: (id) => fetchAPI(`/workspaces/${id}/analyze`, { method: 'POST' }),
    getRelationships: (id) => fetchAPI(`/workspaces/${id}/relationships`),
    getTimeline: (id) => fetchAPI(`/workspaces/${id}/timeline`),
    getGraph: (id) => fetchAPI(`/workspaces/${id}/graph`),
    export: (id) => fetchAPI(`/workspaces/${id}/export`),
  },
  
  evidence: {
    list: (workspaceId) => fetchAPI(`/workspaces/${workspaceId}/evidence`),
    get: (id) => fetchAPI(`/evidence/${id}`),
    createNote: (data) => fetchAPI('/evidence/note', { method: 'POST', body: JSON.stringify(data) }),
    createURL: (data) => fetchAPI('/evidence/url', { method: 'POST', body: JSON.stringify(data) }),
    upload: async (workspaceId, file, type) => {
      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('type', type);
        formData.append('workspaceId', workspaceId);
        
        const response = await fetch(`${API_BASE}/evidence/upload`, {
          method: 'POST',
          body: formData
        });
        
        if (!response.ok) throw new Error(`Upload failed: ${response.status}`);
        return { data: await response.json(), error: null };
      } catch (e) {
        return { data: null, error: e.message };
      }
    },
    update: (id, data) => fetchAPI(`/evidence/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`/evidence/${id}`, { method: 'DELETE' }),
  },
  
  search: (workspaceId, query) => fetchAPI(`/workspaces/${workspaceId}/search?q=${encodeURIComponent(query)}`),
  ask: (workspaceId, question) => fetchAPI(`/workspaces/${workspaceId}/ask`, { method: 'POST', body: JSON.stringify({ question }) }),
  
  relationships: {
    get: (id) => fetchAPI(`/relationships/${id}`),
    create: (data) => fetchAPI('/relationships', { method: 'POST', body: JSON.stringify(data) }),
    delete: (id) => fetchAPI(`/relationships/${id}`, { method: 'DELETE' }),
  }
};

export default api;
