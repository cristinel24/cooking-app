import { Filters } from '../../components'
import './index.css'

export default function Search() {
    return (
        <div className="search-page">
            <div className="search-page-filters">
                <Filters />
            </div>
            <div className="search-page-results">What the hell</div>
        </div>
    )
}
