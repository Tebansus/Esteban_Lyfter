import { Link, useNavigate, useParams } from 'react-router-dom';
import { useContext } from 'react';
import { GlobalContext } from '../context/GlobalContext';
import { formatPrice } from '../utils/formatPrice';
import './ProductDetail.css';

const ProductDetail = ({ products, loading }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useContext(GlobalContext);

  if (loading) {
    return (
      <div className="detail-container empty">
        <p>Cargando producto...</p>
      </div>
    );
  }

  const product = products.find(p => p.id === parseInt(id));

  if (!product) {
    return (
      <div className="detail-container empty">
        <p>Producto no encontrado.</p>
        <Link to="/productos" className="btn-primary" style={{ display: 'inline-block', textDecoration: 'none' }}>Volver al catálogo</Link>
      </div>
    );
  }

  return (
    <div className="detail-container">
      <div className="detail-card">
        <div className="detail-image-section">
          {product.imagen ? (
            <img src={product.imagen} alt={product.nombre} className="detail-image" />
          ) : (
            <div className="detail-image-placeholder">Sin imagen</div>
          )}
        </div>
        
        <div className="detail-info-section">
          <h2 className="detail-name">{product.nombre}</h2>
          <p className="detail-price">{formatPrice(product.precio)}</p>
          <p className="detail-category">{product.categoria}</p>
          <p className="detail-description">{product.descripcion}</p>
          
          <div className="detail-actions">
            <button 
              className="btn-primary detail-button"
              style={{ backgroundColor: '#28a745', borderColor: '#28a745' }}
              onClick={() => addToCart(product)}
            >
              Agregar al carrito
            </button>
            <Link 
              className="btn-primary detail-button"
              to="/productos"
              style={{ display: 'inline-block', textDecoration: 'none', textAlign: 'center', boxSizing: 'border-box' }}
            >
              Volver al catálogo
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
