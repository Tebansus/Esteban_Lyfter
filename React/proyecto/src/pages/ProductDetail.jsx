import { useNavigate, useParams } from 'react-router-dom';
import { useContext } from 'react';
import { GlobalContext } from '../context/GlobalContext';
import { formatPrice } from '../utils/formatPrice';
import './ProductDetail.css';

const ProductDetail = ({ products }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { addToCart } = useContext(GlobalContext);

  const product = products.find(p => p.id === parseInt(id));

  if (!product) {
    return (
      <div className="detail-container empty">
        <p>Producto no encontrado.</p>
        <button className="btn-primary" onClick={() => navigate('/productos')}>Volver al catálogo</button>
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
              onClick={() => addToCart({ id: product.id, name: product.nombre, price: product.precio, image_url: product.imagen })}
            >
              Agregar al carrito
            </button>
            <button 
              className="btn-primary detail-button"
              onClick={() => navigate('/productos')}
            >
              Volver al catálogo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
