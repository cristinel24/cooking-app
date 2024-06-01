import { InfoModal, RatingCard, RatingForm } from '../../components'
import InfiniteScroll from 'react-infinite-scroll-component'

import { getErrorMessage } from '../../utils/api'

import { dateToTimestamp } from '../../utils/date'

import {
    getRatings as apiGetRatings,
    addRating as apiAddRating,
    editRating as apiEditRating,
    deleteRating as apiDeleteRating,
} from '../../services/rating'

import { useState, useEffect, useContext } from 'react'

import { UserContext } from '../../context'

export const Ratings = ({ recipeData }) => {
    const [results, setResults] = useState({
        start: 0,
        total: 1,
        data: [],
    })
    const [fetchError, setFetchError] = useState('')
    const [error, setError] = useState('')

    const { token, user } = useContext(UserContext)

    const initialFetchCount = 40
    const fetchCount = 20

    useEffect(() => {
        let ignore = false
        const fetch = async () => {
            try {
                const result = await apiGetRatings({
                    recipeId: recipeData.id,
                    start: results.start,
                    count: initialFetchCount,
                })
                if (!ignore) {
                    setResults((newResults) => ({
                        ...newResults,
                        start: newResults.start + initialFetchCount,
                        total: result.total,
                        data: reduceRatingsToUniqueIds([...newResults.data, ...result.data]),
                    }))
                }
            } catch (e) {
                setResults((results) => ({ ...results, total: 0 }))
                setFetchError(getErrorMessage(e))
            }
        }
        fetch()
        return () => {
            ignore = true
        }
    }, [])

    // TODO: check if it keeps the order...
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
        try {
            const result = await apiGetRatings({
                recipeId: recipeData.id,
                start: results.start,
                count: fetchCount,
            })
            setResults((newResults) => ({
                ...newResults,
                start: results.start + fetchCount,
                data: reduceRatingsToUniqueIds([...newResults.data, ...result.data]),
            }))
        } catch (e) {
            setResults((results) => ({ ...results, total: 0 }))
            setFetchError(getErrorMessage(e))
        }
    }

    const addRating = async (data) => {
        // raw async callback, to be passed to RatingForm
        const response = await apiAddRating(recipeData.id, data, token)

        // push back in ratings
        setResults((results) => ({
            ...results,
            start: results.start + 1,
            total: results.total + 1,
            data: reduceRatingsToUniqueIds([response, ...results.data]),
        }))
    }

    const editRating = async (formData, id) => {
        // raw async callback, to be passed to RatingCard -> RatingForm
        await apiEditRating(id, formData, token)

        setResults((results) => {
            let newResults = { ...results }
            let index = newResults.data.findIndex((obj) => obj.id === id)
            if (index !== -1) {
                newResults.data[index] = {
                    ...newResults.data[index],
                    description: formData.description,
                    rating: formData.rating,
                    updatedAt: dateToTimestamp(Date.now()),
                }
            }
            return newResults
        })
    }

    const deleteRating = async (id) => {
        // non-raw; not handled in RatingForm; must be handled outside
        try {
            const response = await apiDeleteRating(id, token)

            setResults((newResults) => ({
                ...newResults,
                total: newResults.total - 1,
                data: newResults.data.filter((otherRating) => id !== otherRating.id),
            }))
        } catch (e) {
            setError(getErrorMessage(e))
        }
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
                            description: '',
                            rating: 0,
                        }}
                    />
                    <InfiniteScroll
                        className="recipe-page-ratings-container"
                        dataLength={results.data.length}
                        next={fetchMoreRatings}
                        hasMore={fetchError.length > 0 ? false : results.start < results.total}
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
                        {results.data.map((rating) => {
                            return (
                                <RatingCard
                                    key={rating.id}
                                    ratingData={rating}
                                    onEdit={async (data) => {
                                        await editRating(data, rating.id)
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
