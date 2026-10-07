import { useContext } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Catalog from './pages/Catalog';
import ProductDetail from './pages/ProductDetail';
import Administration from './pages/Administration';
import EditProduct from './pages/EditProduct';
import Login from './pages/Login';
import Register from './pages/Register';
import Cart from './pages/Cart';
import Checkout from './pages/Checkout';
import PurchaseConfirmation from './pages/PurchaseConfirmation';
import NotFound from './pages/NotFound';
import { useProducts } from './hooks/useProducts';
import { GlobalContext } from './context/GlobalContext';
import './App.css';

function App() {
  const { user, login, logout } = useContext(GlobalContext);
  const { products, loading: productsLoading, addProduct, updateProduct, deleteProduct } = useProducts();
  const navigate = useNavigate();

  const handleUpdateProduct = (updatedProduct) => {
    updateProduct(updatedProduct);
    navigate('/admin');
  };

  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/productos" element={<Catalog products={products} />} />
          <Route path="/productos/:id" element={<ProductDetail products={products} loading={productsLoading} />} />
          <Route path="/carrito" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/confirmacion" element={<PurchaseConfirmation />} />
          
          <Route path="/admin" element={
            <Administration
              products={products}
              onAddProduct={addProduct}
              onDeleteProduct={deleteProduct}
            />
          } />
          <Route path="/admin/editar/:id" element={
            <EditProduct
              products={products}
              onSave={handleUpdateProduct}
            />
          } />
          
          <Route path="/login" element={<Login />} />
          <Route path="/registro" element={<Register />} />
          
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
