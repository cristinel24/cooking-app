import { useContext, useEffect, useState } from 'react'
import { getSavedRecipes as apiGetSavedRecipes, getSavedRecipes } from '../../services/profile'
import { UserContext } from '../../context'
import { useNavigate, useOutletContext } from 'react-router-dom'
import { getErrorMessage } from '../../utils/api'
import { RecipeCard } from '../../components'
import InfiniteScroll from 'react-infinite-scroll-component'

export default function Favorites() {
    const { profileData } = useOutletContext()
    const { token, user, loggedIn } = useContext(UserContext)

    const navigate = useNavigate()

    if (!loggedIn() || user.id !== profileData.id) {
        navigate('/not-found')
    }

    const [results, setResults] = useState({ start: 0, total: 0, data: [] })
    const [error, setError] = useState('')

    const fetchCount = 20

    const fetchRecipeCards = async () => {
        try {
            const result = await getSavedRecipes(profileData?.id, results.start, fetchCount, token)
            setResults((results) => ({
                ...results,
                start: results.start + fetchCount,
                total: result.total,
                data: [...results.data, ...result.data],
            }))
        } catch (e) {
            // if fetching fails, set results.count to 0 so that InfiniteScroll thinks there
            // are no more results
            setError(getErrorMessage(e))
        }
    }

    const fetchMore = async () => {
        if (results.fetchedInitial) {
            return
        }
        await fetchRecipeCards()
        console.log('fetched in scroll')
    }

    useEffect(() => {
        console.log('in effect?')
        let ignore = false

        const fetch = async () => {
            try {
                const result = await getSavedRecipes(
                    profileData?.id,
                    results.start,
                    fetchCount,
                    token
                )
                if (!ignore) {
                    setResults((results) => ({
                        ...results,
                        start: results.start + fetchCount,
                        fetchedInitial: true,
                        total: result.total,
                        data: [...results.data, ...result.data],
                    }))
                }
            } catch (e) {
                setError(getErrorMessage(e))
            }
        }

        fetch()
        return () => {
            ignore = true
        }
    }, [])

    return (
        <div>
            <InfiniteScroll
                className="feed"
                dataLength={results.data.length}
                next={fetchMore}
                hasMore={error.length > 0 ? false : results.start <= results.total}
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
                    />
                ))}
            </InfiniteScroll>
        </div>
    )
}
