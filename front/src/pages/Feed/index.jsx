import { useContext, useEffect, useState } from 'react'

import './index.css'
import { Dropdown, RecipeCard } from '../../components'
import { UserContext } from '../../context'
import { useLocation, useNavigate } from 'react-router-dom'
import InfiniteScroll from 'react-infinite-scroll-component'
import { searchRecipes } from '../../services/search'
import { getErrorMessage } from '../../utils/api'
import { deleteRecipe, saveRecipe } from '../../services/recipe'

export default function Feed() {
    const navigate = useNavigate()
    const { pathname } = useLocation()

    const { user, loggedIn, token } = useContext(UserContext)

    const feeds = [
        { name: 'popular', alias: '', params: { sort: 'viewCount', order: 'desc' } },
        { name: 'best', params: { sort: 'ratingAvg', order: 'desc' } },
        { name: 'new', params: { sort: 'createdAt', order: 'desc' } },
    ].concat(
        loggedIn()
            ? [
                  {
                      name: 'followed',
                      params: {
                          filters: {
                              authors: {
                                  /* TODO: get the followed authors of the current user and put their names here */
                              },
                          },
                      },
                  },
                  // 'recommended',
              ]
            : []
    )

    const [feed, setFeed] = useState(
        feeds.find(
            (feed) =>
                feed.name === pathname.substring(1) ||
                ('alias' in feed && feed.alias === pathname.substring(1))
        )
    )
    const [results, setResults] = useState({ count: 1, recipes: [] })
    const [error, setError] = useState('')

    useEffect(() => {
        if (feed.name !== pathname.substring(1)) {
            // reset state if page changed
            setResults({ count: 1, recipes: [] })
            setError('')
            navigate(`/${feed.name}`)
        } else if (results.recipes.length == 0) {
            // after page change, this code should get triggered
            let ignore = false

            searchRecipes({
                ...feed.params,
                query: '',
                start: results.recipes.length,
                count: 10,
            })
                .then((result) => {
                    if (!ignore) {
                        setResults((results) => ({
                            ...result,
                            recipes: [...results.recipes, ...result.recipes],
                        }))
                    }
                })
                .catch((e) => setError(getErrorMessage(e)))

            return () => {
                ignore = true
            }
        }
    }, [navigate, pathname, feed])

    const fetchRecipes = async () => {
        try {
            console.log('fetching...')
            const result = await searchRecipes({
                query: '',
                start: results.recipes.length,
                count: 10,
            })
            setResults((results) => ({
                ...result,
                recipes: [...results.recipes, ...result.recipes],
            }))
            console.log('fetched')
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
                for (const recipe of results.recipes) {
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
                recipes: results.recipes.filter((recipe) => recipe.id !== id),
            }))
        } catch (e) {
            // can't do nothing here
            return
        }
    }

    return (
        <div>
            <h1>Explorează rețetele</h1>
            <Dropdown options={feeds} option={feed} setOption={setFeed} />
            <InfiniteScroll
                className="feed"
                dataLength={results.recipes.length} //This is important field to render the next data
                next={fetchRecipes}
                hasMore={error.length > 0 ? false : results.recipes.length < results.count}
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
                {results.recipes.map((recipe) => (
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
