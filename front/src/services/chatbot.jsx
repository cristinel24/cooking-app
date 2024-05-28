import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getResponse = async (message) => {
    const response = 'Buna siua! :>'
    const delay = (ms) => new Promise((res) => setTimeout(res, ms))
    await delay(1200)
    return response
}
