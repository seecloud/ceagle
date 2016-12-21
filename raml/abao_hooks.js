var hooks = require('hooks'),
    assert = require('chai').assert;

var params = {version: 'v1', region: 'north-2.piedpiper.net', period: 'day'};
var paramsBadVersion = {version: 'VI', region: 'north-2.piedpiper.net', period: 'day'};
var paramsBadRegion = {version: 'v1', region: 'strange-region', period: 'day'};
var paramsBadPeriod = {version: 'v1', region: 'north-2.piedpiper.net', period: 'otherday'};

hooks.before('GET /api/{version}/regions -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/regions/detailed -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/{period} -> 404', function (test, done) {
  test.request.params = paramsBadPeriod;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/health/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/health/{period} -> 404', function (test, done) {
  test.request.params = paramsBadPeriod;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/availability/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/availability/{period} -> 404', function (test, done) {
  test.request.params = paramsBadPeriod;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/performance/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/status/performance/{period} -> 404', function (test, done) {
  test.request.params = paramsBadPeriod;
  done();
});

hooks.before('GET /api/{version}/region/{region}/infra -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/infra -> 404', function (test, done) {
  test.request.params = paramsBadRegion;
  done();
});

hooks.before('GET /api/{version}/security/issues/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/security/issues/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/region/{region}/security/issues/{period} -> 404', function (test, done) {
  test.request.params = paramsBadRegion;
  done();
});

hooks.before('GET /api/{version}/status/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/status/health/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/status/availability/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/status/performance/{period} -> 200', function (test, done) {
  test.request.params = params;
  done();
});
