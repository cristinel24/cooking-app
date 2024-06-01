import axios from 'axios'
import { delay } from '../utils/api'

const API_URL = import.meta.env.VITE_API_URL

export const getFullProfile = async (id, token) => {
    return (
        await axios.get(`${API_URL}/users/${id}/profile`, {
            headers: {
                Authorization: token,
            },
        })
    ).data
}

export const updateProfile = async (id, token, data) => {
    console.log(data)
    await axios.patch(`${API_URL}/users/${id}`, data, {
        headers: {
            Authorization: token,
        },
    })
}
