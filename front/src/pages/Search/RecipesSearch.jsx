import { useContext, useEffect, useState } from 'react'

import { searchRecipes } from '../../services/search'
import { getErrorMessage } from '../../utils/api'
import { deleteRecipe, saveRecipe } from '../../services/recipe'
import { UserContext } from '../../context'
import { RecipeCard } from '../../components'
import InfiniteScroll from 'react-infinite-scroll-component'
import { useOutletContext } from 'react-router-dom'
import { useSearch } from '../../hooks/useSearch'

export default function RecipesSearch() {
    const [results, setResults] = useOutletContext()
    const { user, token } = useContext(UserContext)
    const [error, setError] = useState('')
    const { query, sort, order, filters } = useSearch()

    useEffect(() => {
        const fetch = async () => {
            try {
                const result = await searchRecipes({
                    query,
                    sort,
                    order,
                    filters,
                    start: results.data.length,
                    count: 10,
                })
                if (!ignore) {
                    setResults((results) => ({
                        ...result,
                        data: [...results.data, ...result.data],
                    }))
                }
            } catch (e) {
                // if fetching fails, set results.total to 0 so that InfiniteScroll thinks there
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
                query,
                sort,
                order,
                filters,
                start: results.data.length,
                count: 10,
            })
            if (!ignore) {
                setResults((results) => ({
                    ...result,
                    data: [...results.data, ...result.data],
                }))
            }
        } catch (e) {
            // if fetching fails, set results.total to 0 so that InfiniteScroll thinks there
            // are no more results
            setError(getErrorMessage(e))
        }
    }

    const onFavorite = async (id) => {
        try {
            await saveRecipe(id, token)

            setResults((results) => {
                for (const recipe of results.data) {
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
                data: results.data.filter((recipe) => recipe.id !== id),
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
                dataLength={results.data.length} //This is important field to render the next data
                next={fetchRecipes}
                hasMore={error.length > 0 ? false : results.data.length < results.total}
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
                {results.data.map((recipe) => (
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
