import fetch from 'cross-fetch';

export type ShorthandDataAccessProps = {
  token: string,
}

const __API_ROOT_URL__ = `https://apiv1.shorthand.ai/api/v1`

export type SHValueScalar = number | string | boolean | null

export type SHValueVector = SHValueScalar[]

export type SHValueMatrix = SHValueScalar[][]

export type SHValue = SHValueScalar | SHValueVector | SHValueMatrix

export const ShorthandValue = ({ token }: ShorthandDataAccessProps) => {

  const get = async (topicName: string, tag?: string) => {
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
    try {
      const data = await res.json()
      const value = data?.value as SHValue
      return value
    } catch (e) {
      console.error(e)
      return undefined
    }
  }

  const set = async (topicName: string, value: SHValue) => {
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
    try {
      const data = await res.json()
      return data
    } catch (e) {
      console.error(e)
      return undefined
    }
  }

  return ({
    get,
    set,
  })
}

export default ShorthandValue

const main = async () => {
  const token = 'sh-CQSGBczgnM8sDGBr3Tlh'
  const SH = ShorthandValue({ token })
  console.log(await SH.get('CAH:MLR:2025Y'))

  console.log(await SH.set('demomat', [[0,1,2], [3,4,5]]))
  console.log(await SH.set('demovect', [4,5,6]))
  console.log(await SH.set('demoscalar', 100))

  console.log(await SH.get('demomat'))
  console.log(await SH.get('demovect'))
  console.log(await SH.get('demoscalar'))
}

main()