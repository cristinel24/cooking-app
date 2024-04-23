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
                    <img src="./!.png" alt="Admin Sign" />
                    <h3>{userName}</h3>
                </div>
                <div className="admin-header-right">
                    <p>{userNumber}</p>
                </div>
            </div>
            <div className="admin-content">
                <p>{content}</p>
            </div>
            <div className="admin-footer">
                <div className="admin-footer-left">
                    <p>{date}</p>
                </div>
                <div className="admin-footer-right">
                    <div className="customButtons">
                        <PageButton
                            children={
                                <>
                                    <span>{view}</span>{' '}
                                    <img src="./view.png" alt="View ph" />
                                </>
                            }
                            path={pathPage}
                        />
                    </div>
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
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Admin
