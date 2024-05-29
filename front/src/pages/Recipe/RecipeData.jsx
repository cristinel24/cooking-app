import { useState } from 'react'
import { Link } from 'react-router-dom'
import { RatingValue, Tag, Button, Report, InfoModal } from '../../components'
import './index.css'
import { prepTimeDisplayText, ratingToNumber } from '../../utils/recipeData'
import { IoIosTime } from 'react-icons/io'
import { FaUser, FaEye } from 'react-icons/fa'
import { getErrorMessage } from '../../utils/api'

export default function RecipeData({ recipeData, onFavorite }) {
    const [isReportVisible, setIsReportVisible] = useState(false)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const onPressFavorite = async () => {
        if (loading) {
            return
        }
        try {
            setLoading(true)
            await onFavorite()
        } catch (e) {
            setError(getErrorMessage(e))
        } finally {
            setLoading(false)
        }
    }

    const onCloseModal = () => {
        setError('')
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
        <div className="recipe-page-data">
            <InfoModal onClose={onCloseModal} isOpen={error.length > 0}>
                <p className="form-error">{error}</p>
            </InfoModal>
            {isReportVisible && <Report onSend={onSendReport} onCancel={toggleReport} />}
            <div className="recipe-page-grid-container">
                <div className="recipe-page-data">
                    <h1>{recipeData.title}</h1>

                    <div className="recipe-page-metadata">
                        <div className="recipe-page-icon-data">
                            <IoIosTime />
                            <span>{prepTimeDisplayText(recipeData.prepTime)}</span>
                        </div>
                        <div className="recipe-page-icon-data">
                            <FaUser />
                            <Link
                                to={recipeData.author.id ? `/profile/${recipeData.author.id}` : '/'}
                            >
                                {recipeData.author.displayName}
                            </Link>
                        </div>
                        {recipeData.viewCount !== undefined && (
                            <div className="recipe-page-icon-data">
                                <FaEye />

                                {recipeData.viewCount}
                            </div>
                        )}

                        <RatingValue
                            className="recipe-page-rating-stars"
                            value={ratingToNumber(recipeData.ratingSum, recipeData.ratingCount)}
                        />

                        <button
                            type="button"
                            className="recipe-page-button-report"
                            onClick={toggleReport}
                        >
                            Raportează
                        </button>
                    </div>
                    <div>{recipeData.description}</div>
                    <div className="recipe-page-tags">
                        Tag-uri:
                        <div className="recipe-page-tags-container">
                            {recipeData.tags.map((tag, index) => (
                                <Tag className="recipe-page-tag" key={index} text={tag} />
                            ))}
                        </div>
                    </div>

                    <div className="recipe-page-tags">
                        Alergeni:
                        <div className="recipe-page-tags-container">
                            {recipeData.allergens.map((tag, index) => (
                                <Tag className="recipe-page-tag" key={index} text={tag} />
                            ))}
                        </div>
                    </div>
                </div>

                <div className="recipe-page-image-container">
                    <div className="recipe-page-image">
                        <img src={recipeData.thumbnail} alt="recipe image" />
                    </div>
                    {recipeData.isFavorite !== undefined && (
                        <Button
                            className={'recipe-page-button-favorite'}
                            text={
                                recipeData.isFavorite
                                    ? 'Elimină din favorite'
                                    : 'Adaugă la favorite'
                            }
                            onClick={onPressFavorite}
                        />
                    )}
                </div>
            </div>

            <div className="recipe-page-grid-container">
                <div className="recipe-page-ingredients">
                    <h2>Ingrediente</h2>
                    <div className="recipe-page-ingredients-container">
                        {recipeData.ingredients.map((ingredient, index) => (
                            <p key={index}>{ingredient}</p>
                        ))}
                    </div>
                </div>

                <div className="recipe-page-steps">
                    <h2>Mod de preparare </h2>
                    <div className="recipe-page-steps-container">
                        {recipeData.steps.map((step, index) => (
                            <div key={index} className="recipe-page-step">
                                <div className="recipe-page-step-index">
                                    <span>{index}</span>
                                </div>
                                <p
                                    className="recipe-page-step-content"
                                    dangerouslySetInnerHTML={{
                                        __html: step,
                                    }}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
