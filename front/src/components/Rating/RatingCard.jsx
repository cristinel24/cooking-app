import { useState, useEffect } from 'react'
import './index.css'
import { RatingValue } from '..'

import { IoIosArrowDown, IoIosArrowUp } from 'react-icons/io'

import { dateToRomanian } from '../../utils/date'
import { getErrorMessage } from '../../utils/api'

import RatingButton from './RatingButton'
import RatingForm from './RatingForm'
import { getRatingReplies } from '../../services/rating'

const RatingCard = ({ ratingData, onEdit, onDelete }) => {
    const [showAllText, setShowAllText] = useState(false)
    const [showReplies, setShowReplies] = useState(false)
    const [editing, setEditing] = useState(false)

    const [results, setResults] = useState({ start: 0, count: 1, replies: [] })
    const [error, setError] = useState('')
    const [hasMore, setHasMore] = useState(true)
    const [loading, setLoading] = useState(false)

    const fetchCount = 20

    useEffect(() => {
        setHasMore(error.length > 0 ? false : results.start < results.count)
    }, [results, error])

    useEffect(() => {
        let ignore = false
        const ignoreTrue = () => {
            ignore = true
        }

        if (ratingData.parentType !== 'recipe') {
            return ignoreTrue
        }

        setLoading(true)

        const fetch = async () => {
            try {
                const result = await getRatingReplies({
                    ratingId: ratingData.id,
                    start: results.start,
                    count: fetchCount,
                })
                if (!ignore) {
                    setResults((newResults) => ({
                        ...results,
                        start: results.start + fetchCount,
                        count: result.count,
                        replies: [...newResults.replies, ...result.replies],
                    }))
                }
            } catch (e) {
                setError(getErrorMessage(e))
            }
        }

        fetch()

        return ignoreTrue
    }, [])

    const toggleEdit = () => {
        setEditing(!editing)
    }

    const handleEdit = async (data) => {
        toggleEdit()
        onEdit(data)
    }

    const editRating = async (data, id) => {
        console.log(data)
        setResults((newResults) => {
            let newData = newResults
            newData.replies.find((obj) => obj.id === id).description = data.text
            return newData
        })
    }

    const deleteRating = async (id) => {
        setResults((newResults) => ({
            ...newResults,
            replies: newResults.replies.filter((otherRating) => id !== otherRating.id),
        }))
        console.log(id)
    }

    const shortRatingLength = 300
    return (
        <div className="rating-card">
            <div className="rating-card-main-container">
                <div className="rating-card-image">
                    <img src={ratingData.author.icon} />
                </div>
                <div className="rating-card-content">
                    <div className="rating-card-data">
                        <div className="rating-card-user">
                            <h4 className="rating-card-display-name">
                                {ratingData.author.displayName}
                            </h4>
                            <span className="rating-card-username">
                                @{ratingData.author.username}
                            </span>
                        </div>
                        <div className="rating-card-date">
                            Postat pe {dateToRomanian(ratingData.createdAt)}
                            <em>
                                {ratingData.updatedAt !== ratingData.createdAt ? ' (editat)' : ''}
                            </em>
                        </div>
                    </div>
                    {!editing ? (
                        <>
                            <div className="rating-card-description">
                                {ratingData?.rating > 0 && (
                                    <div className="rating-card-rating">
                                        <RatingValue value={ratingData.rating} showValue={false} />
                                    </div>
                                )}
                                <p>
                                    {showAllText ||
                                    ratingData.description.length <= shortRatingLength
                                        ? ratingData.description
                                        : ratingData.description.slice(0, shortRatingLength) +
                                          '...'}
                                </p>
                            </div>
                            <div className="rating-card-buttons">
                                {ratingData.description.length > shortRatingLength && (
                                    <RatingButton
                                        onClick={() => {
                                            setShowAllText(!showAllText)
                                        }}
                                    >
                                        {showAllText ? (
                                            <>
                                                Arată mai puțin <IoIosArrowUp />
                                            </>
                                        ) : (
                                            <>
                                                Arată mai mult <IoIosArrowDown />
                                            </>
                                        )}
                                    </RatingButton>
                                )}
                                {results.replies.length > 0 && (
                                    <RatingButton
                                        onClick={() => {
                                            setShowReplies(!showReplies)
                                        }}
                                    >
                                        {showReplies ? (
                                            <>
                                                Ascunde răspunsuri <IoIosArrowUp />
                                            </>
                                        ) : (
                                            <>
                                                Arată răspunsuri <IoIosArrowDown />
                                            </>
                                        )}
                                    </RatingButton>
                                )}
                                {ratingData.parentType !== 'rating' && (
                                    <RatingButton>Răspunde</RatingButton>
                                )}
                                <RatingButton onClick={toggleEdit}>Editează</RatingButton>
                                <RatingButton onClick={onDelete}>Șterge</RatingButton>
                            </div>
                        </>
                    ) : (
                        <RatingForm
                            id={ratingData.id}
                            onSubmit={handleEdit}
                            defaultValues={{
                                text: ratingData.description,
                                ...(ratingData?.rating !== undefined
                                    ? { rating: ratingData.rating }
                                    : {}),
                            }}
                            onCancel={toggleEdit}
                        />
                    )}
                </div>
            </div>
            {ratingData.parentType === 'recipe' &&
                showReplies &&
                (error === '' ? (
                    results.replies.length > 0 && (
                        <div className="rating-card-replies">
                            {results.replies.map((reply) => {
                                return (
                                    <RatingCard
                                        key={reply.id}
                                        ratingData={reply}
                                        onEdit={(data) => {
                                            editRating(data, reply.id)
                                        }}
                                        onDelete={() => {
                                            deleteRating(reply.id)
                                        }}
                                    ></RatingCard>
                                )
                            })}
                        </div>
                    )
                ) : (
                    <>{error}</>
                ))}
        </div>
    )
}

export default RatingCard
