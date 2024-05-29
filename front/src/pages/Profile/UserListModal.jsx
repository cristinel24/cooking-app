import { FaHeart } from 'react-icons/fa6'
import { PiCookingPot } from 'react-icons/pi'
import { BsTextParagraph } from 'react-icons/bs'
import React, { useState, useEffect } from 'react'

import './index.css'

import SideButton from './SideButton'
import { Button, GenericModal, UserCard } from '../../components'
import InfiniteScroll from 'react-infinite-scroll-component'
import { getErrorMessage } from '../../utils/api'

export default function UserListModal({ total, fetchData, isOpen, onClose, contentLabel }) {
    const [results, setResults] = useState({
        start: 0,
        total: total,
        data: [],
    })
    const [error, setError] = useState('')

    const fetchCount = 20

    useEffect(() => {
        let ignore = false
        const fetch = async () => {
            try {
                const result = await fetchData(results.start, fetchCount)
                if (!ignore) {
                    setResults((newResults) => ({
                        ...newResults,
                        fetchedInitial: true,
                        start: newResults.start + fetchCount,
                        data: [...newResults.data, ...result.data],
                    }))
                }
            } catch (e) {
                setResults((results) => ({ ...results, total: 0 }))
                setError(getErrorMessage(e))
            }
        }
        fetch()
        return () => {
            ignore = true
        }
    }, [])

    const fetchMoreData = async () => {
        if (!results.fetchedInitial) {
            return
        }
        try {
            const result = await fetchData(results.start, fetchCount)
            setResults((newResults) => ({
                ...newResults,
                start: results.start + fetchCount,
                data: [...newResults.data, ...result.data],
            }))
        } catch (e) {
            setResults((results) => ({ ...results, total: 0 }))
            setError(getErrorMessage(e))
        }
    }

    return (
        <GenericModal
            isOpen={isOpen}
            onRequestClose={onClose}
            contentLabel={contentLabel}
            className="profile-user-list-modal"
        >
            <InfiniteScroll
                className="profile-user-list-container"
                dataLength={results.data.length}
                next={fetchMoreData}
                hasMore={results.start < results.total}
                loader={<h4>Se încarcă...</h4>}
                height={400}
                endMessage={
                    error.length > 0 ? (
                        <p style={{ textAlign: 'center' }}>
                            <b>{error}</b>
                        </p>
                    ) : (
                        <p style={{ textAlign: 'center' }}>
                            <b>Toți utilizatorii au fost încărcați.</b>
                        </p>
                    )
                }
            >
                {results.data.map((result, index) => (
                    <UserCard user={result} />
                ))}
            </InfiniteScroll>
        </GenericModal>
    )
}
