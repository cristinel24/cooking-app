import { useState } from 'react'
import {
    Footer,
    Navbar,
    PreviewRecipe,
    Recipe,
    ShowMenu,
} from '../../components'
import './index.css'
import { recipes } from './constants'
import useResizeWindow from '../../hooks/useResizeWindow'
import usePopup from './usePopup'
import Popup from './Popup'

const UnloggedUsers = () => {
    const width = useResizeWindow()
    const [selectedRecipe, setSelectedRecipe] = useState(null)
    const [isOpen, setIsOpen] = usePopup()
    const buildRecipePreview = () => {
        if (selectedRecipe == null) {
            return null
        }

        return (
            <PreviewRecipe
                title={selectedRecipe.title}
                description={selectedRecipe.description}
                tags={selectedRecipe.tags}
                allergens={selectedRecipe.allergens}
            />
        )
    }
    const handleClickOnRecipe = (recipe) => {
        if (width < 900) {
            setIsOpen(true)
            setSelectedRecipe(recipe)
            return
        }
        if (recipe.id == selectedRecipe?.id) {
            setSelectedRecipe(null)
        } else {
            setSelectedRecipe(recipe)
        }
    }

    return (
        <>
            <Popup isOpen={isOpen} setIsOpen={setIsOpen}>
                {buildRecipePreview()}
            </Popup>
            <div className="unloggedusers-layout">
                <div className="unloggedusers-filters">
                    <ShowMenu />
                </div>
                <div className="unloggedusers-recipes">
                    {recipes.map((recipe) => (
                        <div
                            onClick={() => handleClickOnRecipe(recipe)}
                            key={recipe.id}
                        >
                            <Recipe
                                title={recipe.title}
                                author={recipe.author}
                                image={recipe.image}
                                description={recipe.description}
                            />
                        </div>
                    ))}
                </div>
                {selectedRecipe && (
                    <div className="unloggedusers-preview">
                        {buildRecipePreview()}
                    </div>
                )}
            </div>
            {/* Position fixed is a mistake. */}
            <Footer />
        </>
    )
}

export default UnloggedUsers
