import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getRatings = async ({ recipeId, start, count }) => {
    const placeholderRating = {
        id: '7a',
        parentId: '21',
        rating: 3,
        parentType: 'recipe',
        description:
            'Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune ',
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
    await delay(3000)
    return { count: finalCount, ratings: ratings }
}

export const getRatingReplies = async ({ ratingId, start, count }) => {
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
        createdAt: '2024-05-26T05:29:06Z',
        updatedAt: '2024-05-26T05:29:06Z',
    }

    const finalCount = 100
    const ratings = new Array(count).fill(0).map((_, index) => ({
        ...placeholderRating,
        description: `${index + start}`,
        id: `${ratingId}_${index + start}`,
    }))

    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(1200)
    return { count: 100, replies: ratings }
}
