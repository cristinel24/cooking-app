import Footer from '../Footer'
import Navbar from '../Navbar'

import './index.css'

const Page = ({ children }) => {
    return (
        <>
            <Navbar />
            <div className="page-container">{children}</div>
            <Footer />
        </>
    )
}

export default Page
