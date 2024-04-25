import { useState } from 'react'
import './index.css'
import Filters from '../Filters'
import ActionButton from '../ActionButton'

function ShowMenu() {
    const [menuOpen, setMenuOpen] = useState(false)

    const toggleMenu = () => {
        setMenuOpen(!menuOpen)
    }

    return (
        <div className="filters-menu-wrapper">
            <div className="filters-menu-container">
                <ActionButton text="Filtre" onClick={toggleMenu}></ActionButton>
                {menuOpen && <Filters />}
            </div>
        </div>
    )
}
export default ShowMenu
