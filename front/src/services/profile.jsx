import axios from 'axios'
import { ngrok } from '../utils/api'

const API_URL = import.meta.env.VITE_API_URL

export const getProfile = async (profileId, token) => {
    const headers = { ...(token !== undefined && token !== '' && { Authorization: token }) }

    const response = await axios.get(`${API_URL}/users/${profileId}`, {
        headers: ngrok(headers),
    })
    console.log(response)
    return response.data
}

export const getFollowers = async (profileId, start, count) => {
    const response = await axios.get(`${API_URL}/users/${profileId}/followers`, {
        headers: ngrok({}),
        params: { start: start, count: count },
    })
    console.log(response)
    return response.data
}
export const getFollowing = async (profileId, start, count) => {
    const response = await axios.get(`${API_URL}/users/${profileId}/following`, {
        headers: ngrok({}),
        params: { start: start, count: count },
    })
    console.log(response)
    return response.data
}

export const follow = async (userId, otherUserId, token) => {
    await axios.post(
        `${API_URL}/users/${userId}/follow`,
        { followsId: otherUserId },
        {
            headers: ngrok({ Authorization: token }),
        }
    )
}

export const unfollow = async (userId, otherUserId, token) => {
    await axios.delete(
        `${API_URL}/users/${userId}/follow`,
        { followsId: otherUserId },
        {
            headers: ngrok({ Authorization: token }),
        }
    )
}
