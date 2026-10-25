import { useContext } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { GlobalContext } from '../context/GlobalContext';
import ProductForm from '../components/ProductForm';
import './EditProduct.css';

const EditProduct = ({ products, onSave }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(GlobalContext);

  if (!user || user.role !== 'admin') {
    return (
      <div className="unauthorized-page">
        <div className="unauthorized-card">
          <h2>Acceso no autorizado</h2>
          <p>No tienes permiso para acceder a esta sección.</p>
          <button className="back-home-button" onClick={() => navigate('/')}>Volver al inicio</button>
        </div>
      </div>
    );
  }

  const product = products.find(p => p.id === parseInt(id));

  if (!product) {
    return (
      <div className="edit-container">
        <p>No se ha seleccionado ningún producto para editar.</p>
        <button className="btn-primary" onClick={() => navigate('/admin')}>Volver a administración</button>
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
          onCancel={() => navigate('/admin')}
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
