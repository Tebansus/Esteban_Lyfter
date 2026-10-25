import { Link } from 'react-router-dom';
import './NotFound.css';

const NotFound = () => {
  return (
    <div className="not-found-container">
      <h2 className="not-found-title">Página no encontrada</h2>
      <p className="not-found-text">
        La página que estás buscando no existe o ha sido movida.
      </p>
      <Link to="/" className="btn btn-primary">Volver al inicio</Link>
    </div>
  );
};

export default NotFound;
