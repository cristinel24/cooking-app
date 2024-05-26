import { RatingCard } from '../../components'
import { getRatings } from '../../services/rating'
import { useNavigate, useParams } from 'react-router-dom'

import { ClipLoader } from 'react-spinners'

import { useState, useEffect } from 'react'

export const Ratings = ({ recipeData }) => {
    const [ratings, setRatings] = useState([])
    const [loadingRatings, setLoadingRatings] = useState(true)
    const navigate = useNavigate()

    const editRating = async (data, id) => {
        console.log(data)
        setRatings((ratingData) => {
            let newData = ratingData
            newData.find((obj) => obj.id === id).description = data.text
            return newData
        })
    }

    const deleteRating = async (id) => {
        setRatings(ratings.filter((otherRating) => id !== otherRating.id))
        console.log(id)
    }

    useEffect(() => {
        let ignore = false

        // todo: paginate ratings...
        getRatings(recipeData.id)
            .then((ratings) => {
                if (!ignore) {
                    console.log(ratings)
                    setRatings(ratings)
                }
            })
            .then(() => setLoadingRatings(false))
            .catch((e) => setRepliesError('error'))

        return () => {
            ignore = true
        }
    }, [])

    return (
        <div className="recipe-page-comments">
            <h3>Recenzii</h3>

            <div className="recipe-page-comments-container">
                {loadingRatings && (
                    <ClipLoader
                        className="loading"
                        cssOverride={{
                            borderColor: 'var(--text-color)',
                            color: 'var(--text-color)',
                            alignSelf: 'center',
                        }}
                        width={'100%'}
                        loading={loadingRatings}
                        aria-label="Se încarcă..."
                        data-testid="loader"
                    />
                )}
                {ratings.map((rating) => (
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
                ))}
            </div>
        </div>
    )
}
