var test = require('tape')
var domify = require('domify')

var Scrolltrigger = require('../')

var _duration = 0
var body = document.body

body.style.height = '5000px'

function delay (fn) {
  setTimeout(fn, duration())
}

function duration () {
  _duration += 200
  return _duration
}

test('Basic usage', function (t) {
  t.plan(3)

  var i = 0
  var triggers = new Scrolltrigger()

  t.equal(triggers.axis, 'y', 'axis prop is there')

  var point = triggers.add({
    threshold: function () {
      return 1000
    },
    callback: function (direction, point) {
      if (direction === 1) {
        i++
      }
      if (direction === -1) {
        i++
        triggers.remove(point)
      }
    }
  })

  t.equal(triggers.points[0], point, 'point gets added')

  delay(function () {
    window.scrollTo(0, 1500)
  })
  delay(function () {
    window.scrollTo(0, 500)
  })
  delay(function () {
    window.scrollTo(0, 2000)
  })
  delay(function () {
    t.equal(i, 2, 'callbacks fire correctly')
  })
})

var el = domify(
  '<div style="height: 100px; overflow: scroll">' +
    '<div style="height: 1000px">&nbsp;</div>' +
  '</div>'
)

body.appendChild(el)

test('Container other than window', function (t) {
  t.plan(1)

  var triggers = new Scrolltrigger(el)

  triggers.add({
    threshold: function () {
      return 500
    },
    callback: function (direction) {
      t.equal(direction, 1, 'works')
    }
  })

  delay(function () {
    el.scrollTop = 750
  })
})

test('stopListening()', function (t) {
  t.plan(2)

  var triggers = new Scrolltrigger()
  var _id

  t.ok(triggers.requestId > 0, 'requestId value is set')

  delay(function () {
    _id = triggers.requestId
    triggers.stopListening()
  })
  delay(function () {
    t.equal(_id, triggers.requestId, 'works')
  })
})

