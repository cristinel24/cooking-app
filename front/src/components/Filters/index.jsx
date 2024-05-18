/* daca vrei sa folosesti filtre, componenta pe care o vei folosi este ShowMenu*/
/*componenta asta le tine mereu afisate*/

import { useState } from 'react'

import './index.css'

import { Button } from '../../components'

function Filters() {
    const [filterSearchTerm, setFilterSearchTerm] = useState('')
    const [alergenSearchTerm, setAlergenSearchTerm] = useState('')

    const handleFilterSearchChange = (event) => {
        setFilterSearchTerm(event.target.value)
    }

    const handleAlergenSearchChange = (event) => {
        setAlergenSearchTerm(event.target.value)
    }

    const filters = [
        'Vegetarian',
        'Vegan',
        'Carnivor',
        'Fara zahar',
        'High-protein',
        'Post',
    ]

    const alergens = ['Lapte', 'Oua', 'Gluten', 'Crustacee', 'Nuci', 'Soia']

    const handleFilterClick = (filterName) => {
        console.log(`Filter "${filterName}" clicked`)
    }

    const handleAlergenClick = (alergenName) => {
        console.log(`Alergen "${alergenName}" clicked`)
    }

    return (
        <div className="container1">
            <div className="filters">
                <div className="nameAndSearch1">
                    <div className="TitluTip">Filtre</div>
                    <div className="search-bar1">
                        <input
                            type="text"
                            value={filterSearchTerm}
                            onChange={handleFilterSearchChange}
                            placeholder="Caută..."
                        />
                    </div>
                </div>
                <div className="filter-buttons">
                    {filters
                        .filter((filter) =>
                            filter
                                .toLowerCase()
                                .includes(filterSearchTerm.toLowerCase())
                        )
                        .map((filter) => (
                            <Button
                                key={filter}
                                onClick={() => handleFilterClick(filter)}
                                text={filter}
                            />
                        ))}
                </div>
                <div className="alergens">
                    <div className="nameAndSearch2">
                        <div className="TitluTip">Alergeni</div>
                        <div className="search-bar2">
                            <input
                                type="text"
                                value={alergenSearchTerm}
                                onChange={handleAlergenSearchChange}
                                placeholder="Caută..."
                            />
                        </div>
                    </div>
                    <div className="alergen-buttons">
                        {alergens
                            .filter((alergen) =>
                                alergen
                                    .toLowerCase()
                                    .includes(alergenSearchTerm.toLowerCase())
                            )
                            .map((alergen, index) => (
                                <Button
                                    key={index}
                                    onClick={() => handleAlergenClick(alergen)}
                                    text={alergen}
                                />
                            ))}
                    </div>
                </div>
            </div>
        </div>
    )
}
export default Filters
