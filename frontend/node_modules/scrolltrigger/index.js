var defined = require('defined')
var extend = require('xtend/mutable')
var raf = global.requestAnimationFrame
var cancelRaf = global.cancelAnimationFrame

var FORWARD = 1
var BACKWARD = -1

var propNames = {
  y: ['scrollY', 'pageYOffset', 'scrollTop'],
  x: ['scrollX', 'pageXOffset', 'scrollLeft']
}

module.exports = Scrolltrigger

function Scrolltrigger (container, axis) {
  var self = this
  self.container = container || window
  self.axis = axis || 'y'
  self.points = []
  self.immediatePreviousScroll = 0

  self.listen()
}

Scrolltrigger.loop = function loop (inst) {
  var con = inst.container
  var props = propNames[inst.axis]

  inst.requestId = raf(_loop)

  function _loop () {
    var scroll = defined(con[props[0]], con[props[1]], con[props[2]])

    if (typeof scroll === 'undefined') {
      throw new Error('Couldn’t get scroll position from container element')
    }

    if (inst.immediatePreviousScroll !== scroll) {
      inst.points.forEach(function (point) {
        point.update(scroll)
      })
    }

    inst.immediatePreviousScroll = scroll
    inst.requestId = raf(_loop)
  }
}

Scrolltrigger.FORWARD = FORWARD
Scrolltrigger.BACKWARD = BACKWARD

Scrolltrigger.prototype.add = function (options) {
  var self = this
  var point = new Point(options, self.immediatePreviousScroll)
  self.points.push(point)

  return point
}

Scrolltrigger.prototype.remove = function (point) {
  var self = this
  var index = self.points.indexOf(point)
  self.points.splice(index, 1)
}

Scrolltrigger.prototype.refresh = function () {
  this.points.forEach(function (point) {
    point.refresh()
  })
}

Scrolltrigger.prototype.listen = function () {
  var self = this
  Scrolltrigger.loop(self)
  if (isWindow()) {
    self.resizeHandler = debounce(self.refresh.bind(self), 150)
    window.addEventListener('resize', self.resizeHandler)
  }
}

Scrolltrigger.prototype.stopListening = function () {
  var self = this
  cancelRaf(self.requestId)
  if (isWindow()) {
    window.removeEventListener('resize', self.resizeHandler)
  }
}

function Point (options, scroll) {
  var self = this
  self.previousScroll = scroll
  self.threshold = options.threshold
  self.callback = options.callback
  extend(self, options)

  self.refresh()
}

Point.prototype.update = function (scroll) {
  var self = this
  var previous = self.previousScroll
  var current = scroll
  var threshold = self.__threshold
  var direction = current > previous ? FORWARD : BACKWARD

  // https://github.com/imakewebthings/waypoints/blob/master/src/context.js#L118
  var wasBeforeThreshold = previous < threshold
  var isAfterThreshold = current >= threshold
  var crossedForward = wasBeforeThreshold && isAfterThreshold
  var crossedBackward = !wasBeforeThreshold && !isAfterThreshold
  if (crossedForward || crossedBackward) {
    self.callback(direction, self)
  }

  self.previousScroll = scroll
}

Point.prototype.refresh = function () {
  var self = this
  self.__threshold = self.threshold()
}

function isWindow () {
  return typeof window !== 'undefined' && ('addEventListener' in window)
}

// thank you Remy Sharp
// https://remysharp.com/2010/07/21/throttling-function-calls

function debounce (fn, delay) {
  var timer = null

  return function () {
    var context = this
    var args = arguments
    clearTimeout(timer)
    timer = setTimeout(function () {
      fn.apply(context, args)
    }, delay)
  }
}

