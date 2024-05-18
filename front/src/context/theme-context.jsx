import React from 'react'

export const themes = {
    dark: {
        bgColor: '#FF5348',
        textColor: '#FFFFFF',
        hoverBgColor: '#02080D',
        footerBgColor: '#FFFFFF',
        cardColor: '#FF8878',
        cardBgColor: '#FFE7E2',
        borderColor: '#000000',
        bodyBgColor: '#1C1C1C',
        profileNameColor: '#808080',
        navbarBgColor: '#FF5348',
        navbarColorPrimary: '#FFFFFF',
        navbarColorSecondary: '#000000',
        searchbarBgColor: '#FFFFFF',
        reportBgColor: '#FFFFFF',
        filterBgColor: '#303233',
        cancelBgColor: '#828282',
        bgColorDimmed: '#303233',
        textColorDimmed: '#B4B4B4',
    },
    light: {
        bgColor: '#FF5348',
        textColor: '#0C1821',
        hoverBgColor: '#EE3326',
        footerBgColor: '#0C1821',
        cardColor: '#FF8878',
        cardBgColor: '#FFE7E2',
        borderColor: '#000000',
        bodyBgColor: '#E9E9E9',
        profileNameColor: '#808080',
        navbarBgColor: '#FF5348',
        navbarColorPrimary: '#000000',
        navbarColorSecondary: '#FFFFFF',
        searchbarBgColor: '#FFFFFF',
        reportBgColor: '#1C1C1C',
        filterBgColor: '#F3F3F3',
        cancelBgColor: '#828282',
        bgColorDimmed: '#F3F3F3',
        textColorDimmed: '#B4B4B4',
    },
}

export const ThemeContext = React.createContext({
    theme: themes.light,
    toggleTheme: () => {},
})
