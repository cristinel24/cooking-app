import './index.css'
import Rating from '../Rating'
import { IoIosTime } from 'react-icons/io'
import { FaHeart, FaEdit, FaTrash } from 'react-icons/fa'
export default function RecipeCard({
    title,
    recipePicture,
    authorName,
    authorLink,
    recipeLink,
    rating,
    prepTime,
    onFavorite,
    onRemove,
    onEdit,
}) {
    const prepTimeDisplayText = (() => {
        const prepTimeHours = Math.floor(prepTime / 60)
        const prepTimeMinutes = prepTime % 60
        switch (true) {
            case prepTimeHours > 0 && prepTimeMinutes > 0:
                return `${prepTimeHours} ${
                    prepTimeHours === 1 ? 'ora' : 'ore'
                } ${prepTimeMinutes} ${
                    prepTimeMinutes === 1 ? 'minut' : 'minute'
                }`
            case prepTimeHours > 0:
                return `${prepTimeHours} ${prepTimeHours === 1 ? 'ora' : 'ore'}`
            default:
                return `${prepTimeMinutes} ${
                    prepTimeMinutes === 1 ? 'minut' : 'minute'
                }`
        }
    })()

    return (
        <div className="recipe-card">
            <a href={recipeLink}>
                <img src={recipePicture} className="recipe-card-image" />
            </a>
            <div className="recipe-card-details">
                <div className="recipe-card-details-title-and-options">
                    <a className="recipe-card-details-title" href={recipeLink}>
                        {title}
                    </a>
                    <div className="recipe-card-details-options">
                        {onRemove && (
                            <FaTrash
                                className="recipe-card-trash-icon"
                                onClick={onRemove}
                            />
                        )}
                        {onEdit && (
                            <FaEdit
                                className="recipe-card-edit-icon"
                                onClick={onEdit}
                            />
                        )}
                    </div>
                </div>
                <p className="recipe-card-details-author">
                    Autor: <a href={authorLink}>{authorName}</a>
                </p>
                <div className="recipe-card-details-time-and-rating">
                    <p className="recipe-card-details-time">
                        <IoIosTime /> {prepTimeDisplayText}
                    </p>
                    <Rating ratingValue={rating} />
                </div>
                <div
                    className="recipe-card-details-favorite"
                    onClick={onFavorite}
                >
                    <FaHeart className="recipe-card-heart-icon" />
                    <p>Adaugă la favorite</p>
                </div>
            </div>
        </div>
    )
}
