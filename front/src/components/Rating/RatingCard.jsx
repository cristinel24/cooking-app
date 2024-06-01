import { useState, useEffect, useContext } from 'react'
import './index.css'
import { RatingValue, ConfirmModal, Report } from '..'

import { IoIosArrowDown, IoIosArrowUp } from 'react-icons/io'
import { ClipLoader } from 'react-spinners'

import { timestampToRomanian, dateToTimestamp } from '../../utils/date'
import { getErrorMessage } from '../../utils/api'

import RatingButton from './RatingButton'
import RatingForm from './RatingForm'
import {
    addRatingReply as apiAddRatingReply,
    getRatingReplies as apiGetRatingReplies,
    editRating as apiEditRating,
    deleteRating as apiDeleteRating,
} from '../../services/rating'
import { UserContext } from '../../context'

const RatingCard = ({ ratingData, onEdit, onDelete }) => {
    const [showAllText, setShowAllText] = useState(false)
    const [showReplies, setShowReplies] = useState(false)
    const [showReplyForm, setShowReplyForm] = useState(false)
    const [editing, setEditing] = useState(false)

    const [replyResults, setReplyResults] = useState({ start: 0, total: 0, data: [] })
    const [error, setError] = useState('')
    const [hasMore, setHasMore] = useState(true)
    const [loading, setLoading] = useState(false)

    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)

    const [isReportVisible, setIsReportVisible] = useState(false)

    const { token, user, loggedIn } = useContext(UserContext)

    const fetchCount = 20
    const shortRatingLength = 300

    useEffect(() => {
        setHasMore(error.length > 0 ? false : replyResults.start < replyResults.total)
    }, [replyResults, error])

    useEffect(() => {
        let ignore = false
        const ignoreTrue = () => {
            ignore = true
        }

        if (ratingData.parentType !== 'recipe') {
            // don't even try to fetch replies
            return ignoreTrue
        }

        setLoading(true)

        const fetch = async () => {
            try {
                const result = await apiGetRatingReplies({
                    ratingId: ratingData.id,
                    start: replyResults.start,
                    count: fetchCount,
                })
                if (!ignore) {
                    setReplyResults((newResults) => ({
                        ...replyResults,
                        start: replyResults.start + fetchCount,
                        total: result.total,
                        data: [...newResults.data, ...result.data],
                    }))
                }
            } catch (e) {
                setError(getErrorMessage(e))
            } finally {
                setLoading(false)
            }
        }

        fetch()

        return ignoreTrue
    }, [])

    const fetchMoreReplies = async () => {
        if (loading) {
            return
        }
        try {
            setLoading(true)
            const result = await apiGetRatingReplies({
                ratingId: ratingData.id,
                start: replyResults.start,
                count: fetchCount,
            })
            setReplyResults((newResults) => ({
                ...replyResults,
                start: replyResults.start + fetchCount,
                total: result.total,
                data: [...newResults.data, ...result.data],
            }))
        } catch (e) {
            setError(getErrorMessage(e))
        } finally {
            setLoading(false)
        }
    }

    const toggleEdit = () => {
        setEditing(!editing)
    }

    const handleEdit = async (data) => {
        // raw async callback; to be passed to RatingForm
        const response = await onEdit(data)
        toggleEdit()
    }

    const editRating = async (data, id) => {
        // raw async callback; to be passed to RatingForm
        await apiEditRating(id, token)

        setReplyResults((results) => {
            let newData = { ...results }
            let index = newData.data.findIndex((obj) => obj.id === id)
            if (index !== -1) {
                newData.data[index] = {
                    ...newData.data[index],
                    description: data.description,
                    updatedAt: dateToTimestamp(Date.now()),
                }
            }
            return newData
        })
    }

    const toggleDeleteModal = () => {
        setIsDeleteModalOpen(!isDeleteModalOpen)
    }

    const handleConfirmDeleteModal = async () => {
        await onDelete()
        toggleDeleteModal()
    }

    const deleteReply = async (id) => {
        // raw async callback; to be passed to RatingForm
        await apiDeleteRating(id, token)

        setReplyResults((newResults) => ({
            ...newResults,
            data: newResults.data.filter((otherRating) => id !== otherRating.id),
        }))
    }

    const handleAddReply = async (data) => {
        // raw async callback; to be passed to RatingForm
        const response = await apiAddRatingReply(ratingData.id, data, token)

        // aka: if all of the replies before this new one have been fetched
        if (replyResults.start >= replyResults.total) {
            setReplyResults((newResults) => ({
                ...newResults,
                total: newResults.total + 1,
                data: [...newResults.data, response],
            }))
        }

        toggleAddReply()
    }

    const toggleAddReply = () => {
        setShowReplyForm(!showReplyForm)
        if (!showReplies) {
            setShowReplies(true)
        }
    }

    const onSendReport = async () => {
        try {
            // TODO: api call
        } catch (e) {
            setError(getErrorMessage(e))
        } finally {
            setIsReportVisible(!isReportVisible)
        }
    }

    const toggleReport = () => {
        setIsReportVisible(!isReportVisible)
    }

    return (
        <div className="rating-card">
            <ConfirmModal
                isOpen={isDeleteModalOpen}
                onConfirm={handleConfirmDeleteModal}
                onCancel={toggleDeleteModal}
                confirmText={'Confirmare'}
                cancelText={'Anulare'}
            >
                <p>Sigur doriți să ștergeți această recenzie?</p>
            </ConfirmModal>
            {isReportVisible && <Report onSend={onSendReport} onCancel={toggleReport} />}
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
                            Postat pe {timestampToRomanian(ratingData.createdAt)}
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
                                {replyResults.data.length > 0 && (
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
                                {loggedIn() && ratingData.parentType !== 'rating' && (
                                    <RatingButton onClick={toggleAddReply}>Răspunde</RatingButton>
                                )}
                                {loggedIn() && user?.id && user?.id === ratingData?.author?.id && (
                                    <RatingButton onClick={toggleEdit}>Editează</RatingButton>
                                )}
                                {loggedIn() && user?.id && user?.id === ratingData?.author?.id && (
                                    <RatingButton onClick={toggleDeleteModal}>Șterge</RatingButton>
                                )}

                                {!(loggedIn() && ratingData?.id === user?.id) && (
                                    <RatingButton onClick={setIsReportVisible}>
                                        Raportează
                                    </RatingButton>
                                )}
                            </div>
                        </>
                    ) : (
                        <RatingForm
                            id={`${ratingData.id}-edit`}
                            onSubmit={handleEdit}
                            defaultValues={{
                                description: ratingData.description,
                                ...(ratingData?.parentType === 'recipe' &&
                                ratingData?.rating !== undefined
                                    ? { rating: ratingData.rating }
                                    : {}),
                            }}
                            onCancel={toggleEdit}
                        />
                    )}
                </div>
            </div>
            {ratingData.parentType === 'recipe' && (
                <>
                    {showReplies &&
                        (error === '' ? (
                            <div className="rating-card-replies">
                                {showReplyForm && (
                                    <RatingForm
                                        id={`${ratingData.id}-add-reply`}
                                        onSubmit={handleAddReply}
                                        defaultValues={{
                                            description: '',
                                        }}
                                        onCancel={toggleAddReply}
                                    />
                                )}
                                {replyResults.data.length > 0 &&
                                    replyResults.data.map((reply) => {
                                        return (
                                            <RatingCard
                                                key={reply.id}
                                                ratingData={reply}
                                                onEdit={(data) => {
                                                    editRating(data, reply.id)
                                                }}
                                                onDelete={() => {
                                                    deleteReply(reply.id)
                                                }}
                                            ></RatingCard>
                                        )
                                    })}
                                {!loading && hasMore && (
                                    <RatingButton onClick={fetchMoreReplies}>
                                        Afișează mai multe răspunsuri
                                    </RatingButton>
                                )}
                                <ClipLoader
                                    className="loading"
                                    cssOverride={{
                                        borderColor: 'var(--text-color)',
                                        color: 'var(--text-color)',
                                        alignSelf: 'center',
                                    }}
                                    width={'100%'}
                                    loading={loading}
                                    aria-label="Se încarcă..."
                                    data-testid="loader"
                                />
                            </div>
                        ) : (
                            <div className="form-error">{error}</div>
                        ))}
                </>
            )}
        </div>
    )
}

export default RatingCard
