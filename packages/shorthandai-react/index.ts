import ShorthandValue, { SHValue } from '@shorthandai/web';
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
  const [ value, setValue ] = useState<SHValue>()
  
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

      const val = await SH.get(topicName)
      setValue(val) 
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

  return ({
    value,
    set,
    loading, 
    error,
  })
}