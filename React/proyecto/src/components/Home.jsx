import './Home.css';

const Home = ({ navigateTo }) => {
  return (
    <div className="home-container">
      <h1 className="home-title">Bienvenido a PawStore</h1>
      <p className="home-paragraph">
        Somos una tienda dedicada a ofrecer productos de calidad para tus mascotas.
      </p>
      <p className="home-paragraph mb-large">
        Explora nuestro catálogo para encontrar camas, juguetes, accesorios y más.
      </p>
      <button 
        className="btn-primary home-button"
        onClick={() => navigateTo('catalog')}
      >
        Ver productos
      </button>
      <p className="home-info-text">
        Esta es la página principal de la aplicación. Más adelante aquí se podrán mostrar productos destacados.
      </p>
    </div>
  );
};

export default Home;
