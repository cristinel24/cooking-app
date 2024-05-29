import './index.css'

import { Button, PageButton } from '../../components'

function Admin({
    userName,
    userNumber,
    content,
    date,
    view,
    pathPage,
    handleClick,
}) {
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
                        <PageButton path={pathPage}>
                            <span>{view}</span>{' '}
                            <img src="./view.png" alt="View ph" />
                        </PageButton>
                    </div>
                    <div className="customButtons">
                        <div>
                            <Button
                                onClick={handleClick}
                                text={
                                    <>
                                        <span>Citit</span>{' '}
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
