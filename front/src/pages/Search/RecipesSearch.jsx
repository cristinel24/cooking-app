import { useContext, useEffect, useState } from 'react'

import { searchRecipes } from '../../services/search'
import { getErrorMessage } from '../../utils/api'
import { deleteRecipe, saveRecipe } from '../../services/recipe'
import { UserContext } from '../../context'
import { RecipeCard } from '../../components'
import InfiniteScroll from 'react-infinite-scroll-component'
import { useOutletContext } from 'react-router-dom'

export default function RecipesSearch() {
    const [results, setResults] = useOutletContext()
    const { user, token } = useContext(UserContext)
    const [error, setError] = useState('')

    useEffect(() => {
        const fetch = async () => {
            try {
                const result = await searchRecipes({
                    query: '',
                    start: results.items.length,
                    count: 10,
                })
                if (!ignore) {
                    setResults((results) => ({
                        ...result,
                        items: [...results.items, ...result.recipes],
                    }))
                }
            } catch (e) {
                // if fetching fails, set results.count to 0 so that InfiniteScroll thinks there
                // are no more results
                setError(getErrorMessage(e))
            }
        }
        let ignore = false
        fetch()
        return () => {
            ignore = true
        }
    }, [])

    const fetchRecipes = async (ignore = false) => {
        try {
            const result = await searchRecipes({
                query: '',
                start: results.items.length,
                count: 10,
            })
            if (!ignore) {
                setResults((results) => ({
                    ...result,
                    items: [...results.items, ...result.recipes],
                }))
            }
        } catch (e) {
            // if fetching fails, set results.count to 0 so that InfiniteScroll thinks there
            // are no more results
            setError(getErrorMessage(e))
        }
    }

    const onFavorite = async (id) => {
        try {
            await saveRecipe(id, token)

            setResults((results) => {
                for (const recipe of results.items) {
                    if (recipe.id === id) {
                        recipe.favorite = !recipe.favorite
                    }
                }
                return results
            })
        } catch (e) {
            // can't do nothing here
            return
        }
    }

    const onRemove = async (id) => {
        try {
            await deleteRecipe(id, token)

            setResults((results) => ({
                ...results,
                items: results.items.filter((recipe) => recipe.id !== id),
            }))
        } catch (e) {
            // can't do nothing here
            return
        }
    }

    return (
        <div className="search-page-results">
            <InfiniteScroll
                className="search-page-results-container"
                dataLength={results.items.length} //This is important field to render the next data
                next={fetchRecipes}
                hasMore={error.length > 0 ? false : results.items.length < results.count}
                loader={<h4>Loading...</h4>}
                endMessage={
                    error.length > 0 ? (
                        <p style={{ textAlign: 'center' }}>
                            <b>{error}</b>
                        </p>
                    ) : (
                        <p style={{ textAlign: 'center' }}>
                            <b>No more recipes for you</b>
                        </p>
                    )
                }
            >
                {results.items.map((recipe) => (
                    <RecipeCard
                        key={recipe.id}
                        recipe={recipe}
                        owned={recipe.author.id === user.id}
                        onFavorite={onFavorite}
                        onRemove={onRemove}
                    />
                ))}
            </InfiniteScroll>
        </div>
    )
}
