import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const uploadImage = async (token, image) => {
    return (
        await axios.post(`${API_URL}/images`, image, {
            headers: {
                Authorization: token,
                'Content-Type': image.type,
            },
        })
    ).data.url
}
