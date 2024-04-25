import './index.css'

export default function Recipe(props) {
    const divRecipeImageStype = {
        backgroundImage: `url(${props.image})`,
    }
    return (
        <div className="recipe">
            <div className="recipe-header">
                <div className="recipe-image" style={divRecipeImageStype}></div>
                <div className="recipe-title-and-author">
                    <div className="recipe-title">{props.title}</div>
                    <div className="recipe-author">{props.author}</div>
                </div>
            </div>
            <div className="recipe-description">
                <p>{props.description}</p>
            </div>
        </div>
    )
}
