(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.Scrolltrigger = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
(function (global){
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


}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"defined":2,"xtend/mutable":3}],2:[function(require,module,exports){
module.exports = function () {
    for (var i = 0; i < arguments.length; i++) {
        if (arguments[i] !== undefined) return arguments[i];
    }
};

},{}],3:[function(require,module,exports){
module.exports = extend

var hasOwnProperty = Object.prototype.hasOwnProperty;

function extend(target) {
    for (var i = 1; i < arguments.length; i++) {
        var source = arguments[i]

        for (var key in source) {
            if (hasOwnProperty.call(source, key)) {
                target[key] = source[key]
            }
        }
    }

    return target
}

},{}]},{},[1])(1)
});