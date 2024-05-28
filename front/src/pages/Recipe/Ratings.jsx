import { InfoModal, RatingCard, RatingForm } from '../../components'
import { getRatings } from '../../services/rating'
import InfiniteScroll from 'react-infinite-scroll-component'

import { getErrorMessage } from '../../utils/api'

import { useState, useEffect } from 'react'

export const Ratings = ({ recipeData }) => {
    const [results, setResults] = useState({
        start: 0,
        count: 1,
        ratings: [],
    })
    const [fetchError, setFetchError] = useState('')
    const [error, setError] = useState('')

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
                        ...newResults,
                        fetchedInitial: true,
                        start: newResults.start + initialFetchCount,
                        count: result.count,
                        ratings: reduceRatingsToUniqueIds([
                            ...newResults.ratings,
                            ...result.ratings,
                        ]),
                    }))
                }
            } catch (e) {
                setResults((results) => ({ ...results, count: 0 }))
                setFetchError(getErrorMessage(e))
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
            setFetchError(getErrorMessage(e))
        }
    }

    const addRating = async (data) => {
        // todo: API call to add comment + call to get most recent comment and add it to the list..
        // they don't have to be *perfectly* up to datee
        // throw new Error('mda')
        console.log(data)
    }

    const editRating = async (data, id) => {
        // TODO: API CALL

        console.log(data)
        setResults((ratingData) => {
            let newData = { ...ratingData }
            let index = newData.ratings.findIndex((obj) => obj.id === id)
            if (index !== -1) {
                newData.ratings[index] = {
                    ...newData.ratings[index],
                    description: data.text,
                    rating: data.rating,
                }
            }
            return newData
        })
    }

    const deleteRating = async (id) => {
        // TODO: API CALL
        try {
        } catch (e) {
            setError(getErrorMessage(e))
        }

        setResults((newResults) => ({
            ...newResults,
            count: newResults.count - 1,
            ratings: newResults.ratings.filter((otherRating) => id !== otherRating.id),
        }))
        console.log(id)
    }

    const onModalClose = () => {
        setError('')
    }

    return (
        <div className="recipe-page-ratings">
            <InfoModal isOpen={Boolean(error)} onClose={onModalClose} text={error}>
                <p>{error}</p>
            </InfoModal>
            <h2>Recenzii</h2>
            <h4>Adaugă o recenzie...</h4>

            {
                <div className="recipe-page-ratings-with-form">
                    <RatingForm
                        id={`${recipeData.id}-add-rating`}
                        onSubmit={addRating}
                        confirmText="Adaugă recenzie"
                        defaultValues={{
                            text: '',
                            rating: 0,
                        }}
                    />
                    <InfiniteScroll
                        className="recipe-page-ratings-container"
                        dataLength={results.ratings.length}
                        next={fetchMoreRatings}
                        hasMore={fetchError.length > 0 ? false : results.start < results.count}
                        loader={<h4 style={{ textAlign: 'center' }}>Se încarcă...</h4>}
                        endMessage={
                            fetchError.length > 0 ? (
                                <p style={{ textAlign: 'center' }}>
                                    <b>{fetchError}</b>
                                </p>
                            ) : (
                                <p style={{ textAlign: 'center' }}>
                                    <b>Toate recenziile au fost încărcate.</b>
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
                </div>
            }
        </div>
    )
}
