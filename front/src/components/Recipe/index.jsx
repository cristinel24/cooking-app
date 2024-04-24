import './index.css'

export default function Recipe(props) {
    const divRecipeImageStype = {
        backgroundImage: `url(${props.image})`,
    }
    return (
        <div className="recipe1">
            <div className="recipe-header1">
                <div
                    className="recipe-image1"
                    style={divRecipeImageStype}
                ></div>
                <div className="recipe-title-and-author1">
                    <div className="recipe-title1">{props.title}</div>
                    <div className="recipe-author1">{props.author}</div>
                </div>
            </div>
            <div className="recipe-description1">
                <p>{props.description}</p>
            </div>
        </div>
    )
}
