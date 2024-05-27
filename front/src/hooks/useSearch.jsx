import { useEffect, useState } from 'react'
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom'
import { decodeBase64ToObject, encodeObjectToBase64 } from '../utils/base64'

/*
when i click search i must:
- navigate to search (if i'm not already there)
- initialize the query params
*/

export const useSearch = () => {
    const { pathname } = useLocation()
    const navigate = useNavigate()
    const [params, setParams] = useSearchParams()

    const [searchParams, setSearchParams] = useState({
        query: params.get('query') || '',
        sort: params.get('sort') || '_id',
        order: params.get('order') || 'desc',
        filters: (() => {
            try {
                return decodeBase64ToObject(params.get('filters'))
            } catch (e) {
                return {}
            }
        })(),
        // start: parseInt(params.get('start')) || 0,
        // count: parseInt(params.get('count')) || 10,
    })

    useEffect(() => {
        if (!['/search/users', '/search/recipes'].includes(pathname)) {
            return
        }

        // init params if they are missing
        setParams(
            new URLSearchParams({
                query: params.get('query') || '',
                sort: params.get('sort') || '_id',
                order: params.get('order') || 'desc',
                filters: (() => {
                    try {
                        decodeBase64ToObject(params.get('filters')) // check if it's valid
                        return params.get('filters')
                    } catch (e) {
                        return encodeObjectToBase64({})
                    }
                })(),
                // start: params.get('start') || '0',
                // count: params.get('count') || '10',
            })
        )

        // save params to state
        setSearchParams({
            query: params.get('query'),
            sort: params.get('sort'),
            order: params.get('order'),
            filters: (() => {
                try {
                    return decodeBase64ToObject(params.get('filters'))
                } catch (e) {
                    return {}
                }
            })(),
            // start: parseInt(params.get('start')),
            // count: parseInt(params.get('count')),
        })
    }, [pathname, params, setParams])

    const goToSearch = (query) => {
        setParam('query', query)
        navigate({
            pathname: '/search/users',
            search: `?${params.toString()}`,
        })
    }

    const setParam = (field, value) => {
        if (field == 'filters') {
            value = encodeObjectToBase64(value)
        }

        setParams((params) => {
            params.set(field, value)
            return params
        })
    }

    return {
        ...searchParams,
        goToSearch,
        setParam,
    }
}
