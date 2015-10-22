(function() {
	'use strict';

	var app = angular.module('IAECalApp', ['angularSpinner']);

	// Compatibility with jinja2 templates
	app.config(['$interpolateProvider', function($interpolateProvider) {
		$interpolateProvider.startSymbol('{a');
		$interpolateProvider.endSymbol('a}');
	}]);

	app.controller('IAECalController',	['$scope', '$http', '$timeout', 'usSpinnerService',
			function($scope, $http, $timeout, usSpinnerService) {
				// Take care of the CSRF protection
				var csrftoken = angular.element('meta[name=csrf-token]').attr('content');
				$http.defaults.headers.post['X-CSRFToken'] = csrftoken;

				// Clean up errors
				$scope.errors = {};

				// Nothing to show at first
				$scope.showUrl = false;

				// Process form on submission
				$scope.submitForm = function() {
					if ($scope.showUrl)
						return;

					// Init requested data
					$scope.serverData = {};

					usSpinnerService.spin('spinner-form');

					$http.post('/get-url', {
						'username': $scope.username,
						'password': $scope.password,
					}).success(function(data) {
						angular.forEach(data, function(value, field) {
							$scope.serverData[field] = value;
						});
						$scope.showUrl = true;
					}).error(function(data) {
						angular.forEach(data.errors, function(errors, field) {
							// field is invalid
							$scope.form[field].$setValidity('server', false);

							// display server error messages
							$scope.errors[field] = errors.join(', ');
						});
					}).finally(function() {
						$timeout(function() {
							usSpinnerService.stop('spinner-form');
						}, 100);
					});
				};
			}
	]);

	// Wait for changes in the form and invalidates previous errors
	app.directive('serverError', function() {
		return {
			restrict: 'A',
			require: '?ngModel',
			link: function(scope, element, attrs, ctrl) {
				element.on('change', function() {
					scope.$apply(function() {
						ctrl.$setValidity('server', true);
					});
				});
			},
		};
	});
}());
