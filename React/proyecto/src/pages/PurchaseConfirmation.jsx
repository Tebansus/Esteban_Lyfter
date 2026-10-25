import { Link } from 'react-router-dom';
import './PurchaseConfirmation.css';

const PurchaseConfirmation = () => {
  return (
    <div className="confirmation-container">
      <h2 className="confirmation-title">¡Gracias por tu compra!</h2>
      <p className="confirmation-text">
        Hemos enviado un correo de confirmación con los detalles de tu pedido.
      </p>
      <Link to="/productos" className="btn btn-primary">Volver al catálogo</Link>
    </div>
  );
};

export default PurchaseConfirmation;
