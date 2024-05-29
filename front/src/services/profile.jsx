import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

const placeholderProfile = {
    id: '1',
    username: 'davisann',
    displayName: 'Justin Howard',
    icon: 'https://thispersondoesnotexist.com',
    roles: 0,
    ratingAvg: 3,
    description:
        '<p> text textual <strong>cu</strong> <em>text</em>.  </p> <img src="https://www.eatright.org/-/media/images/eatright-landing-pages/foodgroupslp_804x482.jpg?as=0&w=967&rev=d0d1ce321d944bbe82024fff81c938e7&hash=E6474C8EFC5BE5F0DA9C32D4A797D10D"/> <p>cu ocazia asta</p> <p>am sa intreb: in descriere pot fi imagini? </p>',
    recipes: ['7a', 'a1', 'd5'],
    ratings: ['121'],
    followingCount: 2,
    followersCount: 75,
    isFollowing: false,
}

const placeholderUserCard = {
    id: '4',
    username: 'mark37_timothy03',
    displayName: 'Jason Johnson',
    icon: 'https://thispersondoesnotexist.com',
    roles: 0,
    ratingAvg: 2.5,
    updatedAt: '2024-05-28T19:46:15.695000',
    createdAt: '2024-05-28T19:46:18Z',
}

const placeholderFollows = [
    {
        id: '6h',
        username: 'laurabrown',
        displayName: 'James Cunningham',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3.25,
        updatedAt: '2024-05-28T19:46:18.958000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '6a',
        username: 'janet12_tcole',
        displayName: 'Veronica Smith',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 2.5,
        updatedAt: '2024-05-28T19:46:18.813000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '65',
        username: 'kshepherd',
        displayName: 'Megan Martin',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3.25,
        updatedAt: '2024-05-28T19:46:18.748000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '62',
        username: 'amberramsey',
        displayName: 'Blake Smith',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3,
        updatedAt: '2024-05-28T19:46:18.697000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '5r',
        username: 'edwardsmichael',
        displayName: 'Laura Shelton',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3.5,
        updatedAt: '2024-05-28T19:46:18.546000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '5o',
        username: 'daltonmichael',
        displayName: 'Leslie Gallegos',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3.8,
        updatedAt: '2024-05-28T19:46:18.497000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '5j',
        username: 'heather19',
        displayName: 'Vanessa Cox',
        icon: 'https://thispersondoesnotexist.com',
        roles: 4,
        ratingAvg: 2,
        updatedAt: '2024-05-28T19:46:18.413000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '5i',
        username: 'joseph86',
        displayName: 'Nicole Pacheco',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 4,
        updatedAt: '2024-05-28T19:46:18.407000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '5h',
        username: 'shannon63',
        displayName: 'Jesse Vega',
        icon: 'https://thispersondoesnotexist.com',
        roles: 12,
        ratingAvg: 2.86,
        updatedAt: '2024-05-28T19:46:18.391000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '5c',
        username: 'jacob42_millerfrances',
        displayName: 'Matthew Nash',
        icon: 'https://thispersondoesnotexist.com',
        roles: 8,
        ratingAvg: 1.67,
        updatedAt: '2024-05-28T19:46:18.324000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '53',
        username: 'samanthakane',
        displayName: 'Kimberly Patton',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 4,
        updatedAt: '2024-05-28T19:46:18.181000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '4z',
        username: 'amartinez',
        displayName: 'Christopher Ramos',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3,
        updatedAt: '2024-05-28T19:46:18.129000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '4s',
        username: 'robertibarra',
        displayName: 'Cynthia Miranda',
        icon: 'https://thispersondoesnotexist.com',
        roles: 4,
        ratingAvg: 4,
        updatedAt: '2024-05-28T19:46:18.036000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '4o',
        username: 'laurarodriguez',
        displayName: 'Jorge Villarreal',
        icon: 'https://thispersondoesnotexist.com',
        roles: 4,
        ratingAvg: 3,
        updatedAt: '2024-05-28T19:46:17.988000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '4n',
        username: 'robinsonkimberly',
        displayName: 'Nancy Williams',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3.5,
        updatedAt: '2024-05-28T19:46:17.976000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '44',
        username: 'michellearnold',
        displayName: 'Erik Martinez',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 4.8,
        updatedAt: '2024-05-28T19:46:17.683000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '41',
        username: 'alyssa48',
        displayName: 'Brandon Meyer',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3,
        updatedAt: '2024-05-28T19:46:17.587000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '3x',
        username: 'annette42',
        displayName: 'Johnny Fisher',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 2.33,
        updatedAt: '2024-05-28T19:46:17.540000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '3q',
        username: 'wnunez_joannerichardson',
        displayName: 'Amy Long',
        icon: 'https://thispersondoesnotexist.com',
        roles: 4,
        ratingAvg: 3,
        updatedAt: '2024-05-28T19:46:17.447000',
        createdAt: '2024-05-28T19:46:18Z',
    },
    {
        id: '3o',
        username: 'carl07_josephnelson',
        displayName: 'Roger Christensen',
        icon: 'https://thispersondoesnotexist.com',
        roles: 0,
        ratingAvg: 3,
        updatedAt: '2024-05-28T19:46:17.420000',
        createdAt: '2024-05-28T19:46:18Z',
    },
]

export const getProfile = async (profileId) => {
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(1200)
    return placeholderProfile
}

export const getFollowers = async (profileId, start, count) => {
    // const response = await axios.get(`${API_URL}/user/${profileId}/followers`, {
    //     params: {
    //         start: start,
    //         count: count,
    //     },
    // })
    // return response.data
    // const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    // await delay(1200)

    // let response = {
    //     following: placeholderFollowing.map((user) => ({
    //         ...user,
    //         id: `${1000000 + ((Math.random() % 4579) + 5000)}`,
    //     })),
    // }
    return { followers: placeholderFollows }
}
export const getFollowing = async (profileId, start, count) => {
    // const response = await axios.get(`${API_URL}/user/${profileId}/following`, {
    //     params: {
    //         start: start,
    //         count: count,
    //     },
    // })
    // return response.data
    // const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    // await delay(1200)

    // let response = {
    //     following: placeholderFollowing.following.map((user) => ({
    //         ...user,
    //         id: `${1000000 + (Math.random() % 4579)}`,
    //     })),
    // }

    return { following: placeholderFollows }
}
