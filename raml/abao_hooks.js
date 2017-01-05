var hooks = require('hooks'),
    assert = require('chai').assert;

var params = {version: 'v1', region: 'north-2.piedpiper.net', period: 'day'};
var paramsBadVersion = {version: 'VI', region: 'north-2.piedpiper.net', period: 'day'};
var paramsBadRegion = {version: 'v1', region: 'strange-region', period: 'day'};
var paramsBadPeriod = {version: 'v1', region: 'north-2.piedpiper.net', period: 'otherday'};
var paramsRunBookRun = {version: 'v1', region: 'north-2.piedpiper.net', runbook_id: '123', run_id: '123'};

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

hooks.before('GET /api/{version}/infra -> 200', function (test, done) {
  test.request.params = params;
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

// runbooks
var correctRunbook = {description: "test", name: "test", runbook: "test", type: "test"}
var incorrectRunbook = {description: "test", name: "test"}

hooks.before('GET /api/{version}/region/{region}/runbooks -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('GET /api/{version}/runbooks -> 200', function (test, done) {
  test.request.params = params;
  done();
});

hooks.before('POST /api/{version}/region/{region}/runbooks -> 201', function (test, done) {
  test.request.params = params;
  test.request.body = correctRunbook;
  done();
});

hooks.before('POST /api/{version}/region/{region}/runbooks -> 404', function (test, done) {
  test.request.params = paramsBadRegion;
  done();
});

hooks.before('POST /api/{version}/region/{region}/runbooks -> 400', function (test, done) {
  test.request.params = params;
  test.request.body = incorrectRunbook;
  done();
});

hooks.before('GET /api/{version}/region/{region}/runbooks/{runbook_id} -> 200', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});

hooks.before('PUT /api/{version}/region/{region}/runbooks/{runbook_id} -> 200', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});

hooks.before('PUT /api/{version}/region/{region}/runbooks/{runbook_id} -> 400', function (test, done) {
  test.request.params = paramsRunBookRun;
  test.request.body = incorrectRunbook;
  done();
});

hooks.before('PUT /api/{version}/region/{region}/runbooks/{runbook_id} -> 200', function (test, done) {
  test.request.params = paramsRunBookRun;
  test.request.body = correctRunbook;
  done();
});

hooks.before('DELETE /api/{version}/region/{region}/runbooks/{runbook_id} -> 204', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});

hooks.before('POST /api/{version}/region/{region}/runbooks/{runbook_id}/run -> 202', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});

hooks.before('GET /api/{version}/runbook_runs -> 200', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});

hooks.before('GET /api/{version}/region/{region}/runbook_runs -> 200', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});

hooks.before('GET /api/{version}/region/{region}/runbook_runs/{run_id} -> 200', function (test, done) {
  test.request.params = paramsRunBookRun;
  done();
});
// end runbooks
