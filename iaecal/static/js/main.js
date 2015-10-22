(function() {
	'use strict';

	var app = angular.module('IAECalApp', ['angularSpinner']);

	app.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
		// Compatibility with jinja2 templates
		$interpolateProvider.startSymbol('{a');
		$interpolateProvider.endSymbol('a}');
		
		// Take care of the CSRF protection
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	}]);

	app.controller('IAECalController',	['$scope', '$http', 'usSpinnerService',
			function($scope, $http, usSpinnerService) {
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
					}).
					success(function(data) {
						angular.forEach(data, function(value, field) {
							$scope.serverData[field] = value;
						});
						$scope.showUrl = true;
					}).
					error(function(data) {
						// Clean up errors
						$scope.errors = {};

						// Parse response
						angular.forEach(data.errors, function(errors, field) {
							if ($scope.form.hasOwnProperty(field)) {
								// mark field invalid
								$scope.form[field].$setValidity('server', false);
							}

							// display server error messages
							$scope.errors[field] = errors.join(', ');
						});
					}).
					finally(function() {
						usSpinnerService.stop('spinner-form');
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
