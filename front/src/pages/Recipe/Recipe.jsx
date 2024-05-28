import React, { useState, useEffect } from 'react'

import RecipeData from './RecipeData'
import { Ratings } from './Ratings'

import { getRecipe } from '../../services/recipe'
import { useNavigate, useParams } from 'react-router-dom'

import { ClipLoader } from 'react-spinners'
import { getErrorMessage } from '../../utils/api'

export default function Recipe() {
    const [recipeData, setRecipeData] = useState({})
    const [recipeLoading, setRecipeLoading] = useState(true)

    const [error, setError] = useState('')

    const { recipeId } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        const fetch = async () => {
            try {
                const recipe = await getRecipe(recipeId)
                setRecipeData(recipe)
            } catch (e) {
                if (e.response?.status === 404) {
                    navigate('/not-found')
                } else {
                    setError(getErrorMessage(e))
                }
            } finally {
                setRecipeLoading(false)
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
            {error !== '' && <span class="form-error">{error}</span>}
            {!recipeLoading && error === '' && (
                <>
                    <div className="recipe-page-container">
                        <RecipeData recipeData={recipeData} setRecipeData={setRecipeData} />
                        <Ratings recipeData={recipeData} />
                    </div>
                </>
            )}
        </>
    )
}
