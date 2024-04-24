import React, { useEffect, useState } from "react";

import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"; //necesara pt redirectionarea de la o pag la alta

import { ThemeContext, themes } from "./context";

import {
  ActionButton,
  PageButton,
  PopUpChat,
  Recipe,
  Footer,
  UserProfile,
  Navbar,
  AdminBox,
  PreviewRecipe,
} from "./components";

import Page from "./pages/Page";

function App() {
  const titlu = "BUNA SIUAAA!:>";
  const pathPage = "/Page";

  localStorage.setItem("theme", "dark");

  const [theme, setTheme] = useState(
    themes[localStorage.getItem("theme")] || ""
  );

  useEffect(() => {
    if (theme === "") {
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        setTheme(themes.dark);
        localStorage.setItem("theme", "dark");
      } else {
        setTheme(themes.light);
        localStorage.setItem("theme", "light");
      }
    }
  }, []);

  useEffect(() => {
    for (const color in theme) {
      document.documentElement.style.setProperty(
        `--${color}`,
        `${theme[color]}`
      );
    }
  }, [theme]);

  const toggleTheme = () => {
    if (theme === themes.light) {
      setTheme(themes.dark);
      localStorage.setItem("theme", "dark");
    } else {
      setTheme(themes.light);
      localStorage.setItem("theme", "light");
    }
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme,
      }}
    >
      {/* preview recipe---neterminat */}
      {/* <PreviewRecipe
        title="Titlu reteta"
        tags={["tag1", "tag2", "tag3", "tag4", "tag5"]}
        allergens={["apa", "gluten", "porumb", "alergen4", "alergen5"]}
        description="Descrierea Rețetei"
      /> */}

      {/* <AdminBox /> */}

      <Navbar />

      {/* <UserProfile
        first_name="Popescu"
        last_name="Ion"
        followers="70"
        following="6"
        img="../public/ProfileImage.avif"
      /> */}

      <Footer />

      {/* componenta de reteta */}
      {/* <Recipe
        title="Title1"
        author="Author1"
        image="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
        description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis."
      ></Recipe> */}

      {/* chatbot */}
      {/* <PopUpChat /> */}

      {/* buton cu actiune */}
      {/* <ActionButton onClick={toggleTheme} text={titlu} /> */}

      {/* buton de directionat la pagini */}
      {/* <Router>
        <div>
          <Routes>
            <Route path={pathPage} element={<Page />} />
          </Routes>
          <PageButton title={titlu} path={pathPage} />
        </div>
      </Router> */}
    </ThemeContext.Provider>
  );
}

export default App;
