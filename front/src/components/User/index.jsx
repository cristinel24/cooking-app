import './index.css'

export default function User(props) {
    const imageStyle = {
        backgroundImage: `url(${props.image})`,
    }
    return (
        <div className="user">
            <div className="user-header">
                <div className="user-image" style={imageStyle}></div>
                <div className="user-name-and-posts">
                    <div className="user-name">{props.name}</div>
                    <div className="user-posts">
                        <a href={props.posts}>Postari</a>
                    </div>
                </div>
            </div>
            <div className="user-description">
                <p>{props.description}</p>
            </div>
        </div>
    )
}
