import { useContext, useEffect, useState } from "react";

import './index.css'
import { Dropdown, Page, RecipeCard } from "../../components";
import { UserContext } from "../../context";
import { Navigate, useNavigate, useParams } from "react-router-dom";

export default function Feed() {
    const { user } = useContext(UserContext)
    const { loggedIn } = useContext(UserContext)
    const [feed, setFeed] = useState(type)
    const [recipes, setRecipes] = useState([...Array(10).keys()].map(id => {
        return {
            id,
            author: {
                id: id % 4 === 0 ? user.id : "21",
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
    }))

    const navigate = useNavigate();

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
        if (feed !== type) {
            navigate(`/${feed}`)
        }
    }, [navigate, type, feed])

    return (
        <div>
            <h1>Explorează rețetele</h1>
            <Dropdown options={feeds} option={feed} setOption={setFeed} />
            <div className="feed">
                {recipes.map(recipe =>
                    <RecipeCard
                        key={recipe.id}
                        recipe={recipe}
                        owned={recipe.author.id === user.id}
                        onFavorite={onFavorite}
                        onRemove={onRemove}
                    />
                )}
            </div>
        </div>
    )
}
