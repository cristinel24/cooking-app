import { useContext, useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import InfiniteScroll from 'react-infinite-scroll-component'

import './index.css'
import { Dropdown, RecipeCard } from '../../components'
import { UserContext } from '../../context'
import { searchRecipes } from '../../services/search'
import { getErrorMessage } from '../../utils/api'
import { deleteRecipe, saveRecipe } from '../../services/recipe'

export default function Feed() {
    const navigate = useNavigate()
    const { pathname } = useLocation()

    const { user, loggedIn, token } = useContext(UserContext)

    const feeds = [
        {
            name: 'cele mai vizualizate',
            path: 'popular',
            alias: '',
            params: { sort: 'viewCount', order: 'desc' },
        },
        {
            name: 'cu cele mai bune recenzii',
            path: 'best',
            params: { sort: 'ratingAvg', order: 'desc' },
        },
        { name: 'cele mai recente', path: 'new', params: { sort: 'createdAt', order: 'desc' } },
    ].concat(
        // loggedIn()
        //     ? [
        //           {
        //               name: 'de la cei urmăriți',
        //               path: 'followed',
        //               params: {
        //                   filters: {
        //                       authors: {
        //                           /* TODO: get the followed authors of the current user and put their names here */
        //                       },
        //                   },
        //               },
        //           },
        //           // 'recommended',
        //       ]
        //     : []
    )

    const [feed, setFeed] = useState(
        feeds.find(
            (feed) =>
                feed.path === pathname.substring(1) ||
                ('alias' in feed && feed.alias === pathname.substring(1))
        )
    )
    const [results, setResults] = useState({ total: 1, data: [] })
    const [error, setError] = useState('')

    useEffect(() => {
        if (feed.path !== pathname.substring(1)) {
            // reset state if page changed
            setResults({ total: 1, data: [] })
            setError('')
            navigate(`/${feed.path}`)
        } else if (results.data.length == 0) {
            let ignore = false
            // after page change, this code should get triggered
            const fetch = async () => {
                try {
                    const result = await searchRecipes({
                        query: '',
                        start: results.data.length,
                        count: 10,
                    })
                    console.log(result)
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

            fetch()
            return () => {
                ignore = true
            }
        }
    }, [navigate, pathname, feed])

    const fetchRecipes = async () => {
        try {
            const result = await searchRecipes({
                query: '',
                start: results.data.length,
                count: 10,
            })
            console.log(result)
            setResults((results) => ({
                ...result,
                data: [...results.data, ...result.data],
            }))
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
        <div>
            <h1>Explorează rețetele</h1>
            <Dropdown options={feeds} option={feed} setOption={setFeed} />
            <InfiniteScroll
                className="feed"
                dataLength={results.data.length}
                next={fetchRecipes}
                hasMore={error.length > 0 ? false : results.data.length < results.total}
                loader={<h4 style={{ textAlign: 'center' }}>Se încarcă...</h4>}
                endMessage={
                    error.length > 0 ? (
                        <p style={{ textAlign: 'center' }}>
                            <b>{error}</b>
                        </p>
                    ) : (
                        <p style={{ textAlign: 'center' }}>
                            <b>Toate rețetele au fost încărcate.</b>
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
