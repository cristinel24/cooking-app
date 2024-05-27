import { useEffect, useState } from 'react'

import { searchUsers } from '../../services/search'
import { getErrorMessage } from '../../utils/api'
import InfiniteScroll from 'react-infinite-scroll-component'
import { UserCard } from '../../components'
import { useOutletContext } from 'react-router-dom'

export default function UsersSearch() {
    const [results, setResults] = useOutletContext()
    const [error, setError] = useState('')

    useEffect(() => {
        const fetch = async () => {
            try {
                const result = await searchUsers({
                    query: '',
                    start: results.items.length,
                    count: 10,
                })
                if (!ignore) {
                    setResults((results) => ({
                        ...result,
                        items: [...results.items, ...result.users],
                    }))
                }
            } catch (e) {
                // if fetching fails, set results.count to 0 so that InfiniteScroll thinks there
                // are no more results
                setError(getErrorMessage(e))
            }
        }
        let ignore = false
        fetch()
        return () => {
            ignore = true
        }
    }, [])

    const fetchUsers = async (ignore = false) => {
        try {
            const result = await searchUsers({
                query: '',
                start: results.items.length,
                count: 10,
            })
            if (!ignore) {
                setResults((results) => ({
                    ...result,
                    items: [...results.items, ...result.users],
                }))
            }
        } catch (e) {
            // if fetching fails, set results.count to 0 so that InfiniteScroll thinks there
            // are no more results
            setError(getErrorMessage(e))
        }
    }

    return (
        <div className="search-page-results">
            <InfiniteScroll
                className="search-page-results-container"
                dataLength={results.items.length} //This is important field to render the next data
                next={fetchUsers}
                hasMore={error.length > 0 ? false : results.items.length < results.count}
                loader={<h4>Loading...</h4>}
                endMessage={
                    error.length > 0 ? (
                        <p style={{ textAlign: 'center' }}>
                            <b>{error}</b>
                        </p>
                    ) : (
                        <p style={{ textAlign: 'center' }}>
                            <b>No more users for you</b>
                        </p>
                    )
                }
            >
                {results.items.map((user) => (
                    <UserCard key={user.id} user={user} />
                ))}
            </InfiniteScroll>
        </div>
    )
}
