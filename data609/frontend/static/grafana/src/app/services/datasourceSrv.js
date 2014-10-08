define([
  'angular',
  'lodash',
  'config',
  './graphite/graphiteDatasource',
  './influxdb/influxdbDatasource',
  './opentsdb/opentsdbDatasource',
  './elasticsearch/es-datasource',
],
function (angular, _, config) {
  'use strict';

  var module = angular.module('grafana.services');

  module.service('datasourceSrv', function($q, $http, $injector, $window) {
    var datasources;
    var metricSources = [];
    var annotationSources = [];
    var grafanaDB = {};
    var remote_datasources = {};
    var inited = false;
    // var remote_datasources = {
    //   influxdb: {
    //     type: 'influxdb',
    //     url: "http://127.0.0.1:8086/db/freeloading",
    //     username: 'admin1',
    //     password: 'admin',
    //   },
    //   grafana: {
    //     type: 'influxdb',
    //     url: "http://127.0.0.1:8086/db/grafana",
    //     username: 'admin',
    //     password: 'admin',
    //     grafanaDB: true,
    //     supportMetrics: false,
    //   },
    // };
    var that = this;
    var getDatasources = function(){
      var promise = $http.get('/api/datasources/?format=json').success(function(data, status){
          console.log('success');
          if(!datasources){
            datasources = {}
          angular.extend(datasources, data);
          _.each(datasources, function(datasource, key) {
            datasource.name = key;
            if (datasource.url) { parseBasicAuth(datasource); }
            if (datasource.type === 'influxdb') { parseMultipleHosts(datasource); }
          });
          };
          if(!inited){
            that.init();
          }
        }).error(function(data, status){
          if(status==403){
            $window.location.href="/accounts/login/?next=/static/grafana/src/index.html";
          } else{
            $window.location.href="/errors/404/"
          }
        });
      return promise
    };
    var parseBasicAuth = function(datasource) {
      var passwordEnd = datasource.url.indexOf('@');
      if (passwordEnd > 0) {
        var userStart = datasource.url.indexOf('//') + 2;
        var userAndPassword = datasource.url.substring(userStart, passwordEnd);
        var bytes = crypto.charenc.Binary.stringToBytes(userAndPassword);
        datasource.basicAuth = crypto.util.bytesToBase64(bytes);

        var urlHead = datasource.url.substring(0, userStart);
        datasource.url = urlHead + datasource.url.substring(passwordEnd + 1);
      }

      return datasource;
    };

    var parseMultipleHosts = function(datasource) {
      datasource.urls = _.map(datasource.url.split(","), function (url) { return url.trim(); });
      return datasource;
    };

    this.init = function() {
      _.each(datasources, function(value, key) {
        var ds = this.datasourceFactory(value);
        if (value.default) {
          this.default = ds;
          ds.default = true;
        }
        datasources[key] = ds;
      }, this);

      if (!this.default) {
        this.default = datasources[_.keys(datasources)[0]];
        this.default.default = true;
      }
      // create list of different source types
      _.each(datasources, function(value, key) {
        if (value.supportMetrics) {
          metricSources.push({
            name: value.name,
            value: value.default ? null : key,
            default: value.default,
          });
        }
        if (value.supportAnnotations) {
          annotationSources.push({
            name: key,
            editorSrc: value.annotationEditorSrc,
          });
        }
        if (value.grafanaDB) {
          grafanaDB = value;
        }
      });
      inited = true;
    };

    this.datasourceFactory = function(ds) {
      var Datasource = null;
      switch(ds.type) {
      case 'graphite':
        Datasource = $injector.get('GraphiteDatasource');
        break;
      case 'influxdb':
        Datasource = $injector.get('InfluxDatasource');
        break;
      case 'opentsdb':
        Datasource = $injector.get('OpenTSDBDatasource');
        break;
      case 'elasticsearch':
        Datasource = $injector.get('ElasticDatasource');
        break;
      default:
        Datasource = $injector.get(ds.type);
      }
      return new Datasource(ds);
    };

    this.get = function(name) {
      if (!name) { return this.default; }
      if (datasources[name]) { return datasources[name]; }

      return this.default;
    };

    this.getAnnotationSources = function() {
      return annotationSources;
    };

    this.getMetricSources = function() {
      return metricSources;
    };

    this.getGrafanaDB = function(){
      var deferredGrafanaDB = $q.defer();
      getDatasources().then(function(data){
        deferredGrafanaDB.resolve(grafanaDB);
      });
      return deferredGrafanaDB.promise;
    };

  });
});
