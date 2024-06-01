import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

export const getRecipeCard = async (recipeId, token) => {
    const headers = { ...(token !== undefined && token !== '' && { Authorization: token }) }
    const response = await axios.get(`${API_URL}/recipes/${recipeId}/card`, {
        headers,
    })
    console.log(response)
    return response.data
}

export const getRecipe = async (recipeId, token) => {
    const headers = { ...(token !== undefined && token !== '' && { Authorization: token }) }
    const response = await axios.get(`${API_URL}/recipes/${recipeId}`, {
        headers,
    })
    console.log(response)
    return response.data
}

export const deleteRecipe = async (recipeId, token) => {}

export const saveRecipe = async (userId, recipeId, token) => {
    await axios.put(
        `${API_URL}/users/${userId}/saved-recipes/${recipeId}`,
        {},
        {
            headers: { Authorization: token },
        }
    )
}

export const unsaveRecipe = async (userId, recipeId, token) => {
    await axios.delete(`${API_URL}/users/${userId}/saved-recipes/${recipeId}`, {
        headers: { Authorization: token },
    })
}
