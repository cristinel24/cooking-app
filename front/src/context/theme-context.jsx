import React from 'react'

/*
    ThemeContext defining the color theme of the project.

    If the color you are about to add is the same for both light and dark
    color themes, add it in defaultTheme instead. Otherwise, define it
    in both the dark and light themes.

    The theming will be converted from camelCase to kebab-case;
    if you define a variable like this:
    exampleVariable: "#ABCDEF"
    you will be able to use it in CSS by writing
    var(--example-variable)
    which should help prevent weird abbreviations and respect CSS conventions.
*/

export const defaultTheme = {
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
    defaultTheme: defaultTheme,
    toggleTheme: () => {},
})