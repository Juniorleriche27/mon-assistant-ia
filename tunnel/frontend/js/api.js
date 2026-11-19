const API_BASE = (typeof window !== "undefined" && window.NEXT_PUBLIC_API_URL) 
  ? window.NEXT_PUBLIC_API_URL.replace(/\/$/, "") 
  : "";

export const api = {
  async initiateCheckout({ full_name, email, phone }) {
    const res = await fetch(`${API_BASE}/api/v1/checkout/initiate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ full_name, email, phone }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Erreur lors de l'initialisation de la commande");
    }
    return res.json();
  },

  async getOrderStatus(orderId) {
    const res = await fetch(`${API_BASE}/api/v1/checkout/status/${orderId}`);
    if (!res.ok) throw new Error("Impossible de lire le statut de la commande");
    return res.json();
  },

  async getClientDashboard(email, orderId = "") {
    let url = `${API_BASE}/api/v1/client/dashboard?email=${encodeURIComponent(email)}`;
    if (orderId) {
      url += `&order_id=${encodeURIComponent(orderId)}`;
    }
    const res = await fetch(url);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Accès non autorisé à l'espace client");
    }
    return res.json();
  },

  async validateStep(stepNumber, email, orderId = "") {
    let url = `${API_BASE}/api/v1/client/progress/validate?email=${encodeURIComponent(email)}`;
    if (orderId) {
      url += `&order_id=${encodeURIComponent(orderId)}`;
    }
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ step_number: stepNumber }),
    });
    if (!res.ok) throw new Error("Échec de validation de l'étape");
    return res.json();
  },

  async askSupport(question, history = []) {
    const res = await fetch(`${API_BASE}/api/v1/client/support/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, conversation_history: history }),
    });
    if (!res.ok) throw new Error("Erreur de connexion à l'assistant support");
    return res.json();
  },

  async createTicket(subject, conversation, email, orderId) {
    const res = await fetch(`${API_BASE}/api/v1/client/tickets/create?email=${encodeURIComponent(email)}&order_id=${encodeURIComponent(orderId)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject, conversation }),
    });
    if (!res.ok) throw new Error("Impossible d'enregistrer le ticket");
    return res.json();
  },

  async getAdminStats(token) {
    const res = await fetch(`${API_BASE}/api/v1/admin/stats`, {
      headers: { "X-Admin-Token": token }
    });
    if (!res.ok) throw new Error("Accès refusé au cockpit admin");
    return res.json();
  },

  async getAdminOrders(token) {
    const res = await fetch(`${API_BASE}/api/v1/admin/orders`, {
      headers: { "X-Admin-Token": token }
    });
    if (!res.ok) throw new Error("Accès refusé aux commandes");
    return res.json();
  }
};

/**
 * Moteur de rendu Markdown sécurisé et optimisé pour le Chatbot KNOWLIA
 */
export function renderMarkdown(rawText) {
  if (!rawText) return "";

  const escapeHtml = (str) =>
    str.replace(/[&<>"']/g, (m) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    }[m]));

  // Isolation des blocs de code
  const codeBlocks = [];
  let text = rawText.replace(/```([a-zA-Z0-9_\-]+)?\n([\s\S]*?)```/g, (match, lang, code) => {
    const id = `__CODE_BLOCK_${codeBlocks.length}__`;
    codeBlocks.push({ lang: lang || 'text', code: escapeHtml(code.trim()) });
    return id;
  });

  // Échappement du reste du texte pour la sécurité
  text = escapeHtml(text);

  // Tableaux Markdown (| a | b |)
  text = text.replace(/((?:\|[^\n]+\|\r?\n)+)/g, (tableText) => {
    const rows = tableText.trim().split(/\r?\n/).filter(r => r.includes('|'));
    if (rows.length < 2) return tableText;
    let html = '<div class="table-responsive"><table class="chat-table">';
    rows.forEach((row, idx) => {
      if (row.match(/^\|?\s*:?-+:?\s*\|/)) return;
      const cells = row.split('|').filter((_, cIdx, arr) => cIdx > 0 && cIdx < arr.length - 1);
      const tag = idx === 0 ? 'th' : 'td';
      html += '<tr>' + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('') + '</tr>';
    });
    html += '</table></div>';
    return html;
  });

  // Titres
  text = text.replace(/^### (.*$)/gim, '<h4 class="chat-h4">$1</h4>');
  text = text.replace(/^## (.*$)/gim, '<h3 class="chat-h3">$1</h3>');
  text = text.replace(/^# (.*$)/gim, '<h2 class="chat-h2">$1</h2>');

  // Citations / blockquotes
  text = text.replace(/^\> (.*$)/gim, '<blockquote class="chat-quote">$1</blockquote>');

  // Gras et Italique
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

  // Code en ligne
  text = text.replace(/`([^`]+)`/g, '<code class="chat-inline-code">$1</code>');

  // Listes à puces
  text = text.replace(/^\s*[-*]\s+(.*$)/gim, '<li class="chat-li">$1</li>');
  text = text.replace(/((?:<li class="chat-li">.*?<\/li>\s*)+)/gis, '<ul class="chat-ul">$1</ul>');

  // Listes numérotées
  text = text.replace(/^\s*\d+\.\s+(.*$)/gim, '<li class="chat-ol-li">$1</li>');
  text = text.replace(/((?:<li class="chat-ol-li">.*?<\/li>\s*)+)/gis, '<ol class="chat-ol">$1</ol>');

  // Réinsertion des blocs de code avec bouton de copie
  codeBlocks.forEach((cb, idx) => {
    const blockHtml = `
      <div class="chat-code-card">
        <div class="chat-code-header">
          <span>${cb.lang}</span>
          <button type="button" class="chat-code-copy-btn" onclick="navigator.clipboard.writeText(this.closest('.chat-code-card').querySelector('code').textContent); this.textContent='Copié !'; setTimeout(() => this.textContent='Copier', 2000);">Copier</button>
        </div>
        <pre><code class="language-${cb.lang}">${cb.code}</code></pre>
      </div>`;
    text = text.replace(`__CODE_BLOCK_${idx}__`, blockHtml);
  });

  // Retours à la ligne
  text = text.replace(/\n\n+/g, '<br><br>');

  return text;
}
