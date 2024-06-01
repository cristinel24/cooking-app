import axios from 'axios'
import { wrap } from '../utils/api'

const API_URL = import.meta.env.VITE_API_URL

export const getFullProfile = async (id, token) => {
    return (
        await axios.get(`${API_URL}/users/${id}/profile`, {
            headers: wrap({ Authorization: token }),
        })
    ).data
}

export const updateProfile = async (id, token, data) => {
    await axios.patch(`${API_URL}/users/${id}`, data, {
        headers: {
            Authorization: token,
        },
    })
}
