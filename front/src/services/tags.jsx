import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL

export const getTags = async (startingWith) => {
    return (await axios.get(`${API_URL}/tags?starting_with=${startingWith}`)).data.tags
}
