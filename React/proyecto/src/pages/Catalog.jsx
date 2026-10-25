import { Link, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { GlobalContext } from '../context/GlobalContext';
import { formatPrice } from '../utils/formatPrice';
import './Catalog.css';

const Catalog = ({ products }) => {
  const navigate = useNavigate();
  const { addToCart } = useContext(GlobalContext);

  if (!Array.isArray(products) || products.length === 0) {
    return (
      <div className="catalog-container empty">
        <p className="empty-message">No hay productos disponibles por el momento.</p>
      </div>
    );
  }

  return (
    <div className="catalog-container">
      <h2 className="catalog-title">Catálogo de productos</h2>
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <div className="product-image-container">
              {product.imagen ? (
                <img src={product.imagen} alt={product.nombre} className="product-image" />
              ) : (
                <div className="product-image-placeholder">Sin imagen</div>
              )}
            </div>
            <div className="product-info">
              <h3 className="product-name">{product.nombre}</h3>
              <p className="product-price">{formatPrice(product.precio)}</p>
              <p className="product-category">{product.categoria}</p>
              <Link 
                className="btn-primary product-button"
                to={`/productos/${product.id}`}
                style={{ display: 'block', textDecoration: 'none', textAlign: 'center', boxSizing: 'border-box' }}
              >
                Ver detalles
              </Link>
              <button 
                className="btn-primary product-button"
                style={{ marginTop: '0.5rem', backgroundColor: '#28a745', borderColor: '#28a745' }}
                onClick={() => addToCart(product)}
              >
                Agregar al carrito
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Catalog;
