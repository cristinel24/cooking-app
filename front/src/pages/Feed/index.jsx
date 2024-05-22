import { useContext, useEffect, useState } from "react";

import './index.css'
import { Dropdown, RecipeCard } from "../../components";
import { UserContext } from "../../context";
import { useLocation, useNavigate } from "react-router-dom";
import InfiniteScroll from "react-infinite-scroll-component";

export default function Feed() {
    const navigate = useNavigate()
    const { pathname } = useLocation()

    const { user } = useContext(UserContext)
    const { loggedIn } = useContext(UserContext)
    const [feed, setFeed] = useState(pathname.substring(1))
    const recipe = {
        id: "8c",
        author: {
            id: "21",
            username: "matthew49",
            displayName: "Kimberly Shaw",
            icon: "https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png",
            roles: 0,
            ratingAvg: 1.5,
        },
        title: "Meatballs with sauce",
        description: "Expert create half this increase system. Such weight attorney enough. Newspaper public fast wall fill.\nKeep his network her. Race wish this camera even.",
        prepTime: 8205,
        allergens: [
            "asparagus",
            "dhansak spice mix"
        ],
        tags: [],
        thumbnail: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
        viewCount: 0,
        favorite: false,
    }

    const [recipes, setRecipes] = useState([...Array(10).keys()].map(id => {
        return {
            ...recipe,
            author: {
                ...recipe.author,
                id: id % 4 === 0 ? user.id : "21",
            },
            id,
        }
    }))

    const feeds = [
        "popular",
        "best",
        "new"
    ].concat(loggedIn() ? [
        "favorite",
        "followed",
        "recommended",
    ] : [])

    const onFavorite = (id) => {
        // TODO: use api to add recipe to favorites

        setRecipes(recipes => {
            for (const recipe of recipes) {
                if (recipe.id === id) {
                    recipe.favorite = !recipe.favorite
                }
            }
            return recipes
        })

        console.log(recipes)
    }

    const onRemove = (id) => {
        // TODO: use api to remove recipe

        setRecipes(recipes => recipes.filter(recipe => recipe.id !== id))
    }

    useEffect(() => {
        if (feed !== pathname.substring(1)) {
            navigate(`/${feed}`)
        }
    }, [navigate, pathname, feed])

    return (
        <div>
            <h1>Explorează rețetele</h1>
            <Dropdown options={feeds} option={feed} setOption={setFeed} />
            <InfiniteScroll
                className="feed"
                dataLength={recipes.length} //This is important field to render the next data
                next={() =>
                    setRecipes(
                        recipes => recipes.concat([...Array(10).keys()].map(id => {
                            return {
                                ...recipe,
                                author: {
                                    ...recipe.author,
                                    id: (recipes.length + id) % 4 === 0 ? user.id : "21",
                                },
                                id: recipes.length + id,
                            }
                        }))
                    )
                }
                hasMore={true}
                loader={<h4>Loading...</h4>}
                endMessage={
                    <p style={{ textAlign: 'center' }}>
                        <b>No more recipes for you</b>
                    </p>
                }
            >
                {recipes.map(recipe =>
                    <RecipeCard
                        key={recipe.id}
                        recipe={recipe}
                        owned={recipe.author.id === user.id}
                        onFavorite={onFavorite}
                        onRemove={onRemove}
                    />
                )}
            </InfiniteScroll>
        </div>
    )
}
