const id = 23;
const user = fetch(`https://reqres.in/api/users/${id}`)
    .then(user => {
        if (user.status === 404) {
            console.log(`Usuario con ID ${id} no encontrado.`);
            return null;
        } else if (!user.ok) {
            throw new Error(`HTTP error! status: ${user.status}`);
        }else {
            return user.json();
        }
    }) .then(data => {
        if (data) {
            console.log(`Usuario: ${data.data.first_name} ${data.data.last_name}`);
            console.log(`Email: ${data.data.email}`);
        }
    }).catch(error => {
        console.log(`Hubo un problema: ${error}`);
    }). finally(() => {
        console.log("Await terminado");
    });