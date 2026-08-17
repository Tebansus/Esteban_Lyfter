import { useState, useEffect } from 'react';

// Hook personalizado que centraliza el estado del catálogo y las
// operaciones para agregar, editar y eliminar productos.
export function useProducts() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    import('../data/products.json')
      .then((module) => {
        const data = module.default || module;
        setProducts(Array.isArray(data) ? data : []);
      })
      .catch(() => {
        setProducts([]);
      });
  }, []);

  const addProduct = (newProduct) => {
    setProducts((current) => {
      const nextId = current.length > 0 ? Math.max(...current.map(p => p.id)) + 1 : 1;
      return [...current, { ...newProduct, id: nextId }];
    });
  };

  const updateProduct = (updatedProduct) => {
    setProducts((current) =>
      current.map(p => (p.id === updatedProduct.id ? updatedProduct : p))
    );
  };

  const deleteProduct = (id) => {
    setProducts((current) => current.filter(p => p.id !== id));
  };

  return { products, addProduct, updateProduct, deleteProduct };
}
