import axios from 'axios'

import { authHeader } from '../utils/api'

const API_URL = import.meta.env.VITE_API_URL

const placeholderRating = {
    id: '7a',
    parentId: '21',
    parentType: 'rating',
    description: 'Georgiana a underscore fr spune Georgiana a  ',
    author: {
        id: '40',
        username: 'davisann',
        displayName: 'Justin Howard',
        icon: 'https://thispersondoesnotexist.com/',
        ratingAvg: 3,
    },
    createdAt: '2024-05-26T05:29:05Z',
    updatedAt: '2024-05-26T05:29:06Z',
}

export const getRatings = async (recipeId, params) => {
    const response = await axios.get(`${API_URL}/recipes/${recipeId}/comments`, {
        params: params,
    })
    console.log(response)
    return response.data
}

export const getRatingReplies = async (ratingId, params) => {
    const response = await axios.get(`${API_URL}/ratings/${ratingId}/comments`, {
        params: params,
    })
    console.log(response)
    return response.data
}

export const deleteRating = async (id, token) => {
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)
}

export const editRating = async (id, data, token) => {
    // receive {description: str, rating: float}; update the rating by calling recipe manager
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)
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
    // data contains description and (optionally) rating 0
    let newData = {
        ...placeholderRating,
        rating: 0,
        ...data,
        parentType: 'rating',
        parentId: ratingId,
        author: {
            ...placeholderRating.author,
            id: '1me', // hardcoded
        },
    }

    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)

    return newData
}
