import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Catalog from './components/Catalog';
import ProductDetail from './components/ProductDetail';
import Administration from './components/Administration';
import EditProduct from './components/EditProduct';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home', 'catalog', 'detail'
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [productsData, setProductsData] = useState([]);

  useEffect(() => {
    import('./data/products.json')
      .then((module) => {
        const data = module.default || module;
        setProductsData(Array.isArray(data) ? data : []);
      })
      .catch(() => {
        setProductsData([]);
      });
  }, []);

  const navigateTo = (view, product = null) => {
    setCurrentView(view);
    setSelectedProduct(product);
    window.scrollTo(0, 0); 
  };

  const handleAddProduct = (newProduct) => {
    const nextId = productsData.length > 0 ? Math.max(...productsData.map(p => p.id)) + 1 : 1;
    const productWithId = { ...newProduct, id: nextId };
    setProductsData([...productsData, productWithId]);
  };

  const handleDeleteProduct = (id) => {
    setProductsData(productsData.filter(p => p.id !== id));
    if (selectedProduct && selectedProduct.id === id) {
      setSelectedProduct(null);
    }
  };

  const handleUpdateProduct = (updatedProduct) => {
    setProductsData(productsData.map(p => p.id === updatedProduct.id ? updatedProduct : p));
    if (selectedProduct && selectedProduct.id === updatedProduct.id) {
      setSelectedProduct(updatedProduct);
    }
    navigateTo('admin');
  };

  return (
    <div className="app-container">
      <Header currentView={currentView} navigateTo={navigateTo} />
      <main className="main-content">
        {currentView === 'home' && <Home navigateTo={navigateTo} />}
        {currentView === 'catalog' && <Catalog navigateTo={navigateTo} products={productsData} />}
        {currentView === 'detail' && (
          <ProductDetail 
            navigateTo={navigateTo} 
            product={productsData.find(p => p.id === selectedProduct?.id)} 
          />
        )}
        {currentView === 'admin' && (
          <Administration 
            products={productsData} 
            navigateTo={navigateTo}
            onAddProduct={handleAddProduct}
            onDeleteProduct={handleDeleteProduct}
          />
        )}
        {currentView === 'edit_product' && (
          <EditProduct 
            product={selectedProduct} 
            navigateTo={navigateTo}
            onSave={handleUpdateProduct}
          />
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
