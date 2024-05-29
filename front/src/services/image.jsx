import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

let id = 0

export const uploadImage = async (data) => {
    const imgId = id
    id++
    return `https://picsum.photos/id/${id}/200/300`
    // try {
    //     const response = await axios.put(`${API_URL}/api/image_storage`, data, {
    //         headers: {
    //             // ...data.getHeaders(),
    //             accept: 'application/json',
    //             'Content-Type': 'multipart/form-data',
    //         },
    //     })
    //     return response
    // } catch (err) {
    //     throw err
    // }
}
