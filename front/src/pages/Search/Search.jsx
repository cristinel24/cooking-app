import './index.css'

import { Dropdown, Filters } from '../../components'
import { FormCheckboxList } from '../../components/Form'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'

const sortOptions = [
    { name: 'cele mai bune recenzii', sort: 'ratingAvg', order: 'desc' },
    { name: 'titlu crescător', sort: 'title', order: 'asc' },
    { name: 'titlu descrescător', sort: 'title', order: 'desc' },
    { name: 'cele mai recente', sort: '_id', order: 'desc' },
    { name: 'cele mai vechi', sort: '_id', order: 'asc' },
    { name: 'vizualizări', sort: 'viewCount', order: 'desc' },
]

export default function Search() {
    const { pathname } = useLocation()
    const navigate = useNavigate()
    // const { query, sort, order, filters } = useSearch()

    const [searchTypes, setSearchTypes] = useState([
        { label: 'Utilizatori', id: 'users', checked: pathname.includes("users") },
        { label: 'Rețete', id: 'recipes', checked: pathname.includes("recipes") },
    ])
    const [sortOption, setSortOption] = useState(sortOptions[0])

    const [results, setResults] = useState({ total: 1, data: [] })

    const onChoice = (choice) => {
        setResults({ total: 1, data: [] })
        navigate(`/search/${choice.id}`)
    }

    return (
        <div className="search-page">
            <div className="search-page-options">
                <div className="search-page-section">
                    <h3>Ce vrei să cauți?</h3>
                    <FormCheckboxList
                        options={searchTypes}
                        setOptions={setSearchTypes}
                        onChoice={onChoice}
                    />
                </div>
                <div className="search-page-section">
                    <h3>Sortează după</h3>
                    <Dropdown options={sortOptions} option={sortOption} setOption={setSortOption} />
                </div>
                {pathname.includes("recipes") && <Filters />}
            </div>
            <Outlet context={[results, setResults]} />
        </div>
    )
}
