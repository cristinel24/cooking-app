import './index.css'
import '../index'

const Dropdown = (props) => {
  // const handleCategoryChange = (e) => {
  //   props.onSelectCategory(e.target.value)
  // }

  return (
    <select value={props.selectedCategory} onChange={(event) => props.onSelectCategory(event.target.value)}>
      {props.feed.map((category, index) => (
        <option key={index} value={category}>
          {category}
        </option>
      ))}
    </select>
  )
}

export default Dropdown