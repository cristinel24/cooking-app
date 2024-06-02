export default function ErrorMessage({ children }) {
    return (
        <div className="profile-error">
            <img src="/cooking-app-robot-sad.svg" />
            {children}
        </div>
    )
}
