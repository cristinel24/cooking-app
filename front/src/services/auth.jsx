import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const registerUser = async (user) => {
    await axios.post(`${API_URL}/register`, user)
}

export const verifyAccount = async (token) => {
    await axios.post(`${API_URL}/verify?token_value=${token}`)
}

export const loginUser = async (data) => {
    return (await axios.post(`${API_URL}/login`, data)).data
}

export const credentialChange = async (email, type) => {
    // return await axios.post(`${API_URL}/TODO`, { email, type })
}
