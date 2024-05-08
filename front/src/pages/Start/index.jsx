import { useState, useEffect } from 'react'
import './index.css'
import { Page } from '../../components'
import { Feed, Dropdown, PopUpChat } from '../../components'

const Start = () => {
    const isLogged = true
    const loggedUserRoutes = ['route1', 'route2', 'route3']
    const dropdownCategories = [
        'Cele mai vizualizate',
        'Cel mai mare rating',
        'Cele mai noi',
        'Favorite',
        'Retele prietenilor',
        'Recomandari',
    ]

    let feedIds = []
    dropdownCategories.map(
        (category, index) => (feedIds[category] = 'feed' + index)
    )

    const [selectedCategoryId, setSelectedCategoryId] = useState(
        feedIds[dropdownCategories[0]]
    )

    const manageScrollListener = (action, handleScroll) => {
        if (action === 'add') {
            window.addEventListener('scroll', handleScroll)
        } else if (action === 'remove') {
            window.removeEventListener('scroll', handleScroll)
        }
    }

    const handleCategoryChange = (category) => {
        // if (feedIds[category] == selectedCategoryId) return

        setSelectedCategoryId(feedIds[category])

        let feeds = Array.from(document.getElementsByClassName('feed'))
        // console.log(category)

        for (let i = 0; i < feeds.length; i++)
            if (feeds[i].id == selectedCategoryId) {
                feeds[i].style.display = 'flex'
            } else {
                feeds[i].style.display = 'none'
            }
    }

    // const feedData = [
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

    // let feed = []
    // for (let i = 0; i < feedData.length; i++) {
    //     feed.push(
    //         <Categories
    //             key={i}
    //             name={feedData[i].name}
    //             id={feedData[i].id}
    //             recipes={feedData[i].recipes}
    //         ></Categories>
    //     )
    // }

    const feed = (name, id, route, isSelected, index) => {
        if (loggedUserRoutes.indexOf(route) == -1 && !isLogged) return null

        return (
            <Feed
                name={name}
                id={id}
                route={route}
                isSelected={isSelected}
                key = {selectedCategoryId + ' ' + index}
            ></Feed>
        )
    }

    useEffect (() => {
        let feeds = Array.from(document.getElementsByClassName('feed'))

        for (let i = 0; i < feeds.length; i++)
            if (feeds[i].id == selectedCategoryId) {
                feeds[i].style.display = 'flex'
            } else {
                feeds[i].style.display = 'none'
            }
    }, [selectedCategoryId])

    useEffect(() => {
        handleCategoryChange(dropdownCategories[0])
    }, [])

    return (
        <Page>
            <h1 className="start-page-message start-page-container-component">
                Explorează rețetele...
            </h1>
            <Dropdown
                feed={dropdownCategories}
                selectedCategoryId={selectedCategoryId}
                onSelectCategory={handleCategoryChange}
            ></Dropdown>
            <div className="start-page-container">
                <div className="start-page-container-component">
                    {/* {feed} */}
                    {dropdownCategories.map((category, index) =>
                        feed(category, feedIds[category], 'route', feedIds[category] == selectedCategoryId, index)
                    )}
                    {/* {feed('Cele mai vizualizate', 'id1', 'route1')}
                    {feed('Cel mai mare rating', 'id2', 'route2')}
                    {feed('Cele mai noi', 'id3', 'route3')}
                    {feed('Favorite', 'id4', 'route4')}
                    {feed('Retetele prietenilor', 'id5', 'route5')}
                    {feed('Recomandari', 'id6', 'route6')} */}
                </div>
            </div>
        </Page>
    )
}

export default Start
