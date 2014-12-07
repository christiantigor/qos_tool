'use strict';

angular.module('qostoolApp')
  .controller('AnalyticsCtrl', function ($scope, $location, $filter, $http, $templateCache, $firebase, ngTableParams) {
	
    $scope.go = function (path) {
        $location.url(path);
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
    
    $scope.initAnalytics = function () {
        $scope.getQosResult();
    };
	
    $scope.urlQosResult = 'https://radiant-torch-2376.firebaseio.com/qosresult.json';
	
    $scope.getQosResult = function () {
      $http({
        method: 'GET',
        url: $scope.urlQosResult,
        data: '',
        cache: $templateCache }).
      success(function(data) {
        $scope.listQosResult(data);
        return data;
      }).
      error(function(data) {
        $scope.getQosResult();
        return data;
      });
    };

    $scope.qosResult = [];
    var qosResultData = []; //for table
	
    $scope.listQosResult = function (data) {
        data.forEach(function (qr) {
            try{
                $scope.qosResult.push({
                    tdDate: qr.tddate,
                    tdTime: qr.tdtime,
                    tLat: qr.tlat,
                    tLon: qr.tlon,
                    oper: qr.oper,
                    bal: qr.bal,
                    rssi: qr.rssi,
                    sysMode: qr.sysmode,
                    sms: parseInt(qr.smssuccess)/parseInt(qr.smstrial),
                    mosCall: qr.moscall,
                    ping: qr.ping,
                    dLoad: qr.dload,
                    uLoad: qr.uload
                });
                qosResultData.push({ //data must be put here to show them on table
                    tdDate: qr.tddate,
                    tdTime: qr.tdtime,
                    tLat: qr.tlat,
                    tLon: qr.tlon,
                    oper: qr.oper,
                    bal: qr.bal,
                    rssi: qr.rssi,
                    sysMode: qr.sysmode,
                    sms: parseInt(qr.smssuccess)/parseInt(qr.smstrial),
                    mosCall: qr.moscall,
                    ping: qr.ping,
                    dLoad: qr.dload,
                    uLoad: qr.uload
				});
            }
		    catch(err){
                console.log('error list qosResult');
            }
		});
		//after qosResult data loaded
		//console.log($scope.qosResult);
        $scope.setQosResultTableParams()
    };
	
	//qosResult table
    $scope.setQosResultTableParams = function () {
        $scope.qosResultTableParams = new ngTableParams({
            page: 1, //show first page
            count: 10, //count per page
            filter: {
                tdDate: '' //initial filter
			},
            sorting: {
                tdDate: 'asc' //initial sorting
			}
		},  {
            total: qosResultData.length, //length of data
            getData: function($defer, params) {
				//use build-in angular filter
                var filteredData = params.filter() ?
                    $filter('filter')(qosResultData, params.filter()) :
                    qosResultData;
                var orderedData = params.sorting() ?
                    $filter('orderBy')(filteredData, params.orderBy()) :
                    qosResultData;
                params.total(orderedData.length); //set total for recalc pagination
                $defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
			}
		});
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
});