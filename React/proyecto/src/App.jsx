import { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import ProductDetail from './pages/ProductDetail';
import Administration from './pages/Administration';
import EditProduct from './pages/EditProduct';
import { useProducts } from './hooks/useProducts';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home', 'catalog', 'detail', 'admin', 'edit_product'
  const [selectedProductId, setSelectedProductId] = useState(null);
  const { products, addProduct, updateProduct, deleteProduct } = useProducts();

  // Se deriva siempre del catálogo a partir del id, evitando mantener una
  // copia separada que haya que sincronizar a mano.
  const selectedProduct = products.find(p => p.id === selectedProductId) || null;

  const navigateTo = (view, product = null) => {
    setCurrentView(view);
    setSelectedProductId(product ? product.id : null);
    window.scrollTo(0, 0);
  };

  const handleUpdateProduct = (updatedProduct) => {
    updateProduct(updatedProduct);
    navigateTo('admin');
  };

  return (
    <div className="app-container">
      <Header currentView={currentView} navigateTo={navigateTo} />
      <main className="main-content">
        {currentView === 'home' && <Home navigateTo={navigateTo} />}
        {currentView === 'catalog' && <Catalog navigateTo={navigateTo} products={products} />}
        {currentView === 'detail' && (
          <ProductDetail navigateTo={navigateTo} product={selectedProduct} />
        )}
        {currentView === 'admin' && (
          <Administration
            products={products}
            navigateTo={navigateTo}
            onAddProduct={addProduct}
            onDeleteProduct={deleteProduct}
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
