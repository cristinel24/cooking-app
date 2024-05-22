import React, { useState, useEffect } from 'react'
import { RatingValue, Tag, Button, Report } from '../../components'
import './index.css'
import { prepTimeDisplayText, ratingToNumber } from '../../utils/recipeData'
import { IoIosTime } from 'react-icons/io'
import { FaUser } from 'react-icons/fa'

export default function Recipe() {
    const placeholderRecipe = {
        updatedAt: {
            $date: '2024-05-19T14:18:39.964Z',
        },
        id: '5',
        title: 'Vegetarian lasagne',
        description:
            'Make our easy vegetable lasagne using just a few ingredients. You can use ready-made tomato sauce and white sauce, or batch cook the sauces and freeze them',
        prepTime: 95,
        steps: [
            '<img src="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"/><p>To <em>make</em> the tomato sauce, heat the olive oil in a saucepan.</p> <p> Add the onions, garlic and carrot. Cook for 5-7 mins over a medium heat until softened. Turn up the heat a little and stir in the tomato purée. Cook for 1 min, pour in the white wine, then cook for 5 mins until this has reduced by two-thirds. Pour over the chopped tomatoes and add the basil leaves. Bring to the boil then simmer for 20 mins. Leave to cool then whizz in a food processor. Will keep, cooled, in the fridge for up to three days or frozen for three months.</p>',
            'To make the white sauce, melt the butter in a saucepan, stir in the plain flour, then cook for 2 mins. Slowly whisk in the milk, then bring to the boil, stirring. Turn down the heat, then cook until the sauce starts to thicken and coats the back of a wooden spoon. Will keep, cooled, in the fridge for up to three days or frozen for three months.',
            'Heat the oven to 200C/180C fan/gas 6. Lightly oil two large baking trays and add the peppers and aubergines. Toss with the olive oil, season well, then roast for 25 mins until lightly browned.',
            'Reduce the oven to 180C/160C fan/gas 4. Lightly oil a 30 x 20cm ovenproof dish. Arrange a layer of the vegetables on the bottom, then pour over a third of the tomato sauce. Top with a layer of lasagne sheets, then drizzle over a quarter of the white sauce. Repeat until you have three layers of pasta.',
            'Spoon the remaining white sauce over the pasta, making sure the whole surface is covered, then scatter over the mozzarella and cherry tomatoes. Bake for 45 mins until bubbling and golden.',
        ],
        ingredients: [
            '3 red peppers, cut into large chunks',
            '2 aubergines, cut into ½ cm thick slices',
            '8 tbsp olive oil, plus extra for the dish',
            '300g lasagne sheets',
            '125g mozzarella',
            'handful cherry tomatoes, halved',
            '1 tbsp olive oil',
            '2 onions, finely chopped',
            '2 garlic cloves, sliced',
            '1 carrot, roughly chopped',
            '2 tbsp tomato purée',
            '200ml white wine',
            '3 x 400g cans chopped tomatoes',
            '1 bunch of basil, leaves picked',
            '85g butter',
            '85g plain flour',
            '750ml milk',
        ],
        allergens: [
            'flour',
            'milk',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
        ],
        tags: [
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
            'Vegetarian',
            'Lasagne',
        ],
        tokens: [],
        ratings: [],
        thumbnail:
            'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
        viewCount: 10,
        ratingCount: 2,
        ratingSum: 7,
        author: {
            id: '21',
            username: 'matthew49',
            displayName: 'Kimberly Shaw',
            icon: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
            roles: 0,
            ratingAvg: 1.5,
        },
    }

    const [recipeData, setRecipeData] = useState(placeholderRecipe)
    const [isReportVisible, setIsReportVisible] = useState(false)

    const toggleReport = () => {
        setIsReportVisible(!isReportVisible)
    }

    const onFavorite = () => {
        // TODO: api call

        setRecipeData((prevRecipe) => {
            return {
                ...prevRecipe,
                favorite: !prevRecipe.favorite,
            }
        })
    }

    useEffect(() => {
        setRecipeData(placeholderRecipe)
    }, [])

    return (
        <>
            {isReportVisible && (
                <Report onSend={toggleReport} onCancel={toggleReport} />
            )}
            <div className="recipe-page-container">
                <div className="recipe-page-grid-container">
                    <div className="recipe-page-data">
                        <h1>{recipeData.title}</h1>

                        <div className="recipe-page-metadata">
                            <div className="recipe-page-icon-data">
                                <IoIosTime />
                                <span>
                                    {prepTimeDisplayText(recipeData.prepTime)}
                                </span>
                            </div>
                            <div className="recipe-page-icon-data">
                                <FaUser />
                                <span>{recipeData.author.displayName}</span>
                            </div>

                            <RatingValue
                                className="recipe-page-rating-stars"
                                value={ratingToNumber(
                                    recipeData.ratingSum,
                                    recipeData.ratingCount
                                )}
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
                                    <Tag
                                        className="recipe-page-tag"
                                        key={index}
                                        text={tag}
                                    />
                                ))}
                            </div>
                        </div>

                        <div className="recipe-page-tags">
                            Alergeni:
                            <div className="recipe-page-tags-container">
                                {recipeData.allergens.map((tag, index) => (
                                    <Tag
                                        className="recipe-page-tag"
                                        key={index}
                                        text={tag}
                                    />
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="recipe-page-image-container">
                        <div className="recipe-page-image">
                            <img
                                src={recipeData.thumbnail}
                                alt="recipe image"
                            />
                        </div>
                        <Button
                            className={'recipe-page-button-favorite'}
                            text={
                                recipeData.favorite
                                    ? 'Elimină din favorite'
                                    : 'Adaugă la favorite'
                            }
                            onClick={onFavorite}
                        />
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
        </>
    )
}
