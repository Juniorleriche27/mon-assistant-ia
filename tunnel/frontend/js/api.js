const API_BASE = "";

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

  async getClientDashboard(email, orderId) {
    const res = await fetch(`${API_BASE}/api/v1/client/dashboard?email=${encodeURIComponent(email)}&order_id=${encodeURIComponent(orderId)}`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Accès non autorisé à l'espace client");
    }
    return res.json();
  },

  async validateStep(stepNumber, email, orderId) {
    const res = await fetch(`${API_BASE}/api/v1/client/progress/validate?email=${encodeURIComponent(email)}&order_id=${encodeURIComponent(orderId)}`, {
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
