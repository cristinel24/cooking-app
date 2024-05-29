import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const registerUser = async (user) => {
    await axios.post(`${API_URL}/register`, user)
}

export const verifyAccount = async (token) => {
    await axios.post(`${API_URL}/verify?token_value=${token}`)
}

// export const loginUser = async (data) => {
//     return (await axios.post(`${API_URL}/login`, data)).data
// }

export const loginUser = async (data) => {
    return {
        sessionToken: '1234',
        user: {
            id: '1',
            username: 'jimmy07_dylan04',
            displayName: 'jimmy',
            icon: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            roles: 2,
            ratingAvg: 12312.3,
        },
    }
}

export const credentialChange = async (email, type) => {
    // return await axios.post(`${API_URL}/TODO`, { email, type })
}
