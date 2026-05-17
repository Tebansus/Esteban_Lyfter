import { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import Catalog from './components/Catalog';
import ProductDetail from './components/ProductDetail';
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

  return (
    <div className="app-container">
      <Header currentView={currentView} navigateTo={navigateTo} />
      <main className="main-content">
        {currentView === 'home' && <Home navigateTo={navigateTo} />}
        {currentView === 'catalog' && <Catalog navigateTo={navigateTo} products={productsData} />}
        {currentView === 'detail' && <ProductDetail navigateTo={navigateTo} product={selectedProduct} />}
      </main>
      <Footer />
    </div>
  );
}

export default App;
