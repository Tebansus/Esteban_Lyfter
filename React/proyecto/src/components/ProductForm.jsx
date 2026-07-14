import { useState } from 'react';
import './ProductForm.css';

// Valores iniciales de un producto vacío (usado por el formulario de alta).
const EMPTY_PRODUCT = {
  nombre: '',
  descripcion: '',
  precio: '',
  categoria: '',
  imagen: '',
  stock: ''
};

// Formulario reutilizable para agregar y editar productos.
// El estado se inicializa a partir de `initialValues` desde el primer render,
// por lo que los campos nacen ya con los datos (sin parpadeo).
const ProductForm = ({
  initialValues = EMPTY_PRODUCT,
  onSubmit,
  onCancel,
  submitLabel = 'Guardar',
  cancelLabel = 'Cancelar',
  formClassName = '',
  submitClassName = '',
  cancelClassName = '',
  actionsClassName = '',
  showPlaceholders = false,
  resetOnSubmit = false
}) => {
  const [formData, setFormData] = useState(initialValues);
  const [errorMsg, setErrorMsg] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.nombre || !formData.descripcion || !formData.precio ||
        !formData.categoria || !formData.imagen || !formData.stock) {
      setErrorMsg('Por favor completa todos los campos obligatorios.');
      return;
    }

    onSubmit({
      ...formData,
      precio: Number(formData.precio),
      stock: Number(formData.stock)
    });

    setErrorMsg('');
    if (resetOnSubmit) {
      setFormData(initialValues);
    }
  };

  const placeholder = (text) => (showPlaceholders ? text : undefined);

  return (
    <>
      {errorMsg && <div className="form-error-msg">{errorMsg}</div>}
      <form className={formClassName} onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="product-nombre">Nombre</label>
          <input id="product-nombre" type="text" name="nombre" value={formData.nombre} onChange={handleInputChange} placeholder={placeholder('Ej: Pelota de Juguete Resistente')} />
        </div>
        <div className="form-group">
          <label htmlFor="product-descripcion">Descripción</label>
          <textarea id="product-descripcion" name="descripcion" value={formData.descripcion} onChange={handleInputChange} placeholder={placeholder('Una descripción detallada del producto...')}></textarea>
        </div>
        <div className="form-group">
          <label htmlFor="product-precio">Precio</label>
          <input id="product-precio" type="number" name="precio" value={formData.precio} onChange={handleInputChange} placeholder={placeholder('Ej: 19.99')} />
        </div>
        <div className="form-group">
          <label htmlFor="product-categoria">Categoría</label>
          <input id="product-categoria" type="text" name="categoria" value={formData.categoria} onChange={handleInputChange} placeholder={placeholder('Ej: Juguetes')} />
        </div>
        <div className="form-group">
          <label htmlFor="product-imagen">URL de la imagen</label>
          <input id="product-imagen" type="text" name="imagen" value={formData.imagen} onChange={handleInputChange} placeholder={placeholder('Ej: https://example.com/imagen-pelota.jpg')} />
        </div>
        <div className="form-group">
          <label htmlFor="product-stock">Stock</label>
          <input id="product-stock" type="number" name="stock" value={formData.stock} onChange={handleInputChange} placeholder={placeholder('Ej: 50')} />
        </div>
        <div className={actionsClassName}>
          {onCancel && (
            <button type="button" className={cancelClassName} onClick={onCancel}>{cancelLabel}</button>
          )}
          <button type="submit" className={submitClassName}>{submitLabel}</button>
        </div>
      </form>
    </>
  );
};

export default ProductForm;
