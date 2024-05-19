import { useState } from 'react'
import { FaEdit, FaHeart, FaTrash } from 'react-icons/fa'
import { IoIosTime } from 'react-icons/io'
import { Link } from 'react-router-dom'

import './index.css'
import { Rating } from '../../components'
import { prepTimeDisplayText } from '../../utils/recipeData'

export default function RecipeCard({ recipe, owned, onFavorite, onRemove }) {
    const [favorite, setFavorite] = useState(recipe.favorite)

    const onFavoriteInternal = () => {
        setFavorite((favorite) => !favorite)
        onFavorite(recipe.id)
    }

    return (
        <div className="recipe-card">
            <a href={`/recipe/${recipe.id}`}>
                <img
                    src={`${recipe.thumbnail}`}
                    className="recipe-card-image"
                    alt="recipe"
                />
            </a>
            <div className="recipe-card-details">
                <div className="recipe-card-details-title-and-options">
                    <a
                        className="recipe-card-details-title"
                        href={`/recipe/${recipe.id}`}
                    >
                        {recipe.title}
                    </a>
                    <div className="recipe-card-details-options">
                        {owned && onRemove && (
                            <FaTrash
                                className="recipe-card-trash-icon"
                                onClick={() => onRemove(recipe.id)}
                            />
                        )}
                        {owned && (
                            <Link to={`/recipe/${recipe.id}/edit`}>
                                <FaEdit className="recipe-card-edit-icon" />
                            </Link>
                        )}
                    </div>
                </div>
                <div className="recipe-card-details-author-time-rating">
                    <p className="recipe-card-details-author">
                        Autor:{' '}
                        <a href={`/profile/${recipe.author.id}`}>
                            {recipe.author.displayName}
                        </a>
                    </p>
                    <div className="recipe-card-details-time-and-rating">
                        <p className="recipe-card-details-time">
                            <IoIosTime /> {prepTimeDisplayText(recipe.prepTime)}
                        </p>
                        <Rating ratingValue={recipe.author.ratingAvg} />
                    </div>
                </div>
                {onFavorite && (
                    <button
                        type="button"
                        className="recipe-card-details-favorite"
                        onClick={onFavoriteInternal}
                    >
                        <FaHeart
                            className={
                                favorite
                                    ? 'recipe-card-heart-icon-favorite'
                                    : 'recipe-card-heart-icon-not-favorite'
                            }
                        />
                        <p>
                            {favorite
                                ? 'Elimină din favorite'
                                : 'Adaugă la favorite'}
                        </p>
                    </button>
                )}
            </div>
        </div>
    )
}
