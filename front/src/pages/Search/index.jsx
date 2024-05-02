import React from 'react'
import './index.css'
import { useState } from 'react'
import { MdFoodBank } from 'react-icons/md'
import { FaRegUser } from 'react-icons/fa'
import { Page } from '../../components'
import ActionButton from '../../components/ActionButton'
import SearchFilter from '../../components/SearchFilter'
import User from '../../components/User'
import Recipe from '../../components/Recipe'

const Search = () => {
    const [showUsers, setShowUsers] = useState(false)
    const [allData, setData] = useState({
        users: [
            {
                name: 'Name',
                posts: '/',
                image: 'https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
            {
                name: 'Name',
                posts: '/',
                image: 'https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
            {
                name: 'Name',
                posts: '/',
                image: 'https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
            {
                name: 'Name',
                posts: '/',
                image: 'https://images.pexels.com/photos/1264210/pexels-photo-1264210.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
        ],
        recipes: [
            {
                title: 'Title',
                author: 'Author',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
            {
                title: 'Title',
                author: 'Author',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
            {
                title: 'Title',
                author: 'Author',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
            {
                title: 'Title',
                author: 'Author',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea.',
            },
        ],
    })
    // allData.recipes.length = 0
    // allData.users.length = 0

    const handleClickRecipes = () => {
        setShowUsers(false)
    }

    const handleClickUsers = () => {
        setShowUsers(true)
    }

    const handleFilterIngredients = (ingredients) => {
        const filteredUsers = allData.users.filter((user) =>
            user.name.toLowerCase().includes(ingredients.toLowerCase())
        )
        const filteredRecipes = allData.recipes.filter((recipe) =>
            recipe.title.toLowerCase().includes(ingredients.toLowerCase())
        )

        setData({
            users: filteredUsers,
            recipes: filteredRecipes,
        })
    }

    return (
        <Page>
            <div className="search">
                <div className="search-filter-box">
                    <strong>Filtre</strong>
                    <SearchFilter
                        onIngredientsFilter={handleFilterIngredients}
                        onTagsFilter={handleFilterIngredients}
                        onAllergensFilter={handleFilterIngredients}
                        onAuthorsFilter={handleFilterIngredients}
                    />
                </div>
                {allData.users.length === 0 && allData.recipes.length === 0 && (
                    <div className="search-results">
                        <div className="search-results-no-found">
                            No users or recipes found.
                        </div>
                    </div>
                )}
                {allData.users.length !== 0 && allData.recipes.length !== 0 && (
                    <div className="search-results">
                        <div className="search-results-buttons">
                            <ActionButton
                                onClick={handleClickRecipes}
                                text="Retete"
                                Icon={MdFoodBank}
                            />
                            <ActionButton
                                onClick={handleClickUsers}
                                text="Utilizatori"
                                Icon={FaRegUser}
                            />
                        </div>
                        <div className="search-results-content">
                            <div
                                className="search-results-content-users"
                                style={{
                                    display: showUsers ? 'flex' : 'none',
                                }}
                            >
                                {allData.users.map((user, index) => (
                                    <User
                                        key={index}
                                        name={user.name}
                                        posts={user.posts}
                                        image={user.image}
                                        description={user.description}
                                    />
                                ))}
                            </div>
                            <div
                                className="search-results-content-recipes"
                                style={{
                                    display: showUsers ? 'none' : 'flex',
                                }}
                            >
                                {allData.recipes.map((recipe, index) => (
                                    <Recipe
                                        key={index}
                                        title={recipe.title}
                                        author={recipe.author}
                                        image={recipe.image}
                                        description={recipe.description}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                )}
                {allData.recipes.length !== 0 && allData.users.length === 0 && (
                    <div className="search-results">
                        <div className="search-results-content">
                            <div className="search-results-content-recipes">
                                {allData.recipes.map((recipe, index) => (
                                    <Recipe
                                        key={index}
                                        title={recipe.title}
                                        author={recipe.author}
                                        image={recipe.image}
                                        description={recipe.description}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                )}
                {allData.users.length !== 0 && allData.recipes.length === 0 && (
                    <div className="search-results">
                        <div className="search-results-content">
                            <div className="search-results-content-users">
                                {allData.users.map((user, index) => (
                                    <User
                                        key={index}
                                        name={user.name}
                                        posts={user.posts}
                                        image={user.image}
                                        description={user.description}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </Page>
    )
}

export default Search