import { useState, useEffect } from 'react'
import './index.css'
import '../index'
import { PageButton, Recipe, ActionButton } from '../index'

const Feed = (props) => {
    const [recipeList, setRecipeList] = useState([])
    const [isScrollable, setIsScrollable] = useState(false)

    const getRecipes = (nr, offset, route) => {
        //recipeData will be replaced with an async call to backend
        const recipeData = [
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
            {
                title: 'Title1',
                author: 'Author1',
                image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
                description:
                    'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
                tags: ['mancare', 'mancare', 'mancare'],
                allergens: ['oua', 'oua', 'oua'],
            },
        ]
        return recipeData.slice(offset, offset + nr)
    }

    const handleScroll = () => {
        const { scrollTop, clientHeight, scrollHeight } =
            document.documentElement
        if (scrollTop + clientHeight >= scrollHeight - 0) {
            let newRecipes = getRecipes(10, recipeList.length, props.route)
            setRecipeList((recipeList) => [...recipeList, ...newRecipes])
        }
    }

    const toogleRecipe = () => {
        //get current feed element
        const recipes = Array.from(
            document.getElementsByClassName('recipe')
        ).filter((recipe) => {
            return recipe.parentElement.id == props.id
        })

        //show/hide feed recipes
        const displays = ['flex', 'none']
        let isDisplayed = 0
        if (recipes[recipes.length - 1].style.display != 'none') {
            isDisplayed = 1
        }
        for (let i = 2; i < recipes.length; i++) {
            recipes[i].style.display = displays[isDisplayed]
        }

        //set display: none for the other feeds
        const otherCategories = Array.from(
            document.getElementsByClassName('categories')
        ).filter((category) => {
            return category.id != props.id
        })

        for (let i = 0; i < otherCategories.length; i++)
            otherCategories[i].style.display = displays[1 - isDisplayed]

        //set isScrollable for feed
        if (isDisplayed) {
            setIsScrollable(false)
            window.removeEventListener('scroll', handleScroll)
        } else {
            setIsScrollable(true)
            window.addEventListener('scroll', handleScroll)
        }
    }

    let recipes = []
    for (let i = 0; i < recipeList.length; i++) {
        recipes.push(
            <Recipe
                key={i}
                title={recipeList[i].title}
                author={recipeList[i].author}
                image={recipeList[i].image}
                description={recipeList[i].description}
            ></Recipe>
        )
    }

    useEffect(() => {
        let newRecipes = getRecipes(10, 0, props.route)
        setRecipeList((recipeList) => [...recipeList, ...newRecipes])
    }, [])

    useEffect(() => {
        if (isScrollable) 
            return

        const recipes = Array.from(
            document.getElementsByClassName('recipe')
        ).filter((recipe) => {
            return recipe.parentElement.id == props.id
        })

        for (let i = 2; i < recipes.length; i++)
            recipes[i].style.display = 'none'
        
    }, [recipeList])

    return (
        <div className="categories" id={props.id}>
            <ActionButton onClick={toogleRecipe} text={props.name} />
            {recipes}
        </div>
    )
}

export default Feed
