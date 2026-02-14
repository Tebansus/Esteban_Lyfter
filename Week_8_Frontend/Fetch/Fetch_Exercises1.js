async function fetchData() {
    const response = await fetch("https://api.restful-api.dev/objects");
    const data = await response.json();
    const itemsWithData = data.filter(item => item.data !== null);
    for (const item of itemsWithData) {
        const dataEntries = Object.entries(item.data).map(([key, value]) => `${key}: ${value}`).join(", ");
        console.log(`${item.name} (${dataEntries})`);
    }
}
fetchData();