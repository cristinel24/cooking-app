// import axios from 'axios'
//
// const API_URL = import.meta.env.VITE_API_URL

export const registerUser = async (user) => {
    // await axios
    //     .post(`${API_URL}/auth/register`, user)
    //     .then((response) => console.log(response))
    //     .catch((err) => console.log(err))
}

export const verifyAccount = async (token) => {
    // await axios
    //     .post(`${API_URL}/auth/verify?token=${token}`)
    //     .then((response) => console.log(response))
    //     .catch((err) => console.log(err))
}

export const loginUser = async (data) => {
    // return await axios
    //     .post(`${API_URL}/auth/login`, data)
    //     .then((response) => response.data)
    //     .catch((err) => console.log(err))

    // throw { response: { errorCode: 12345 } }

    return {
        sessionToken: '1234',
        user: {
            id: '1',
            username: 'jimmy07_dylan04',
            displayName: 'jimmy',
            icon: 'avatar.png',
            roles: 2,
            ratingAvg: 12312.3
        }
    }
}

export const credentialChange = async (email, type) => {
    // return await axios
    //     .post(`${API_URL}/auth/reset`, { email, type })
    //     .then((response) => response.data)
    //     .catch((err) => console.log(err))
}
