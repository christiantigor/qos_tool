'use strict';

angular.module('qostoolApp')
  .controller('TaxpayerCtrl', function ($scope, $location, $filter, $http, $templateCache) {
    
    $scope.go = function (path) {
        $location.url(path);
    };
	
    $scope.goTo = function (type, id) {
        if(type === 'Hotel'){
            $location.url('transHotel?id=' + id);
		}
        else if(type === 'Parking'){
            $location.url('transParking?id=' + id);
        }
		else{
            $location.url('transRestaurant?id=' + id);
		}
    };
	
    //date
    $scope.todayDate = {
        'day':'',
        'date':'',
        'month':'',
        'year':''
    };
	
    $scope.gettingDate = function(){
        var today = new Date();
        
        var weekday = new Array('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
        var dy = weekday[today.getDay()];
        
        var dd = today.getDate();
        var month = new Array('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
        var mm = month[today.getMonth()];
        var yyyy = today.getFullYear();
        
        if(dd<10){dd='0'+dd}
        
        $scope.todayDate.day = dy;
        $scope.todayDate.date = dd;
        $scope.todayDate.month = mm;
        $scope.todayDate.year = yyyy;
        $scope.todayDate.monYear = mm + ' ' + yyyy;
    }
    //end date
    
    $scope.initTaxpayer = function () {
        $scope.getTaxpayers();
    };
	
    $scope.addDot = function (nStr) {
        nStr += '';
        var x = nStr.split('.');
        var x1 = x[0];
        var x2 = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while(rgx.test(x1)){
            x1 = x1.replace(rgx, '$1' + '.' + '$2');
        }
        return x1 + x2;
    };
	
    /*taxpayer page*/
    $scope.urlTaxpayers = 'http://testingpurpose.eu5.org/getTaxPayers';
	
    $scope.getTaxpayers = function () {
      $http({
        method: 'GET',
        url: $scope.urlTaxpayers,
        data: '',
        cache: $templateCache }).
      success(function(data) {
        $scope.listTaxpayers(data);
        return data;
      }).
      error(function(data) {
        $scope.getTaxpayers();
        return data;
      });
    };

    $scope.taxpayers = [];
	
    $scope.listTaxpayers = function (taxpayerList, purpose) {
        taxpayerList.forEach(function (t) {
            try{
                $scope.taxpayers.push({
                    id: t.taxPayersId,
                    type: t.type,
                    name: t.name,
                    address: t.address,
                    phone: t.phone,
                    monitoredTax: parseInt(t.monitoredTax),
                    validatedTax: parseInt(t.validatedTax),
                    onDevice: t.onDevice,
                    offDevice: t.offDevice,
                    lat: parseFloat(t.lat),
                    lng: parseFloat(t.lng),
                    message: '<h5><right><strong>' + t.type + ' - ' + t.name +
					'</strong></right></h5><h6><strong>' + t.address +
					'</strong></h6><h6>Monitored tax: <strong><font color="grey">Rp ' +
					$scope.addDot(t.monitoredTax) + ',00</font></strong></h6><h6>Validated tax: <strong><font color="blue">Rp ' +
					$scope.addDot(t.validatedTax)+ ',00</font><strong></h6>'
                });
            }
		    catch(err){
                console.log('error list taxpayer');
            }
		});
		//after taxpayers data loaded
    };
	
	
	//leaflet
    $scope.defaults = {
	    scrollWheelZoom: false
    };
    $scope.center = {
        lat: -6.9104,
        lng: 107.6344,
        zoom: 12
      };
    $scope.markers = {
	    m1: {
		    lat: 52.52,
            lng: 13.40
        }
	};
	
	//get taxpayer icon
    $scope.getTaxpayerIcon = function (tp){
        if(tp.type === 'Hotel') {
            return 'fa fa-building-o';
        }
        else if(tp.type === 'Parking') {
            return 'fa fa-truck';
        }
        else if(tp.type === 'Restaurant') {
            return 'fa fa-cutlery';
        }
        else{
            return 'fa fa-windows';
        }
    };

	/*end taxpayer page*/
	
    $scope.$watch('searchText', function() {
	
        $scope.filteredTaxpayers = $filter('filter')($scope.taxpayers, $scope.searchText);
		
        if($scope.searchText === '' || $scope.initMap === 0){
            $scope.center = {
                lat: -6.219404,
                lng: 106.812365,
                zoom: 12 
            };
            $scope.initMap = 1;
        }
		else{
            if($scope.filteredTaxpayers.length > 0){
                $scope.center = {
                    lat: $scope.filteredTaxpayers[0].lat,
                    lng: $scope.filteredTaxpayers[0].lng,
                    zoom: 14
                };
			}
            else{
                $scope.center = {
                    lat: -6.9104,
                    lng: 107.6344,
                    zoom: 12
                };
            }
        }
		
    });
});