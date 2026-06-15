import './ProductDetail.css';

const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CR', {
    style: 'currency',
    currency: 'CRC',
    minimumFractionDigits: 0
  }).format(price);
};

const ProductDetail = ({ product, navigateTo }) => {
  if (!product) {
    return (
      <div className="detail-container empty">
        <p>Producto no encontrado.</p>
        <button className="btn-primary" onClick={() => navigateTo('catalog')}>Volver al catálogo</button>
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
            <p className="detail-info-text">
              Más adelante aquí se podrá agregar este producto al carrito y completar la compra.
            </p>
            <button 
              className="btn-primary detail-button"
              onClick={() => navigateTo('catalog')}
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
