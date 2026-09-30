import { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { GlobalContext } from '../context/GlobalContext';
import './Checkout.css';

const Checkout = () => {
  const { cart, getCartTotal, clearCart } = useContext(GlobalContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    address: ''
  });
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (cart.length === 0) return;

    setIsSubmitting(true);
    setError(null);

    const token = localStorage.getItem('token');

    // Create the payload exactly as the backend expects
    const salePayload = {
      buyer_name: formData.fullName,
      buyer_email: formData.email,
      shipping_address: formData.address,
      items: cart.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price
      })),
      total_amount: getCartTotal()
    };

    try {
      const response = await fetch('http://localhost:3001/api/sales', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify(salePayload)
      });

      if (!response.ok) {
        throw new Error('Ocurrió un problema al procesar tu compra. Por favor intenta de nuevo.');
      }

      clearCart();
      navigate('/confirmacion');
    } catch (err) {
      setError(err.message || 'Ocurrió un problema al procesar tu compra. Por favor intenta de nuevo.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="checkout-container">
        <p>Tu carrito está vacío.</p>
        <button className="btn btn-primary" onClick={() => navigate('/productos')}>Volver al catálogo</button>
      </div>
    );
  }

  return (
    <div className="checkout-container">
      <h2 className="checkout-title">Checkout</h2>
      <p className="checkout-intro">Revisa los detalles de tu compra y completa la información necesaria para finalizar el pedido.</p>
      
      {error && <div className="error-message">{error}</div>}

      <div className="checkout-content">
        <div className="checkout-summary">
          <h3>Resumen de compra</h3>
          <ul className="summary-list">
            {cart.map(item => (
              <li key={item.id}>
                <span>{item.name} (x{item.quantity})</span>
                <span>${item.price * item.quantity}</span>
              </li>
            ))}
          </ul>
          <div className="summary-total">
            <strong>Total: ${getCartTotal()}</strong>
          </div>
        </div>

        <div className="checkout-form-container">
          <form onSubmit={handleSubmit} className="checkout-form">
            <div className="form-group">
              <label htmlFor="fullName">Nombre completo</label>
              <input
                type="text"
                id="fullName"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">Correo electrónico</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="address">Dirección de envío</label>
              <textarea
                id="address"
                name="address"
                value={formData.address}
                onChange={handleChange}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary btn-block" disabled={isSubmitting}>
              {isSubmitting ? 'Procesando...' : 'Confirmar compra'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
