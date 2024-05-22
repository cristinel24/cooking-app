import { useState } from 'react'

import './index.css'

import { Button, Filters } from '../../components'

function ShowMenu() {
    const [menuOpen, setMenuOpen] = useState(false)

    const toggleMenu = () => {
        setMenuOpen(!menuOpen)
    }

    return (
        <div className="menu-wrapper">
            <div className="menu-container">
                <Button text="Filtre" onClick={toggleMenu} />
                {menuOpen && <Filters />}
            </div>
        </div>
    )
}
export default ShowMenu
