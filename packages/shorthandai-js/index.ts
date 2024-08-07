import fetch from 'cross-fetch';

export type ShorthandDataAccessProps = {
  token: string,
}

const __API_ROOT_URL__ = `https://apiv1.shorthand.ai/api/v1`

export type SHValueScalar = number | string | boolean | null

export type SHValueVector = SHValueScalar[]

export type SHValueMatrix = SHValueScalar[][]

export type SHValue = SHValueScalar | SHValueVector | SHValueMatrix

export type SHValueAuthor = {
  uid?: string
  name?: string
  email?: string
}


export type SHValueDoc = {
  value: SHValue,
  createdTS: number,
  updatedTS: number,
  author: SHValueAuthor,
  description: string,
}

export const ShorthandValue = ({ token }: ShorthandDataAccessProps) => {

  const getinfo = async (topicName: string, tag?: string) => {
    try {
      const res = await fetch(
        `${__API_ROOT_URL__}/get`,
        {
          body: JSON.stringify({
            topicName,
            tag,
            token,
          }),
          method: 'POST',
          redirect: 'follow',
          headers: [[ "Content-Type", "application/json" ]]
        }
      )
  
      if (res.status >= 500) {
        throw new Error(res.statusText)
      }
      if (res.status >= 400) {
        throw new Error(res.statusText)
      }
      const data = await res.json()
      const value = {
        value: data?.value,
        createdTS: data?.createdTS,
        updatedTS: data?.updatedTS,
        author: data?.author,
        description: data?.description,
      } as SHValueDoc
      return value
    } catch (e) {
      console.error(e)
      return undefined
    }
  }

  const get = async (topicName: string, tag?: string) => {
    try {
      const res = await fetch(
        `${__API_ROOT_URL__}/get`,
        {
          body: JSON.stringify({
            topicName,
            tag,
            token,
          }),
          method: 'POST',
          redirect: 'follow',
          headers: [[ "Content-Type", "application/json" ]]
        }
      )
  
      if (res.status >= 500) {
        throw new Error(res.statusText)
      }
      if (res.status >= 400) {
        throw new Error(res.statusText)
      }
      const data = await res.json()
      const value = data?.value as SHValue
      return value
    } catch (e) {
      console.error(e)
      return undefined
    }
  }

  const set = async (topicName: string, value: SHValue) => {
    try {
      const res = await fetch(
        `${__API_ROOT_URL__}/set`,
        {
          body: JSON.stringify({
            topicName,
            value,
            token,
          }),
          method: 'POST',
          redirect: 'follow',
          headers: [[ "Content-Type", "application/json" ]]
        }
      )
      if (res.status >= 500) {
        throw new Error(res.statusText)
      }
      if (res.status >= 400) {
        throw new Error(res.statusText)
      }
      const data = await res.json()
      return data
    } catch (e) {
      console.error(e)
      return undefined
    }
  }

  return ({
    getinfo,
    get,
    set,
  })
}

export default ShorthandValue