import axios from "axios"

const API_URL = import.meta.env.VITE_API_URL

export const register = async (data) => {
    await axios.post(`${API_URL}/auth/register`, data)
        .then(response => console.log(response))
        .catch(err => console.log(err))
}

export const verify = async (token) => {
    await axios.post(`${API_URL}/auth/verify?token=${token}`)
        .then(response => console.log(response))
        .catch(err => console.log(err))
}

export const login = async (data) => {
    await axios.post(`${API_URL}/auth/login`, data)
        .then(response => console.log(response))
        .catch(err => console.log(err))
}
