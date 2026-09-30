import { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { GlobalContext } from '../context/GlobalContext';
import './Cart.css';

const Cart = () => {
  const { cart, updateQuantity, removeFromCart, getCartTotal, clearCart } = useContext(GlobalContext);
  const navigate = useNavigate();

  return (
    <div className="cart-container">
      <h2 className="cart-title">Tu Carrito</h2>
      {cart.length === 0 ? (
        <div className="empty-cart">
          <p>Tu carrito está vacío.</p>
          <Link to="/productos" className="btn btn-primary">Volver al catálogo</Link>
        </div>
      ) : (
        <div className="cart-content">
          <div className="cart-items">
            {cart.map((item) => (
              <div key={item.id} className="cart-item">
                <img src={item.image_url} alt={item.name} className="cart-item-image" />
                <div className="cart-item-details">
                  <h3 className="cart-item-name">{item.name}</h3>
                  <p className="cart-item-price">Precio: ${item.price}</p>
                </div>
                <div className="cart-item-actions">
                  <div className="quantity-control">
                    <button onClick={() => updateQuantity(item.id, -1)}>-</button>
                    <span>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.id, 1)}>+</button>
                  </div>
                  <button onClick={() => removeFromCart(item.id)} className="btn-remove">
                    Quitar
                  </button>
                </div>
                <div className="cart-item-subtotal">
                  <p>Subtotal: ${item.price * item.quantity}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <h3>Total: ${getCartTotal()}</h3>
            <button className="btn btn-primary" onClick={() => navigate('/checkout')}>
              Ir al checkout
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart;
