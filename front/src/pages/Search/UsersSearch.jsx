import { useEffect, useState } from 'react'

import { searchUsers } from '../../services/search'
import { getErrorMessage } from '../../utils/api'
import InfiniteScroll from 'react-infinite-scroll-component'
import { UserCard } from '../../components'
import { useOutletContext } from 'react-router-dom'
import { useSearch } from '../../hooks/useSearch'

export default function UsersSearch() {
    const [results, setResults] = useOutletContext()
    const [error, setError] = useState('')
    const { query, sort, order } = useSearch()

    useEffect(() => {
        const fetch = async () => {
            try {
                const result = await searchUsers({
                    query,
                    sort,
                    order,
                    start: results.data.length,
                    count: 10,
                })
                if (!ignore) {
                    setResults((results) => ({
                        ...result,
                        data: [...results.data, ...result.data],
                    }))
                }
            } catch (e) {
                // if fetching fails, set results.total to 0 so that InfiniteScroll thinks there
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
                query,
                sort,
                order,
                start: results.data.length,
                count: 10,
            })
            if (!ignore) {
                setResults((results) => ({
                    ...result,
                    data: [...results.data, ...result.data],
                }))
            }
        } catch (e) {
            // if fetching fails, set results.total to 0 so that InfiniteScroll thinks there
            // are no more results
            setError(getErrorMessage(e))
        }
    }

    return (
        <div className="search-page-results">
            <InfiniteScroll
                className="search-page-results-container"
                dataLength={results.data.length} //This is important field to render the next data
                next={fetchUsers}
                hasMore={error.length > 0 ? false : results.data.length < results.total}
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
                {results.data.map((user) => (
                    <UserCard key={user.id} user={user} />
                ))}
            </InfiniteScroll>
        </div>
    )
}
