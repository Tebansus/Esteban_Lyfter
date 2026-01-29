const pokemon_ids = [3, 6, 9];

const request = pokemon_ids.map(id =>
    fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
        .then(response => response.json())
);

Promise.all(request)
    .then(pokemons => {
        pokemons.forEach(pokemon => {
            console.log(`Pokemon: ${pokemon.forms[0].name}`);
        });
    }).catch(error => {
        console.error('Error:', error);
    });