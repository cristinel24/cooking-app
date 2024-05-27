import React, { useState } from 'react'
import './index.css'

import { ReportBug, Report } from '../index'

function Footer() {
    const [isReportBugVisible, setIsReportBugVisible] = useState()

    const onSendBug = () => {
        console.log('sent bug')
        toggleReportBugVisibility()
    }

    const toggleReportBugVisibility = () => {
        setIsReportBugVisible(!isReportBugVisible)
    }

    return (
        <>
            {isReportBugVisible && (
                <ReportBug
                    onSend={onSendBug}
                    onCancel={toggleReportBugVisibility}
                />
            )}
            <footer className="footer">
                <div className="footer-brand">
                    COOKING APP. 2024 TOATE DREPTURILE REZERVATE
                </div>
                <div className="footer-bug">
                    <button type="button" onClick={toggleReportBugVisibility}>
                        Raportează un bug
                    </button>
                </div>
            </footer>
        </>
    )
}
export default Footer
