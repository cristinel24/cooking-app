import { useContext } from 'react'
import { Outlet } from 'react-router-dom'

import './index.css'

import { Footer, PopUpChat, Navbar } from '../../components'
import { UserContext } from '../../context'

const Page = () => {
    const { loggedIn } = useContext(UserContext)

    return (
        <>
            <Navbar />
            <div className="page-container">
                <Outlet />
                {loggedIn && <PopUpChat />}
            </div>
            <Footer />
        </>
    )
}

export default Page
