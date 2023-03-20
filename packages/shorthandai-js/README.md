## shorthandai

This package provides a Javascript SDK for working with the ShorthandAI platform. Compatible with both node and the browser.

### Installation
```sh
$ npm install --save @shorthandai/web
```

```sh
$ yarn add @shorthandai/web
```

### Usage
```ts
const token = 'sh-CQSGBczgnM8sDGBr3Tlh'
const SH = ShorthandValue({ token })
console.log(await SH.get('CAH:MLR:2025Y'))

console.log(await SH.set('demomat', [[0,1,2], [3,4,5]]))
console.log(await SH.set('demovect', [4,5,6]))
console.log(await SH.set('demoscalar', 100))

console.log(await SH.get('demomat'))
console.log(await SH.get('demovect'))
console.log(await SH.get('demoscalar'))
```