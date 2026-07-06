import { useState, useEffect } from 'react';
import './EditProduct.css';

const EditProduct = ({ product, navigateTo, onSave }) => {
  const [formData, setFormData] = useState({
    nombre: '',
    descripcion: '',
    precio: '',
    categoria: '',
    imagen: '',
    stock: ''
  });
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (product) {
      setFormData({
        nombre: product.nombre || '',
        descripcion: product.descripcion || '',
        precio: product.precio || '',
        categoria: product.categoria || '',
        imagen: product.imagen || '',
        stock: product.stock || ''
      });
    }
  }, [product]);

  if (!product) {
    return (
      <div className="edit-container">
        <p>No se ha seleccionado ningún producto para editar.</p>
        <button className="btn-primary" onClick={() => navigateTo('admin')}>Volver a administración</button>
      </div>
    );
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSave = (e) => {
    e.preventDefault();
    if (!formData.nombre || !formData.descripcion || !formData.precio || !formData.categoria || !formData.imagen || !formData.stock) {
      setErrorMsg('Por favor completa todos los campos antes de guardar los cambios.');
      return;
    }
    
    const updatedProduct = {
      ...product,
      ...formData,
      precio: Number(formData.precio),
      stock: Number(formData.stock)
    };

    onSave(updatedProduct);
  };

  return (
    <div className="edit-container">
      <h1 className="edit-title">Editar producto</h1>
      
      <div className="edit-form-card">
        {errorMsg && <div className="edit-error-msg">{errorMsg}</div>}
        <form className="edit-form" onSubmit={handleSave}>
          <div className="form-group">
            <label>Nombre</label>
            <input type="text" name="nombre" value={formData.nombre} onChange={handleInputChange} />
          </div>
          <div className="form-group">
            <label>Descripción</label>
            <textarea name="descripcion" value={formData.descripcion} onChange={handleInputChange}></textarea>
          </div>
          <div className="form-group">
            <label>Precio</label>
            <input type="number" name="precio" value={formData.precio} onChange={handleInputChange} />
          </div>
          <div className="form-group">
            <label>Categoría</label>
            <input type="text" name="categoria" value={formData.categoria} onChange={handleInputChange} />
          </div>
          <div className="form-group">
            <label>URL de la imagen</label>
            <input type="text" name="imagen" value={formData.imagen} onChange={handleInputChange} />
          </div>
          <div className="form-group">
            <label>Stock</label>
            <input type="number" name="stock" value={formData.stock} onChange={handleInputChange} />
          </div>
          <div className="edit-actions">
            <button type="button" className="btn-secondary" onClick={() => navigateTo('admin')}>Cancelar</button>
            <button type="submit" className="btn-submit-edit">Guardar cambios</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditProduct;
