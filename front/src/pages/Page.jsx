import React from 'react'

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
    Filters,
    ShowMenu,
    Report,
    ReportRecipe,
    Categories,
} from '../components'

import { MdWavingHand } from 'react-icons/md'

//pagina noua
function Page() {
    let userName = 'Utilizator'
    let userNumber = '#1'
    let content =
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. '
    let date = '23.07.2023 18:00 AM'
    let view = 'Vizualizare profil'
    const pathPage = '/'
    const handleClick = () => {}
    const mostViewedRecipes = [
        [
            'Title1',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title2',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title3',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title4',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title5',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title6',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title7',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title8',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
        [
            'Title9',
            'Author1',
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia!',
        ],
    ]

    const func1 = () => {}
    return (
        <>
            {/* <Categories
                name="Cele mai vizualizate"
                recipes={mostViewedRecipes}
                id="recipe-view-1"
            /> */}

            {/* <ReportRecipe /> */}
            {/* <Report /> */}
            {/* <ShowMenu /> */}

            {/* <PreviewRecipe
                title="Titlu reteta"
                tags={['tag1', 'tag2', 'tag3', 'tag4', 'tag5']}
                allergens={['apa', 'gluten', 'porumb', 'alergen4', 'alergen5']}
                description="Descrierea Rețetei"
            /> */}

            {/* <AdminBox
                userName={userName}
                userNumber={userNumber}
                content={content}
                date={date}
                view={view}
                pathPage={pathPage}
                handleClick={handleClick}
            /> */}

            {/* <Navbar /> */}

            {/* <UserProfile /> */}

            {/* <Footer /> */}

            {/* componenta de reteta */}
            {/* <Recipe
                title="Title1"
                author="Author1"
                image="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis."
            ></Recipe> */}

            {/* <PopUpChat /> */}

            {/* <PageButton children="Buna" path={pathPage} className="da" /> */}

            <ActionButton onClick={func1} text="buna" Icon={MdWavingHand} />
        </>
    )
}

export default Page
