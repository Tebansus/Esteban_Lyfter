const pokemon_ids = [3, 6, 9];

const request = pokemon_ids.map(id =>
    fetch(`https://pokeapi.co/api/v2/pokemon/${id}`)
        .then(response => response.json())
);

Promise.any(request)
    .then(pokemon => {
        console.log(`Pokemon: ${pokemon.forms[0].name}`);
    }).catch(error => {
        console.error('All requests failed', error);
    });