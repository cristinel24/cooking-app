import React from 'react'

const defaultTheme = {
    bkgcolor: '#FF5348',
    caseta: '#FF8878',
    corpcaseta: '#FFE7E2',
    border: '#000000',
    compreteta: '#FFD4D4',
    hover: '#0000000a',
    profname: '#808080',
    navbar: '#ff5348',
    searchbar: '#FFFFFF',
    neutru: '#828282',
    recipetext: "#0c1821",
}

export const themes = {
    dark: {
        ...defaultTheme,
        txtcolor: '#FFFFFF',
        hoverbkgcolor: '#02080D',
        footercolor: '#FFFFFF',
        hovercolor: '#0c1821',
        body: '#1C1C1C',
        navbarcolor1: '#FFFFFF',
        navbarcolor2: '#000000',
        ubody: '#FFFFFF',
        filterbkcolor: '#303233',
    },
    light: {
        ...defaultTheme,
        txtcolor: '#0c1821',
        hoverbkgcolor: '#ee3326',
        footercolor: '#0C1821',
        hovercolor: '#FFFFFF',
        body: '#E9E9E9',
        navbarcolor1: '#000000',
        navbarcolor2: '#FFFFFF',
        ubody: '#1C1C1C',
        filterbkcolor: '#F3F3F3',
    },
}

export const ThemeContext = React.createContext({
    theme: themes.light,
    toggleTheme: () => {},
})
