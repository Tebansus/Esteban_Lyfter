import ProductTable from '../components/ProductTable';
import ProductForm from '../components/ProductForm';
import './Administration.css';

const Administration = ({ products, navigateTo, onAddProduct, onDeleteProduct }) => {
  return (
    <div className="admin-container">
      <h1 className="admin-title">Administración de productos</h1>
      <p className="admin-subtitle">En esta sección puedes gestionar el catálogo de productos de PawStore.</p>

      <div className="admin-content">
        <div className="admin-list-section">
          <h2>Listado de Productos</h2>
          <ProductTable
            products={products}
            navigateTo={navigateTo}
            onDeleteProduct={onDeleteProduct}
          />
        </div>

        <div className="admin-form-section">
          <h2>Agregar nuevo producto</h2>
          <ProductForm
            onSubmit={onAddProduct}
            submitLabel="Agregar producto"
            formClassName="admin-form"
            submitClassName="btn-submit-add"
            showPlaceholders
            resetOnSubmit
          />
        </div>
      </div>
    </div>
  );
};

export default Administration;
