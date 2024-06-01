import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL

export const getAllergens = async (startingWith) => {
    return (await axios.get(`${API_URL}/allergens?starting_with=${startingWith}`)).data.allergens
}
