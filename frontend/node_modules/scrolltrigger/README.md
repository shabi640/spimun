# Scrolltrigger

Fire callbacks as you scroll (or a low-level version of [Waypoints](https://github.com/imakewebthings/waypoints)).

## Install

With [npm](http://npmjs.org) do:

```bash
npm install scrolltrigger
```
## Usage

```js
var Scrolltrigger = require('scrolltrigger')

var triggers = new Scrolltrigger(window, 'y')

// `callback` will fire when the `window` scroll position reaches 1000 pixels
triggers.add({
  threshold: function () {
    return 1000
  },
  callback: function (direction, trigger) {
    console.log(direction) // 1 is forward, -1 is backwards
    // => 1
  }
})
```

## License

MIT
