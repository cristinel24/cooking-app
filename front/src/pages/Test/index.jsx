import React from 'react'

import {
    ActionButton,
    PageButton,
    PopUpChat,
    Recipe,
    Footer,
    UserProfile,
    Navbar,
    ReportCard,
    PreviewRecipe,
    Filters,
    ShowMenu,
    Report,
    ReportRecipe,
    Categories,
} from '../../components'

import { MdWavingHand } from 'react-icons/md'

//pagina noua
function Test() {
    let user = 'Tania'
    let title = 'Utilizator: ' + user
    let nr = 1
    let number = '#' + nr
    let reason = 'Conținut instigător la ură sau abuziv'
    let date = '23.07.2023 18:00 AM'
    let view = 'Vizualizare profil'
    const pathPageView = '/'
    const handleClickRead = () => {}
    let specificAction = 'Restricționare'
    const handleClickSpecificAction = () => {}
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
            {/* <ReportCard
                title={title}
                number={number}
                reason={reason}
                date={date}
                view={view}
                pathPageView={pathPageView}
                handleClickRead={handleClickRead}
                specificAction={specificAction}
                handleClickSpecificAction={handleClickSpecificAction}
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

            <PageButton path={pathPage} className="da">
                Buna
            </PageButton>

            <ActionButton onClick={func1} text="buna" Icon={MdWavingHand} />
        </>
    )
}

export default Test
