import React, { useState, useEffect } from 'react'

import RecipeData from './RecipeData'

import { getRecipe } from '../../services/recipe'
import { useNavigate, useParams } from 'react-router-dom'

import { ClipLoader } from 'react-spinners'
import FormStars from '../../components/Form/FormStars'

import { RatingCard } from '../../components'
import { getRatings } from '../../services/rating'

export default function Recipe() {
    const [recipeData, setRecipeData] = useState({})
    const [recipeLoading, setRecipeLoading] = useState(true)

    const [ratings, setRatings] = useState([])
    const [ratingsLoading, setRatingsLoading] = useState(true)

    const [error, setError] = useState('')

    const { recipeId } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        const fetch = async () => {
            try {
                const recipe = await getRecipe(recipeId)
                setRecipeData(recipe)
            } catch (e) {
                navigate('/not-found')
            } finally {
                setRecipeLoading(false)
            }

            try {
                const ratings = await getRatings(recipeData.id)
                setRatings(ratings)
            } catch (e) {
                navigate('/not-found')
            } finally {
                setRatingsLoading(false)
            }
        }

        fetch()
    }, [])

    return (
        <>
            <ClipLoader
                className="loading"
                cssOverride={{
                    borderColor: 'var(--text-color)',
                    color: 'var(--text-color)',
                    alignSelf: 'center',
                }}
                width={'100%'}
                loading={recipeLoading}
                aria-label="Se încarcă..."
                data-testid="loader"
            />
            {error !== '' && <span>{error}</span>}
            {!recipeLoading && error === '' && (
                <>
                    <div className="recipe-page-container">
                        <RecipeData recipeData={recipeData} setRecipeData={setRecipeData} />
                    </div>

                    <div className="recipe-page-comments">
                        <h3>Comentarii</h3>
                        {ratings.map((rating, index) => (
                            <RatingCard key={index} ratingData={rating} />
                        ))}
                    </div>
                </>
            )}
        </>
    )
}
