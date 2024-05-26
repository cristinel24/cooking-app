import { useState, useEffect } from 'react'
import './index.css'
import { RatingValue } from '..'

import { IoIosArrowDown, IoIosArrowUp } from 'react-icons/io'

import { useForm } from 'react-hook-form'

import { RatingButton } from './RatingButton'
import { getRatingReplies } from '../../services/rating'

const RatingCard = ({ ratingData }) => {
    const [showAllText, setShowAllText] = useState(false)
    const [editing, setEditing] = useState(false)

    const [replies, setReplies] = useState([])
    const [showReplies, setShowReplies] = useState(false)
    const [repliesError, setRepliesError] = useState('')
    const [loadingReplies, setLoadingReplies] = useState(false)

    useEffect(() => {
        let ignore = false
        const ignoreTrue = () => {
            ignore = true
        }

        if (ratingData.parentType !== 'recipe') {
            return ignoreTrue
        }

        setLoadingReplies(true)

        getRatingReplies(ratingData.id)
            .then((result) => {
                if (!ignore) {
                    setReplies(result)
                }
            })
            .then(() => {
                setLoadingReplies(false)
            })
            .catch((e) => setRepliesError('mda'))

        return () => {
            ignore = true
        }
    }, [])

    const toggleEdit = () => {
        setEditing(!editing)
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
                        {ratingData.rating && ratingData.rating > 0 && (
                            <div className="rating-card-rating">
                                <RatingValue value={ratingData.rating} showValue={false} />
                            </div>
                        )}
                        <div className="rating-card-user">
                            <h4 className="rating-card-display-name">Sabina Prodan</h4>
                            <span className="rating-card-username">@câtrtoj</span>
                        </div>
                        <div className="rating-card-date">ora 123:3534 data 2335:#$ :#$@:#</div>
                    </div>
                    <div className="rating-card-description">
                        {!editing ? (
                            <p>
                                {showAllText || ratingData.description.length <= shortRatingLength
                                    ? ratingData.description
                                    : ratingData.description.slice(0, shortRatingLength) + '...'}
                            </p>
                        ) : (
                            <form></form>
                        )}
                    </div>
                    <div className="rating-card-buttons">
                        {!editing ? (
                            <>
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
                                {replies.length > 0 && (
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
                                <RatingButton>Răspunde</RatingButton>
                                <RatingButton onClick={toggleEdit}>Editează</RatingButton>
                            </>
                        ) : (
                            <>mda</>
                        )}
                    </div>
                </div>
            </div>
            {ratingData.parentType === 'recipe' &&
                showReplies &&
                (repliesError !== '' ? (
                    <div className="rating-card-replies">
                        {replies.map((reply, index) => {
                            return <RatingCard key={index} ratingData={reply}></RatingCard>
                        })}
                    </div>
                ) : (
                    <>{repliesError}</>
                ))}
        </div>
    )
}

export default RatingCard
