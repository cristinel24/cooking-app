import React from 'react'
import './index.css'
import { useState } from 'react'
import { Page } from '../../components'
import { MdFoodBank } from 'react-icons/md'
import { FaRegUser } from 'react-icons/fa'
import ActionButton from '../../components/ActionButton'
import SearchFilter from '../../components/SearchFilter'

const SearchPage = () => {
    const data = {
        users: [],
        recipes: [],
    }

    const [allData, setData] = useState(data)
    const handleClickRecipes = () => {}
    const handleClickUsers = () => {}

    const handleFilterIngredients = (ingredients) => {
        const filteredData = data.filter((item) => {
            const fullName = `${item.first_name} ${item.last_name}`
            if (fullName.toLowerCase().includes(ingredients.toLowerCase())) {
                return item
            }
        })

        setData(filteredData)
    }

    return (
        <Page>
            <div className="search-page">
                <div className="search-page-filter-box">
                    <strong>Filtre</strong>
                    <SearchFilter
                        onIngredientsFilter={handleFilterIngredients}
                        onTagsFilter={handleFilterIngredients}
                        onAllergensFilter={handleFilterIngredients}
                        onAuthorsFilter={handleFilterIngredients}
                    />
                </div>
                <div className="search-page-results">
                    <div className="search-page-result-buttons">
                        <ActionButton
                            onClick={handleClickRecipes}
                            text="Retete"
                            Icon={MdFoodBank}
                        />
                    </div>
                    <div className="search-page-result-buttons">
                        <ActionButton
                            onClick={handleClickUsers}
                            text="Utiliztori"
                            Icon={FaRegUser}
                        />
                    </div>
                </div>
            </div>
        </Page>
    )
}

export default SearchPage
