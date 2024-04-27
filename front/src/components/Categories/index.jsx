import './index.css'
import '../index'
import { PageButton, Recipe, ActionButton } from '../index'

const ViewRecipe = (props) => {
    const toogleRecipe = () => {
        const recipes = Array.from(
            document.getElementsByClassName('recipe')
        ).filter((recipe) => {
            return recipe.parentElement.id == props.id
        })

        const displays = ['flex', 'none']
        let isDisplayed = 0
        if (recipes[recipes.length - 1].style.display != 'none') {
            isDisplayed = 1
        }
        for (let i = 2; i < recipes.length; i++) {
            recipes[i].style.display = displays[isDisplayed]
        }
    }
    let recipes = []
    for (let i = 0; i < props.recipes.length; i++) {
        recipes.push(
            <Recipe
                key={i}
                title={props.recipes[i][0]}
                author={props.recipes[i][1]}
                image={props.recipes[i][2]}
                description={props.recipes[i][3]}
            ></Recipe>
        )
    }
    return (
        <div className="categories" id={props.id}>
            <ActionButton onClick={toogleRecipe} text={props.name} />
            {recipes}
        </div>
    )
}

export default ViewRecipe
