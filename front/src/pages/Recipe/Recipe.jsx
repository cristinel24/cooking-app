import { useContext, useState, useEffect } from 'react'
import { UserContext } from '../../context'

import RecipeData from './RecipeData'
import { Ratings } from './Ratings'

import { getRecipe } from '../../services/recipe'
import { useNavigate, useParams } from 'react-router-dom'

import { ClipLoader } from 'react-spinners'
import { getErrorMessage } from '../../utils/api'
import { saveRecipe as apiSaveRecipe, unsaveRecipe as apiUnsaveRecipe } from '../../services/recipe'

export default function Recipe() {
    const [recipeData, setRecipeData] = useState({})
    const [recipeLoading, setRecipeLoading] = useState(true)

    const [error, setError] = useState('')

    const { recipeId } = useParams()
    const navigate = useNavigate()

    const { token, user } = useContext(UserContext)

    useEffect(() => {
        const fetch = async () => {
            try {
                const recipe = await getRecipe(recipeId, token)
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

    const onFavorite = async () => {
        if (recipeData.isFavorite) {
            await apiUnsaveRecipe(user.id, recipeData.id, token)
        } else {
            await apiSaveRecipe(user.id, recipeData.id, token)
        }
        setRecipeData((recipeData) => {
            return {
                ...recipeData,
                isFavorite: !recipeData.isFavorite,
            }
        })
    }

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
            {error !== '' && <span className="form-error">{error}</span>}
            {!recipeLoading && error === '' && (
                <>
                    <div className="recipe-page-container">
                        <RecipeData recipeData={recipeData} onFavorite={onFavorite} />
                        <Ratings recipeData={recipeData} />
                    </div>
                </>
            )}
        </>
    )
}
