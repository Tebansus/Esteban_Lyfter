import axios from "axios";


async function fetchData() {
    const response = await axios.get("https://api.restful-api.dev/objects");
    const data = response.data;
    const itemsWithData = data.filter(item => item.data !== null);
    for (const item of itemsWithData) {
        const dataEntries = Object.entries(item.data).map(([key, value]) => `${key}: ${value}`).join(", ");
        console.log(`${item.name} (${dataEntries})`);
    }
}
fetchData();