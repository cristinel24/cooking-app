import { useState } from 'react'
import './index.css'
import { RatingValue } from '..'

import { IoIosArrowDown, IoIosArrowUp } from 'react-icons/io'

const RatingCard = ({ ratingData }) => {
    ratingData = {
        rating: 2,
        parentId: 21,
        author: {
            icon: 'https://www.eatright.org/-/media/images/eatright-landing-pages/foodgroupslp_804x482.jpg?as=0&w=967&rev=d0d1ce321d944bbe82024fff81c938e7&hash=E6474C8EFC5BE5F0DA9C32D4A797D10D',
        },
        description:
            'Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune Georgiana a underscore fr spune ',
    }
    /**
    parentId, parentType, author: UserCardData, updatedAt,
    rating, description */

    const [showAllText, setShowAllText] = useState(false)

    const shortRatingLength = 300

    return (
        <div className="rating-card">
            <div className="rating-card-image">
                <img src={ratingData.author.icon} />
            </div>
            <div className="rating-card-content">
                <div className="rating-card-data">
                    {ratingData.rating > 0 && (
                        <div className="rating-card-rating">
                            <RatingValue value={ratingData.rating} showValue={false} />
                        </div>
                    )}
                    <div className="rating-card-user">
                        <span className="rating-card-display-name">Sabina Prodan</span>
                        <span className="rating-card-username">@câtrtoj</span>
                    </div>
                    <div className="rating-card-date">ora 123:3534 data 2335:#$ :#$@:#</div>
                </div>
                <div className="rating-card-description">
                    <p>
                        {showAllText || ratingData.description.length <= shortRatingLength
                            ? ratingData.description
                            : ratingData.description.slice(0, shortRatingLength) + '...'}
                    </p>
                </div>
                <div className="rating-card-buttons">
                    {ratingData.description.length > shortRatingLength && (
                        <button
                            type="button"
                            className="rating-card-transparent-button"
                            onClick={() => {
                                setShowAllText(!showAllText)
                            }}
                        >
                            {showAllText ? (
                                <>
                                    Arată mai puțin <IoIosArrowUp />
                                </>
                            ) : (
                                <>
                                    Arată mai mult <IoIosArrowDown />
                                </>
                            )}
                        </button>
                    )}
                    <button type="button" className="rating-card-transparent-button">
                        Mda
                    </button>
                    <button type="button" className="rating-card-transparent-button">
                        Corect
                    </button>
                </div>
            </div>
        </div>
    )
}

export default RatingCard
