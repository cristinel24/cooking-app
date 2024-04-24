import React from 'react'
import './index.css'
import PageButton from '../PageButton'
import ActionButton from '../ActionButton'

function Admin({
    userName,
    userNumber,
    content,
    date,
    view,
    pathPage,
    handleClick,
}) {
    let read = 'Citit'

    return (
        <div className="admin-box">
            <div className="admin-header">
                <div className="admin-header-left">
<<<<<<< HEAD
                    <BsExclamationCircle className="admin-header-left-img" />
                    <h3 className="admin-header-left-title">{userName}</h3>
=======
                    <img src="./!.png" alt="Admin Sign" />
                    <h3>{userName}</h3>
>>>>>>> parent of 5be36a3 (add icons)
                </div>
                <div className="admin-header-right">
                    <p>{userNumber}</p>
                </div>
            </div>
            <div className="admin-content">
                <p className="admin-content-description">{content}</p>
            </div>
            <div className="admin-footer">
                <div className="admin-footer-left">
                    <p className="admin-footer-left-description">{date}</p>
                </div>
                <div className="admin-footer-right">
                    <div className="admin-footer-right-customButtons-view">
                        <PageButton
                            children={
                                <>
<<<<<<< HEAD
                                    <span>
                                        <PiArrowSquareOutBold className="admin-footer-right-customButtons-img" />
                                    </span>
                                    <span>{view}</span>
=======
                                    <span>{view}</span>{' '}
                                    <img src="./view.png" alt="View ph" />
>>>>>>> parent of 5be36a3 (add icons)
                                </>
                            }
                            path={pathPage}
                        />
                    </div>
<<<<<<< HEAD
                    <div className="admin-footer-right-customButtons-read">
                        <ActionButton
                            onClick={handleClick}
                            text={
                                <>
                                    <span>{read}</span>{' '}
                                </>
                            }
                            Icon={FaCheck}
                        />
=======
                    <div className="customButtons">
                        <div>
                            <ActionButton
                                onClick={handleClick}
                                text={
                                    <>
                                        <span>{read}</span>{' '}
                                        <img src="./read.png" alt="Read ph" />
                                    </>
                                }
                            />
                        </div>
>>>>>>> parent of 5be36a3 (add icons)
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Admin
