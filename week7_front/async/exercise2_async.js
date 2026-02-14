async function getUser(userId) {
  console.log("1. Enviando request");
  try {
    const response = await fetch(`https://reqres.in/api/users/${userId}`);
    console.log("2. Response recibido");
    
    if (response.status === 404) {
      console.log(`3. Usuario con ID ${userId} no encontrado.`);
    } else if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    } else {
      const data = await response.json();
      console.log(`3. Usuario: ${data.data.first_name} ${data.data.last_name}`);
      console.log(`Email: ${data.data.email}`);
    }
    
  } catch (error) {
    console.log(`3. Hubo un problema: ${error}`);
  }
  console.log("4. Await terminado");
}
const id = 23;
getUser(id);

console.log("5. Codigo llegado al final");
