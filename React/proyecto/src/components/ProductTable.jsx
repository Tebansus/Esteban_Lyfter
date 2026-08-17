import { formatPrice } from '../utils/formatPrice';

// Listado de productos en tabla, con acciones de editar y eliminar.
const ProductTable = ({ products, navigateTo, onDeleteProduct }) => {
  return (
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
  );
};

export default ProductTable;
