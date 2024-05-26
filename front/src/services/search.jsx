// import axios from 'axios'
//
// const API_URL = import.meta.env.VITE_API_URL

import { delay } from '../utils/api'

const recipeMock = {
    id: '8c',
    author: {
        id: '21',
        username: 'matthew49',
        displayName: 'Kimberly Shaw',
        icon: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
        roles: 0,
        ratingAvg: 1.5,
    },
    title: 'Meatballs with sauce',
    description:
        'Expert create half this increase system. Such weight attorney enough. Newspaper public fast wall fill.\nKeep his network her. Race wish this camera even.',
    prepTime: 8205,
    allergens: ['asparagus', 'dhansak spice mix'],
    tags: [],
    thumbnail: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    viewCount: 0,
    favorite: false,
}

export const searchRecipes = async ({ query, filters, start, count }) => {
    // return await axios
    //     .post(`${API_URL}/search`, {
    //         data: query,
    //         filters,
    //         page: start,
    //         results_per_page: count
    //     })
    //     .then((response) => response.data)
    //     .catch((err) => console.log(err))
    await delay(2000) // in ms

    return {
        count: 100,
        recipes: [...Array(count).keys()].map((id) => {
            return {
                ...recipeMock,
                title: `${recipeMock.title} #${start + id}`,
                author: {
                    ...recipeMock.author,
                    id: (start + id) % 4 == 0 ? '1' : '21',
                },
                id: start + id,
            }
        }),
    }
}
