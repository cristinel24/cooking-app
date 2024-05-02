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
        <div className="admin-box">
            <div className="admin-header">
                <div className="admin-header-left">
                    <BsExclamationCircle className="admin-header-left-img" />
                    <h3 className="admin-header-left-title">
                        {props.userName}
                    </h3>
                </div>
                <div className="admin-header-right">
                    <p>{props.userNumber}</p>
                </div>
            </div>
            <div className="admin-content">
                <p className="admin-content-description">{props.content}</p>
            </div>
            <div className="admin-footer">
                <div className="admin-footer-left">
                    <p className="admin-footer-left-description">
                        {props.date}
                    </p>
                </div>
                <div className="admin-footer-right">
                    <div className="admin-footer-right-custom-buttons-view">
                        <PageButton
                            children={
                                <>
                                    <span>
                                        <PiArrowSquareOutBold className="admin-footer-right-custom-buttons-img" />
                                    </span>
                                    <span>{props.view}</span>
                                </>
                            }
                            path={props.pathPage}
                        />
                    </div>
                    <div className="admin-footer-right-custom-buttons-read">
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
