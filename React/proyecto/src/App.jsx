import { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import ProductDetail from './pages/ProductDetail';
import Administration from './pages/Administration';
import EditProduct from './pages/EditProduct';
import Login from './pages/Login';
import Register from './pages/Register';
import { useProducts } from './hooks/useProducts';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home'); // 'home', 'catalog', 'detail', 'admin', 'edit_product', 'login'
  const [selectedProductId, setSelectedProductId] = useState(null);
  const [user, setUser] = useState(null); // Estado para el usuario autenticado
  const { products, addProduct, updateProduct, deleteProduct } = useProducts();

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

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigateTo('home');
  };

  return (
    <div className="app-container">
      <Header 
        currentView={currentView} 
        navigateTo={navigateTo} 
        user={user} 
        onLogout={handleLogout} 
      />
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
            user={user}
          />
        )}
        {currentView === 'edit_product' && (
          <EditProduct
            product={selectedProduct}
            navigateTo={navigateTo}
            onSave={handleUpdateProduct}
            user={user}
          />
        )}
        {currentView === 'login' && (
          <Login navigateTo={navigateTo} onLogin={handleLogin} />
        )}
        {currentView === 'register' && (
          <Register navigateTo={navigateTo} />
        )}
      </main>
      <Footer />
    </div>
  );
}

export default App;
