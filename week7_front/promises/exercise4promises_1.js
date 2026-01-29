const id = 2;
const user = fetch(`https://reqres.in/api/users/${id}`)
    .then(user => user.json());

user.then(user => {
    console.log(`Usuario: ${user.data.first_name} ${user.data.last_name}`);
}).catch(error => {
    console.log(`Hubo un problema: ${error}`);
});

    
