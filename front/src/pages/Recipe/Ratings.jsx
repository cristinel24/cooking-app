import { RatingCard } from '../../components'
import { getRatings } from '../../services/rating'
import { useNavigate, useParams } from 'react-router-dom'
import InfiniteScroll from 'react-infinite-scroll-component'

import { getErrorMessage } from '../../utils/api'

import { useState, useEffect } from 'react'

export const Ratings = ({ recipeData }) => {
    const [results, setResults] = useState({
        start: 0,
        count: 1,
        ratings: [],
    })
    const [error, setError] = useState('')
    const [hasMore, setHasMore] = useState(true)

    // useEffect(() => {
    //     console.log(results.start + ' - ' + results.count)
    //     setHasMore(
    //         error.length > 0
    //             ? false
    //             : results.fetchedInitial === false || results.start < results.count
    //     )
    // }, [error, results])

    const editRating = async (data, id) => {
        console.log(data)
        setResults((ratingData) => {
            let newData = ratingData
            newData.ratings.find((obj) => obj.id === id).description = data.text
            return newData
        })
    }

    const deleteRating = async (id) => {
        setResults(results.ratings.filter((otherRating) => id !== otherRating.id))
        console.log(id)
    }

    const initialFetchCount = 40
    const fetchCount = 20

    useEffect(() => {
        let ignore = false
        const fetch = async () => {
            try {
                const result = await getRatings({
                    recipeId: recipeData.id,
                    start: results.start,
                    count: initialFetchCount,
                })
                if (!ignore) {
                    setResults((newResults) => ({
                        ...results,
                        fetchedInitial: true,
                        start: results.start + initialFetchCount,
                        count: result.count,
                        ratings: reduceRatingsToUniqueIds([
                            ...newResults.ratings,
                            ...result.ratings,
                        ]),
                    }))
                }
            } catch (e) {
                setResults((results) => ({ ...results, count: 0 }))
                setError(getErrorMessage(e))
            }
        }
        fetch()
        return () => {
            ignore = true
        }
    }, [])

    const reduceRatingsToUniqueIds = (array) =>
        Array.from(
            new Set(
                array.reduce((acc, rating) => {
                    const existingRating = acc.find((r) => r.id === rating.id)
                    if (!existingRating) {
                        acc.push(rating)
                    }
                    return acc
                }, [])
            )
        )

    const fetchMoreRatings = async () => {
        if (!results.fetchedInitial) {
            return
        }
        try {
            const result = await getRatings({
                recipeId: recipeData.id,
                start: results.start,
                count: fetchCount,
            })
            setResults((newResults) => ({
                ...newResults,
                start: results.start + fetchCount,
                ratings: reduceRatingsToUniqueIds([...newResults.ratings, ...result.ratings]),
            }))
        } catch (e) {
            setResults((results) => ({ ...results, count: 0 }))
            setError(getErrorMessage(e))
        }
    }

    return (
        <div className="recipe-page-ratings">
            <h3>Recenzii</h3>

            {
                <InfiniteScroll
                    className="recipe-page-ratings-container"
                    dataLength={results.ratings.length}
                    next={fetchMoreRatings}
                    hasMore={error.length > 0 ? false : results.start < results.count}
                    loader={<h4 style={{ textAlign: 'center' }}>Se încarcă...</h4>}
                    endMessage={
                        error.length > 0 ? (
                            <p style={{ textAlign: 'center' }}>
                                <b>{error}</b>
                            </p>
                        ) : (
                            <p style={{ textAlign: 'center' }}>
                                <b>Toate comentariile au fost încărcate.</b>
                            </p>
                        )
                    }
                >
                    {results.ratings.map((rating) => {
                        return (
                            <RatingCard
                                key={rating.id}
                                ratingData={rating}
                                onEdit={(data) => {
                                    editRating(data, rating.id)
                                }}
                                onDelete={() => {
                                    deleteRating(rating.id)
                                }}
                            />
                        )
                    })}
                </InfiniteScroll>
            }
        </div>
    )
}
