var INTEGER_REGEXP = /^\-?\d*$/;
var FLOAT_REGEXP = /^\-?\d+((\.|\,)\d+)?$/;
var LATIN_REGEXP = /^[a-zA-Z0-9_.]+$/;

angular.module('manageApp.directives', []).directive('integer', function() {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$parsers.unshift(function(viewValue) {
        if (INTEGER_REGEXP.test(viewValue)) {
          // it is valid
          ctrl.$setValidity('integer', true);
          return viewValue;
        } else {
          // it is invalid, return undefined (no model update)
          ctrl.$setValidity('integer', false);
          return undefined;
        }
      });
    }
  };
}).directive('smartFloat', function() {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$parsers.unshift(function(viewValue) {
        if (FLOAT_REGEXP.test(viewValue)) {
          ctrl.$setValidity('float', true);
          return parseFloat(viewValue.replace(',', '.'));
        } else {
          ctrl.$setValidity('float', false);
          return undefined;
        }
      });
    }
  };
}).directive('latinChars', function() {
  return {
    require: 'ngModel',
    link: function(scope, elm, attrs, ctrl) {
      ctrl.$parsers.unshift(function(viewValue) {
        if (LATIN_REGEXP.test(viewValue)) {
          ctrl.$setValidity('latin', true);
          return viewValue;
        } else {
          ctrl.$setValidity('latin', false);
          return undefined;
        }
      });
    }
  };
});