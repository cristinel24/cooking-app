import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getRatings = async (recipeId) => {
    const placeholderRating = {
        id: '7a',
        parentId: '21',
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
    }
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(1200)
    return [placeholderRating]
}

export const getRatingReplies = async (ratingId) => {
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
    }
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(1200)
    return new Array(10).fill(0).map((_) => placeholderRating)
}
