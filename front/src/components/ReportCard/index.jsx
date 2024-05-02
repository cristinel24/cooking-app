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
                        {props.title}
                    </h3>
                </div>
                <div className="report-card-header-right">
                    <p>{props.number}</p>
                </div>
            </div>
            <div className="report-card-content">
                <p className="report-card-content-description">
                    Motive:
                    <br />
                    {props.reason}
                </p>
                <p className="report-card-content-date">Data: {props.date}</p>
            </div>
            <div className="report-card-footer">
                <div className="report-card-footer-custom-buttons-view">
                    <PageButton
                        children={
                            <>
                                <span>
                                    <PiArrowSquareOutBold className="report-card-footer-custom-buttons-img" />
                                </span>
                                <span>{props.view}</span>
                            </>
                        }
                        path={props.pathPageView}
                    />
                </div>
                <div className="report-card-footer-custom-buttons-read">
                    <ActionButton
                        onClick={props.handleClickRead}
                        text={
                            <>
                                <span>{read}</span>{' '}
                            </>
                        }
                        Icon={FaCheck}
                    />
                </div>
                <div className="report-card-footer-custom-buttons-specific-action">
                    <ActionButton
                        onClick={props.handleClickSpecificAction}
                        text={
                            <>
                                <span>{props.specificAction}</span>{' '}
                            </>
                        }
                        Icon={BsExclamationCircle}
                    />
                </div>
            </div>
        </div>
    )
}

export default ReportCard
