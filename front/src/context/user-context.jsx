import React from "react";

export const UserContext = React.createContext({
    user: {},
    token: {},
    login: (token, user) => {},
    logout: () => {},
    loggedIn: () => {}
})
