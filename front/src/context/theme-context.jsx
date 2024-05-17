import React from 'react'

/*
    ThemeContext defining the color theme of the project.

    The theming will be converted from camelCase to kebab-case;
    if you define a variable like this:
    exampleVariable: "#ABCDEF"
    you will be able to use it in CSS by writing
    var(--example-variable)
    which should help prevent weird abbreviations and respect CSS conventions.
*/

export const themes = {
    dark: {
        bkgcolor: '#FF5348',
        txtcolor: '#FFFFFF',
        hoverbkgcolor: '#02080D',
        footercolor: '#FFFFFF',
        hovercolor: '#0c1821',
        caseta: '#FF8878',
        corpcaseta: '#FFE7E2',
        border: '#000000',
        compreteta: '#FFD4D4',
        body: '#1C1C1C',
        hover: '#0000000a',
        profname: '#808080',
        navbar: '#ff5348',
        navbarcolor1: '#FFFFFF',
        navbarcolor2: '#000000',
        searchbar: '#FFFFFF',
        ubody: '#FFFFFF',
        filterbkcolor: '#303233',
        neutru: '#828282',
        verifyBox: "#FFCDCD",
        recipetext: '#0c1821',
        bkgcolordimmed: '#303233',
        txtcolordimmed: '#B4B4B4',
    },
    light: {
        bkgcolor: '#FF5348',
        txtcolor: '#0c1821',
        hoverbkgcolor: '#ee3326',
        footercolor: '#0C1821',
        hovercolor: '#FFFFFF',
        caseta: '#FF8878',
        corpcaseta: '#FFE7E2',
        border: '#000000',
        compreteta: '#FFD4D4',
        body: '#E9E9E9',
        hover: '#0000000a',
        profname: '#808080',
        navbar: '#ff5348',
        navbarcolor1: '#000000',
        navbarcolor2: '#FFFFFF',
        searchbar: '#FFFFFF',
        ubody: '#1C1C1C',
        filterbkcolor: '#F3F3F3',
        neutru: '#828282',
        verifyBox: "#FFCDCD",
        recipetext: '#0c1821',
        bkgcolordimmed: '#F3F3F3',
        txtcolordimmed: '#B4B4B4',
    },
}

export const ThemeContext = React.createContext({
    theme: themes.light,
    toggleTheme: () => {},
})