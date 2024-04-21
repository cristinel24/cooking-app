import React from "react";
import "./index.css";

const PreviewRecipe = ({ title, tags, allergens, description }) => {
  return (
    <div className="preview-recipe-container">
      <div className="recipe-details-container">
        <h1 className="recipe-title">{title}</h1>
        <div className="recipe-tags">
          <div className="tags-title">Tag-uri:</div>
          {tags.map((tag, index) => (
            <div key={index} className="tag">
              {tag}
            </div>
          ))}
        </div>
        <div className="recipe-allergens">
          <div className="allergens-title">Alergeni:</div>
          {allergens.map((allergen, index) => (
            <div key={index} className="allergen">
              {allergen}
            </div>
          ))}
        </div>
        <div className="recipe-description">
          <div className="description-title">Descriere:</div>
          <div className="description-text">{description}</div>
        </div>
      </div>
    </div>
  );
};

export default PreviewRecipe;
