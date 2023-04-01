## shorthandai

This package provides a Javascript SDK for working with the ShorthandAI in React.

### Installation
```sh
$ npm install --save @shorthandai/react
```

```sh
$ yarn add @shorthandai/react
```

### Usage
```tsx
import { useShorthandValue } from '@shorthandai/react'

const { value, loading, error } = useShorthandValue('demo123', {
    token: 'demo',
    lazy: false,
    pollIntervalMS: 0,
})
```