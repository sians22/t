const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'API request failed');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Auth endpoints
  async login(username, password) {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async register(userData) {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async initDemoUsers() {
    return this.request('/init-demo-users', {
      method: 'POST',
    });
  }

  // Order endpoints
  async getOrders(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/orders${queryString ? `?${queryString}` : ''}`);
  }

  async createOrder(orderData) {
    return this.request('/orders', {
      method: 'POST',
      body: JSON.stringify(orderData),
    });
  }

  async updateOrder(orderId, updateData) {
    return this.request(`/orders/${orderId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  async getOrder(orderId) {
    return this.request(`/orders/${orderId}`);
  }

  async calculatePrice(coordinates) {
    return this.request('/calculate-price', {
      method: 'POST',
      body: JSON.stringify(coordinates),
    });
  }

  // Promo code endpoints
  async validatePromoCode(code, orderAmount) {
    return this.request('/promo-codes/validate', {
      method: 'POST',
      body: JSON.stringify({ code, order_amount: orderAmount }),
    });
  }

  async getPromoCodes() {
    return this.request('/promo-codes');
  }

  async createPromoCode(promoData) {
    return this.request('/promo-codes', {
      method: 'POST',
      body: JSON.stringify(promoData),
    });
  }

  async initDemoPromos() {
    return this.request('/init-demo-promos', {
      method: 'POST',
    });
  }

  // User endpoints
  async getUsers() {
    return this.request('/users');
  }

  async getUser(userId) {
    return this.request(`/users/${userId}`);
  }

  async updateUser(userId, userData) {
    return this.request(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
  }

  async deleteUser(userId) {
    return this.request(`/users/${userId}`, {
      method: 'DELETE',
    });
  }
}

export default new ApiService();

