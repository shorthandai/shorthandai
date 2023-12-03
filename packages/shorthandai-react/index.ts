import ShorthandValue, { SHValue, SHValueDoc } from '@shorthandai/web';
import React, { useState, useEffect, useCallback } from 'react';

type UseShorthandValueOptions = {
  pollIntervalMS?: number,
  token: string,
  lazy?: boolean
}

const DefaultUseShorthandValueOptions: UseShorthandValueOptions = {
  token: 'demo',
  lazy: false,
}

export function useShorthandValue(topicName: string, options=DefaultUseShorthandValueOptions) {
  const [ loading, setLoading ] = useState(false)
  const [ error, setError ] = useState<string>()
  const [ valueDoc, setValueDoc ] = useState<SHValueDoc>()
  
  const set = async (value: SHValue) => {
    const SH = ShorthandValue({
      token: options?.token,
    })
    const res = await SH.set(topicName, value)
    return res
  }

  const getData = useCallback(async () => {
    setLoading(true)
    setError(undefined)
    try {
      const SH = ShorthandValue({
        token: options?.token,
      })

      const doc = await SH.getinfo(topicName)
      setValueDoc(doc) 
    } catch(e) {
      setError(JSON.stringify(e))
    } finally {
      setLoading(false)
    }

  }, [ topicName ])

  useEffect(() => {
    if (!options?.lazy) {
      getData()
    }
  }, [ getData ])

  useEffect(() => {
    if (options?.pollIntervalMS) {
      const intvl = setInterval(getData, options?.pollIntervalMS)
      return () => clearInterval(intvl)
    }
  }, [ getData, options?.pollIntervalMS ])

  const value = valueDoc?.value

  const author = valueDoc?.author
  const description = valueDoc?.description
  const updatedTS = valueDoc?.updatedTS
  const createdTS = valueDoc?.createdTS

  return ({
    topicName,
    options,
    value,
    author,
    description,
    updatedTS,
    createdTS,
    set,
    loading, 
    error,
  })
}