import React from 'react'
import './index.css'
import PageButton from '../PageButton'
import ActionButton from '../ActionButton'
import { FaCheck } from 'react-icons/fa'
import { PiArrowSquareOutBold } from 'react-icons/pi'
import { BsExclamationCircle } from 'react-icons/bs'

function ReportCard(props) {
    let read = 'Citit'

    return (
        <div className="report-card-box">
            <div className="report-card-header">
                <div className="report-card-header-left">
                    <BsExclamationCircle className="report-card-header-left-img" />
                    <h3 className="report-card-header-left-title">
                        {props.userName}
                    </h3>
                </div>
                <div className="report-card-header-right">
                    <p>{props.userNumber}</p>
                </div>
            </div>
            <div className="report-card-content">
                <p className="report-card-content-description">
                    {props.content}
                </p>
            </div>
            <div className="report-card-footer">
                <div className="report-card-footer-left">
                    <p className="report-card-footer-left-description">
                        {props.date}
                    </p>
                </div>
                <div className="report-card-footer-right">
                    <div className="report-card-footer-right-custom-buttons-view">
                        <PageButton
                            children={
                                <>
                                    <span>
                                        <PiArrowSquareOutBold className="report-card-footer-right-custom-buttons-img" />
                                    </span>
                                    <span>{props.view}</span>
                                </>
                            }
                            path={props.pathPage}
                        />
                    </div>
                    <div className="report-card-footer-right-custom-buttons-read">
                        <ActionButton
                            onClick={props.handleClick}
                            text={
                                <>
                                    <span>{read}</span>{' '}
                                </>
                            }
                            Icon={FaCheck}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ReportCard
