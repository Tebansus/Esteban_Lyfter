async function getUser(userId) {
  console.log("1. Enviando request");
  try {
    const response = await fetch(`https://reqres.in/api/users/${userId}`);
    console.log("2. Response recibido");
    const data = await response.json();
    console.log(`3. Usuario: ${data.data.first_name} ${data.data.last_name}`);
    console.log(`Email: ${data.data.email}`);
    
  } catch (error) {
    console.log(`3. Hubo un problema: ${error}`);
  }
  console.log("4. Await terminado");
}

const id = 2;
getUser(id);

console.log("5. Codigo llegado al final");
