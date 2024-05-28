import { Outlet } from 'react-router-dom'
import PopUpChat from '../PopUpChat'
import Footer from '../Footer'
import Navbar from '../Navbar'

import './index.css'

const Page = () => {
    return (
        <>
            <Navbar />
            <div className="page-container">
                <Outlet />
                <PopUpChat />
            </div>
            <Footer />
        </>
    )
}

export default Page
