import { useState } from 'react';
import './Administration.css';

const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CR', {
    style: 'currency',
    currency: 'CRC',
    minimumFractionDigits: 0
  }).format(price);
};

const Administration = ({ products, navigateTo, onAddProduct, onDeleteProduct }) => {
  const [formData, setFormData] = formDataInit();
  const [errorMsg, setErrorMsg] = useState('');

  function formDataInit() {
    return useState({
      nombre: '',
      descripcion: '',
      precio: '',
      categoria: '',
      imagen: '',
      stock: ''
    });
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleAddSubmit = (e) => {
    e.preventDefault();
    if (!formData.nombre || !formData.descripcion || !formData.precio || !formData.categoria || !formData.imagen || !formData.stock) {
      setErrorMsg('Por favor completa todos los campos antes de agregar el producto.');
      return;
    }
    
    // Convert to appropriate types
    const newProduct = {
      ...formData,
      precio: Number(formData.precio),
      stock: Number(formData.stock)
    };

    onAddProduct(newProduct);
    
    // reset
    setFormData({
      nombre: '',
      descripcion: '',
      precio: '',
      categoria: '',
      imagen: '',
      stock: ''
    });
    setErrorMsg('');
  };

  return (
    <div className="admin-container">
      <h1 className="admin-title">Administración de productos</h1>
      <p className="admin-subtitle">En esta sección puedes gestionar el catálogo de productos de PawStore.</p>

      <div className="admin-content">
        <div className="admin-list-section">
          <h2>Listado de Productos</h2>
          <div className="admin-table-container">
            <table className="admin-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Precio</th>
                  <th>Categoría</th>
                  <th>Stock</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {products.map((product) => (
                  <tr key={product.id}>
                    <td>{String(product.id).padStart(3, '0')}</td>
                    <td>{product.nombre}</td>
                    <td>{formatPrice(product.precio)}</td>
                    <td>{product.categoria}</td>
                    <td>{product.stock}</td>
                    <td className="admin-actions">
                      <button className="btn-edit" onClick={() => navigateTo('edit_product', product)}>Editar</button>
                      <button className="btn-delete" onClick={() => onDeleteProduct(product.id)}>Eliminar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="admin-form-section">
          <h2>Agregar nuevo producto</h2>
          <form className="admin-form" onSubmit={handleAddSubmit}>
            <div className="form-group">
              <label>Nombre</label>
              <input type="text" name="nombre" value={formData.nombre} onChange={handleInputChange} placeholder="Ej: Pelota de Juguete Resistente" />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea name="descripcion" value={formData.descripcion} onChange={handleInputChange} placeholder="Una descripción detallada del producto..."></textarea>
            </div>
            <div className="form-group">
              <label>Precio</label>
              <input type="number" name="precio" value={formData.precio} onChange={handleInputChange} placeholder="Ej: 19.99" />
            </div>
            <div className="form-group">
              <label>Categoría</label>
              <input type="text" name="categoria" value={formData.categoria} onChange={handleInputChange} placeholder="Ej: Juguetes" />
            </div>
            <div className="form-group">
              <label>URL de la imagen</label>
              <input type="text" name="imagen" value={formData.imagen} onChange={handleInputChange} placeholder="Ej: https://example.com/imagen-pelota.jpg" />
            </div>
            <div className="form-group">
              <label>Stock</label>
              <input type="number" name="stock" value={formData.stock} onChange={handleInputChange} placeholder="Ej: 50" />
            </div>
            <button type="submit" className="btn-submit-add">Agregar producto</button>
          </form>
          {errorMsg && <div className="admin-error-msg">{errorMsg}</div>}
        </div>
      </div>
    </div>
  );
};

export default Administration;
