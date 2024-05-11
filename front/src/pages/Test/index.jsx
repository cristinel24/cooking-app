import React, { useState } from 'react'

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
    Tag,
    TagSelector,
    RecipeCard,
    UserCard,
} from '../../components'

import { MdWavingHand } from 'react-icons/md'

//pagina noua
function Test() {
    const [tags, setTags] = useState([])
    const [favorite, setFavorite] = useState(false)

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

    // Function to add a tag to the tags array
    const addTag = (tag) => {
        if (!tags.includes(tag)) {
            setTags([...tags, tag])
        }
    }

    // Function to remove a tag from the tags array
    const removeTag = (tagToRemove) => {
        setTags(tags.filter((tag) => tag !== tagToRemove))
    }

    // Function to search for similar tags
    const searchTags = (searchTag) => {
        return ['suggestionA', 'suggestionB', 'suggestionC']
    }
    const func1 = () => {}
    const handleFavorite = () => {
        setFavorite(!favorite)
        console.log('Favorite')
    }
    const handleRemove = () => {
        console.log('Remove')
    }
    const handleEdit = () => {
        console.log('Edit')
    }
    return (
        <>
            {/* <RecipeCard
                title="Reteta cu sushi sushi sushi sushisushi sushisushi sushi"
                recipePicture="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                authorName="Ioana"
                authorLink="./Login"
                recipeLink="./Login"
                rating={3.8}
                prepTime={30}
                favorite={favorite}
                onFavorite={handleFavorite}
                onRemove={handleRemove}
                onEdit={handleEdit}
            />

            <RecipeCard
                title="Reteta cu sushi sushi "
                recipePicture="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                authorName="Ioana"
                authorLink="./Login"
                recipeLink="./Login"
                rating={3.8}
                prepTime={30}
                favorite={favorite}
                onFavorite={handleFavorite}
                onRemove={handleRemove}
                onEdit={handleEdit}
            />

            <RecipeCard
                title="Chec pufos"
                recipePicture="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                authorName="Sabina"
                authorLink="./Login"
                recipeLink="./Login"
                rating={2.1}
                prepTime={73}
            /> */}

            {/*

            <UserCard
                displayName="Ana"
                username="username"
                rating={3.6}
                link="./Register"
                profilePicture="https://images.unsplash.com/photo-1501869150797-9bbb64f782fd?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            /> */}

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

            {/* <PageButton path={pathPage} className="da">
                Buna
            </PageButton>

            <ActionButton onClick={func1} text="buna" Icon={MdWavingHand} /> */}
            {/* <TagSelector
                tags={tags}
                addTag={addTag}
                removeTag={removeTag}
                searchTags={searchTags}
            /> */}
        </>
    )
}

export default Test
