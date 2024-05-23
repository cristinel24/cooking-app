import React, { useState, useEffect } from 'react'

import RecipeData from './RecipeData'

import { getRecipe } from '../../services/recipe'
import { useNavigate, useParams } from 'react-router-dom'

import { ClipLoader } from 'react-spinners'

export default function Recipe() {
    const [recipeData, setRecipeData] = useState({})
    const [recipeLoading, setRecipeLoading] = useState(true)
    const [error, setError] = useState('')

    const { recipeId } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        const fetch = async () => {
            // temporary; TODO: proper error handling with actual error message
            try {
                const recipe = await getRecipe(recipeId)
                setRecipeData(recipe)
                setRecipeLoading(false)
            } catch (e) {
                navigate('/not-found')
            }
        }

        fetch()
    }, [])

    return (
        <>
            <ClipLoader
                // color={'blue'}
                className="loading"
                cssOverride={{
                    borderColor: 'var(--color-white)',
                    color: 'var(--color-white)',
                    alignSelf: 'center',
                }}
                width={'100%'}
                loading={recipeLoading}
                aria-label="Se încarcă..."
                data-testid="loader"
            />
            {error !== '' && <span>{error}</span>}
            {!recipeLoading && error === '' && (
                <div className="recipe-page-container">
                    <RecipeData recipeData={recipeData} setRecipeData={setRecipeData} />
                </div>
            )}
        </>
    )
}