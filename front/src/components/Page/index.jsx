import { Outlet } from 'react-router-dom'
import Footer from '../Footer'
import Navbar from '../Navbar'

import './index.css'

const Page = () => {
    return (
        <>
            <Navbar />
            <div className="page-container">
                <Outlet />
            </div>
            <Footer />
        </>
    )
}

export default Page
