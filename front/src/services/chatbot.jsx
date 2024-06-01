import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getResponse = async (token, message) => {
    return (
        await axios.post(
            `${API_URL}/ai/chatbot`,
            { userQuery: message },
            {
                headers: { Authorization: token },
            }
        )
    ).data.response
}
