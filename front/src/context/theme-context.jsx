import React from "react";

export const themes = {
  dark: {
    bkgcolor: "#FF5348",
    txtcolor: "#FFFFFF",
    hoverbkgcolor: "#02080D",
    footercolor: "#FFFFFF",
    hovercolor: "#0c1821",
    caseta: "#FF8878",
    corpcaseta: "#FFE7E2",
    border: "#000000",
    compreteta: "#FFD4D4",
    body: "#1C1C1C",
    hover: "#0000000a",
    profname: "#808080",
    navbar: "#ff5348",
    navbarcolor1: "#FFFFFF",
    navbarcolor2: "#000000",
    searchbar: "#FFFFFF",
  },
  light: {
    bkgcolor: "#FF5348",
    txtcolor: "#0c1821",
    hoverbkgcolor: "#ee3326",
    footercolor: "#0C1821",
    hovercolor: "#FFFFFF",
    caseta: "#FF8878",
    corpcaseta: "#FFE7E2",
    border: "#000000",
    compreteta: "#FFD4D4",
    body: "#E9E9E9",
    hover: "#0000000a",
    profname: "#808080",
    navbar: "#ff5348",
    navbarcolor1: "#000000",
    navbarcolor2: "#FFFFFF",
    searchbar: "#FFFFFF",
  },
};

export const ThemeContext = React.createContext({
  theme: themes.light,
  toggleTheme: () => {},
});
