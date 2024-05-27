import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getProfile = async (profileId) => {
    const placeholderProfile = {
        id: '40',
        username: 'davisann',
        displayName: 'Justin Howard',
        icon: 'https://www.eatright.org/-/media/images/eatright-landing-pages/foodgroupslp_804x482.jpg?as=0&w=967&rev=d0d1ce321d944bbe82024fff81c938e7&hash=E6474C8EFC5BE5F0DA9C32D4A797D10D',
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
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(1200)
    return placeholderProfile
}
