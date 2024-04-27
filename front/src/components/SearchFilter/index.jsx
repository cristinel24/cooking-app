import React from 'react'
import { useState } from 'react'
import { IoIosArrowDown, IoIosArrowUp } from 'react-icons/io'
import { CiStar } from 'react-icons/ci'
import { FaStar } from 'react-icons/fa6'
import './index.css'

const SearchFilter = (
    onIngredientsFilter,
    onTagsFilter,
    onAllergensFilter,
    onAuthorsFilter
) => {
    const [filters, setFilters] = useState({
        ingredients: '',
        tags: '',
        allergens: '',
        authors: '',
    })

    const [prepTime, setPrepTime] = useState(0)
    const [starSelected, setStarSelected] = useState(0)

    const handleInput = (field) => (event) => {
        const { value } = event.target

        setFilters({
            ...filters,
            [field]: value,
        })

        switch (field) {
            case 'ingredients':
                onIngredientsFilter(value)
                break
            case 'tags':
                onTagsFilter(value)
                break
            case 'allergens':
                onAllergensFilter(value)
                break
            case 'authors':
                onAuthorsFilter(value)
                break
            default:
                break
        }
    }

    const incrementPrepTime = () => {
        setPrepTime((prevPrepTime) => prevPrepTime + 5)
    }

    const decrementPrepTime = () => {
        if (prepTime > 0) {
            setPrepTime((prevPrepTime) => prevPrepTime - 5)
        }
    }

    const handleStarClick = (starNumber) => {
        setStarSelected((prevStarSelected) => {
            if (prevStarSelected === starNumber) {
                return (starNumber = 0)
            } else {
                return starNumber
            }
        })
    }
    return (
        <div className="search-page-filter-lbox">
            <div className="search-page-filter-box-input">
                <label htmlFor="search-page-filter-box-ingredients-name">
                    Ingrediente:
                </label>
                <input
                    type="text"
                    className="form-control"
                    id="search-page-filter-box-ingredients-name"
                    value={filters.name}
                    onChange={handleInput(
                        'search-page-filter-box-ingredients-name'
                    )}
                />
            </div>
            <div className="search-page-filter-box-input">
                <label htmlFor="search-page-filter-box-tags">Taguri:</label>
                <input
                    type="text"
                    className="form-control"
                    id="search-page-filter-box-ingredients-tags"
                    value={filters.name}
                    onChange={handleInput(
                        'search-page-filter-box-ingredients-tags'
                    )}
                />
            </div>
            <div className="search-page-filter-box-input">
                <label htmlFor="search-page-filter-box-ingredients-allergens">
                    Alergeni:
                </label>
                <input
                    type="text"
                    className="form-control"
                    id="search-page-filter-box-ingredients-allergens"
                    value={filters.name}
                    onChange={handleInput(
                        'search-page-filter-box-ingredients-allergens'
                    )}
                />
            </div>
            <div className="search-page-filter-box-input">
                <label htmlFor="search-page-filter-box-ingredients-authors">
                    Autori:
                </label>
                <input
                    type="text"
                    className="form-control"
                    id="search-page-filter-box-ingredients-authors"
                    value={filters.name}
                    onChange={handleInput(
                        'search-page-filter-box-ingredients-authors'
                    )}
                />
            </div>
            <div className="search-page-filter-box-prep-time">
                <strong>Timp de preparare:</strong>
                <div className="search-page-filter-box-prep-time-spinner">
                    <p className="search-page-filter-box-prep-time-spinner-data">
                        {prepTime} min
                    </p>
                    <div className="search-page-filter-box-prep-time-spinner-icons">
                        <IoIosArrowUp
                            onClick={() => incrementPrepTime(prepTime)}
                        />
                        <IoIosArrowDown
                            onClick={() => decrementPrepTime(prepTime)}
                        />
                    </div>
                </div>
            </div>
            <div className="search-page-filter-box-rating">
                <strong>Evaluare</strong>
                <div className="search-page-filter-box-rating-stars">
                    {[1, 2, 3, 4, 5].map((starNumber) => (
                        <span
                            key={starNumber}
                            className={
                                starNumber <= starSelected
                                    ? 'selected'
                                    : 'not-selected'
                            }
                            onClick={() => handleStarClick(starNumber)}
                        >
                            {starSelected >= starNumber ? (
                                <FaStar />
                            ) : (
                                <CiStar />
                            )}
                        </span>
                    ))}
                </div>
            </div>
            <div className="search-page-filter-box-creation-date">
                <strong>Sorteaza</strong>
                <label htmlFor="search-page-filter-box-creation-date"></label>
                <select
                    className="search-page-filter-box-creation-date-select"
                    id="date"
                    onChange={handleInput('date')}
                >
                    <option value="">Selecteaza</option>
                    <option value="today">Astazi</option>
                    <option value="one-day">Acum o zi</option>
                    <option value="one-week">Acum o saptamana</option>
                    <option value="one-month">Acum o luna</option>
                    <option value="six-months">Acum 6 luni</option>
                    <option value="one-year"> Acum un an</option>
                </select>
            </div>
            <div className="search-page-filter-box-input">
                <label htmlFor="search-page-filter-box-black-list">
                    Lista neagra:
                </label>
                <input
                    type="text"
                    className="form-control"
                    id="search-page-filter-box-black-list"
                    value={filters.name}
                    onChange={handleInput('search-page-filter-box-black-list')}
                />
            </div>
        </div>
    )
}

export default SearchFilter
