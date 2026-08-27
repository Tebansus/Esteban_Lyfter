import ProductForm from '../components/ProductForm';
import './EditProduct.css';

const EditProduct = ({ product, navigateTo, onSave, user }) => {
  if (!user || user.role !== 'admin') {
    return (
      <div className="unauthorized-page">
        <div className="unauthorized-card">
          <h2>Acceso no autorizado</h2>
          <p>Esta sección está disponible únicamente para administradores.</p>
          <button className="back-home-button" onClick={() => navigateTo('home')}>Volver al inicio</button>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="edit-container">
        <p>No se ha seleccionado ningún producto para editar.</p>
        <button className="btn-primary" onClick={() => navigateTo('admin')}>Volver a administración</button>
      </div>
    );
  }

  const handleSave = (values) => {
    onSave({ ...product, ...values });
  };

  return (
    <div className="edit-container">
      <h1 className="edit-title">Editar producto</h1>

      <div className="edit-form-card">
        {/* La `key` fuerza el remontaje del formulario al cambiar de producto,
            de modo que sus campos nacen ya con los datos correctos. */}
        <ProductForm
          key={product.id}
          initialValues={product}
          onSubmit={handleSave}
          onCancel={() => navigateTo('admin')}
          submitLabel="Guardar cambios"
          cancelLabel="Cancelar"
          formClassName="edit-form"
          submitClassName="btn-submit-edit"
          cancelClassName="btn-secondary"
          actionsClassName="edit-actions"
        />
      </div>
    </div>
  );
};

export default EditProduct;
