import './index.css'
import ActionButton from '../ActionButton'
import useResizeWindow from '../../hooks/useResizeWindow'
import { MdWavingHand } from 'react-icons/md'

/**
 * @typedef {Object} PrepareDescriptionReturns
 * @property {string} descrip
 * @property {boolean} isShowMoreToRead
 */

/**
 *
 * @param {string | undefined} description Recipe's description.
 * @param {number} width Screen width.
 * @returns {PrepareDescriptionReturns}
 */

const prepareDescription = (description, width) => {
    // Check if the description is null or undefined.
    // If it is replace it with empty string.
    const descrip = description ?? 'Descriere reteta'
    // Trim the description to a realistic size.
    const trimmedDescription =
        width > 1100 ? descrip.slice(0, 350) : descrip.slice(0, 200)
    // If the trimming changed the length of the string that means
    // we have more to read.
    const isShowMoreToRead = trimmedDescription.length != descrip.length

    return {
        descrip: trimmedDescription,
        isShowMoreToRead,
    }
}

/**
 * @param {string} title Recipe's title
 * @param {string[]} tags Recipe's tags
 * @param {string[]} allergens Recipe's allergens
 * @param {string} description Recipe's description
 * @param {number} width Width of screen
 */

const PreviewRecipe = ({ title, tags, allergens, description }) => {
    const width = useResizeWindow()
    const { descrip, isShowMoreToRead } = prepareDescription(description, width)

    const handleViewRecipe = () => {
        console.log('Change route')
        // handle change route.
    }

    return (
        <div className="preview-recipe-container">
            <div className="preview-recipe-details-container">
                <h1 className="preview-recipe-title">{title ?? 'Titlu'}</h1>
                <div className="preview-recipe-tags">
                    <div className="preview-tags-title">Tag-uri:</div>
                    {tags &&
                        tags.map((tag, index) => (
                            <div key={index} className="preview-tag">
                                {tag}
                            </div>
                        ))}
                </div>
                <div className="preview-recipe-allergens">
                    <div className="preview-allergens-title">Alergeni:</div>
                    {allergens &&
                        allergens.map((allergen, index) => (
                            <div key={index} className="preview-allergen">
                                {allergen}
                            </div>
                        ))}
                </div>
                <div className="preview-recipe-description">
                    <div className="preview-description-title">Descriere:</div>
                    <div className="preview-description-text">
                        {descrip} {isShowMoreToRead && '...'}
                    </div>
                </div>
                <ActionButton
                    onClick={handleViewRecipe}
                    text="Vizualizare reteta"
                    Icon={MdWavingHand}
                />
            </div>
        </div>
    )
}

export default PreviewRecipe
