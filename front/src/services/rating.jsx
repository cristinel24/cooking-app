import axios from 'axios'

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

export const getRatings = async ({ recipeId, start, count }) => {
    const finalCount = 100

    console.log(
        `count ${finalCount !== undefined ? finalCount : '-'} ${
            start !== undefined ? start : '-'
        } ${count !== undefined ? count : '-'} `
    )
    const ratings = new Array(count).fill(0).map((_, index) => ({
        ...placeholderRating,
        description: `${index + start}`,
        id: `${index + start}`,
    }))
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)
    return { total: 100, data: ratings }
}

export const getRatingReplies = async ({ ratingId, start, count }) => {
    const finalCount = 100
    const ratings = new Array(count).fill(0).map((_, index) => ({
        ...placeholderRating,
        description: `${index + start}`,
        id: `${ratingId}_${index + start}`,
    }))

    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)
    return { total: 100, data: ratings }
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
    // data contains description and (optionally) rating 0
    let newData = {
        ...placeholderRating,
        rating: 0,
        ...data,
        parentType: 'recipe',
        parentId: recipeId,
        id: `${100000 + (Math.random() % 2500)}`,
    }

    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)

    return newData
}

export const addRatingReply = async (ratingId, data, token) => {
    // data contains description and (optionally) rating 0
    let newData = { rating: 0, ...data, parentType: 'rating', parentId: ratingId }

    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(700)
}
