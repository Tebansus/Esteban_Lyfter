import './Catalog.css';

const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CR', {
    style: 'currency',
    currency: 'CRC',
    minimumFractionDigits: 0
  }).format(price);
};

const Catalog = ({ products, navigateTo }) => {
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
              <button 
                className="btn-primary product-button"
                onClick={() => navigateTo('detail', product)}
              >
                Ver detalles
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Catalog;
