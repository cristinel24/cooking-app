import './index.css'
import { Page } from '../../components'
import { Feed, Filters, PopUpChat, PreviewRecipe } from '../../components'
import ReactPaginate from 'react-paginate'

const StartPage = () => {
    const isLogged = true
    const loggedUserRoutes = ['route1', 'route2', 'route3']

    // const categoriesData = [
    //     {
    //         name: 'cele mai vizualizate',
    //         id: 'id1',
    //         recipes: [
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //         ],
    //     },
    //     {
    //         name: 'cele mai nou adaugate',
    //         id: 'id2',
    //         recipes: [
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //             {
    //                 title: 'Title1',
    //                 author: 'Author1',
    //                 image: 'https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png',
    //                 description:
    //                     'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Minima ea id aliquam quisquam dolore recusandae fugit placeat perspiciatis est similique doloribus iure quas, dolores non inventore provident dolorem unde fuga necessitatibus earum quam quia! Rerum ad, velit aliquid eveniet error, natus saepe unde id ratione quaerat numquam repellendus nobis maxime perferendis suscipit sit ipsa ab alias quasi sequi totam libero accusamus reiciendis! Aperiam veniam molestias sint ex provident libero inventore nesciunt voluptatum dolorem deserunt labore odio qui vel eos, beatae numquam saepe excepturi id tempora! Nesciunt velit molestias deleniti! Vitae ut eum nam, aspernatur facere provident ullam voluptate porro debitis.',
    //                 tags: ['mancare', 'mancare', 'mancare'],
    //                 allergens: ['oua', 'oua', 'oua'],
    //             },
    //         ],
    //     },
    // ]

    // let categories = []
    // for (let i = 0; i < categoriesData.length; i++) {
    //     categories.push(
    //         <Categories
    //             key={i}
    //             name={categoriesData[i].name}
    //             id={categoriesData[i].id}
    //             recipes={categoriesData[i].recipes}
    //         ></Categories>
    //     )
    // }

    const categories = (name, id, route) => {
        if (loggedUserRoutes.indexOf(route) == -1 && !isLogged) return null

        return <Feed name={name} id={id} route={route}></Feed>
    }

    // useEffect(() => {
    //     //for each set() there should be an async call to obtain data from backend
    //     let newRecipes = getRecipes(2, 0, 'most viewed')
    //     setMostViewed((mostViewed) => [...mostViewed, ...newRecipes])
    //     newRecipes = getRecipes(2, 0, 'highest rating')
    //     setHighestRating((highestRating) => [...highestRating, ...newRecipes])
    //     newRecipes = getRecipes(2, 0, 'newest')
    //     setNewest((newest) => [...newest, ...newRecipes])
    //     if (isLogged) {
    //         newRecipes = getRecipes(2, 0, 'favourites')
    //         setFavourites((favourites) => [...favourites, ...newRecipes])
    //         newRecipes = getRecipes(2, 0, 'friends recipes')
    //         setFriendsRecipes((friendsRecipes) => [
    //             ...friendsRecipes,
    //             ...newRecipes,
    //         ])
    //         newRecipes = getRecipes(2, 0, 'recommended')
    //         setRecommended((recommended) => [...recommended, ...newRecipes])
    //     }
    // }, [])

    return (
        <Page>
            <div className="start-page-container">
                <div className="start-page-container-component">
                    <Filters className="start-page-container-component"></Filters>
                </div>
                <div className="start-page-container-component">
                    {/* {categories} */}
                    {categories('Cele mai vizualizate', 'id1', 'route1')}
                    {categories('Cel mai mare rating', 'id2', 'route2')}
                    {categories('Cele mai noi', 'id3', 'route3')}
                    {categories('Favorite', 'id4', 'route4')}
                    {categories('Retetele prietenilor', 'id5', 'route5')}
                    {categories('Recomandari', 'id6', 'route6')}
                </div>
            </div>
        </Page>
    )
}

export default StartPage
