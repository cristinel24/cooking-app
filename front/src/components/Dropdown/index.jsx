import './index.css'
import '../index'

const Dropdown = (props) => {
  return (
    <select className="dropdown-item" value={props.selectedCategory} onChange={(event) => props.onSelectCategory(event.target.value)}>
      {props.feed.map((category, index) => (
        <option key={index} value={category} className="dropdown-option">
          {category}
        </option>
      ))}
    </select>
  )
}

export default Dropdown
