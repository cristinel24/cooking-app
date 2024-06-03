import axios from 'axios'
import { authHeader } from '../utils/api'

const API_URL = import.meta.env.VITE_API_URL

export const getRating = async (ratingId) => {
    return (await axios.get(`${API_URL}/ratings/${ratingId}`)).data
}

export const getRatings = async (recipeId, params) => {
    const response = await axios.get(`${API_URL}/recipes/${recipeId}/comments`, {
        params: params,
    })
    return response.data
}

export const getRatingReplies = async (ratingId, params) => {
    const response = await axios.get(`${API_URL}/ratings/${ratingId}/comments`, {
        params: params,
    })
    return response.data
}

export const deleteRating = async (ratingId, token) => {
    await axios.delete(`${API_URL}/ratings/${ratingId}`, { headers: { ...authHeader(token) } })
}

export const editRating = async (ratingId, data, token) => {
    await axios.patch(`${API_URL}/ratings/${ratingId}`, data, { headers: { ...authHeader(token) } })
}

export const addRating = async (recipeId, data, token) => {
    await axios.post(
        `${API_URL}/ratings`,
        {
            ...data,
            parentType: 'recipe',
            parentId: recipeId,
        },
        { headers: { ...authHeader(token) } }
    )
}

export const addRatingReply = async (ratingId, data, token) => {
    await axios.post(
        `${API_URL}/ratings`,
        {
            ...data,
            parentType: 'rating',
            parentId: ratingId,
        },
        { headers: { ...authHeader(token) } }
    )
}
