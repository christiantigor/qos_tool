'use strict';

angular.module('qostoolApp')
  .controller('MainCtrl', function ($scope, $location, $filter, $http, $templateCache, $firebase) {
	
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
	
    $scope.initMain = function () {
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
	
    //init map center - for testing to update leaflet parameter after data loaded
	$scope.centerTest = {
        lat: 0,
        lng: 0,
        zoom: 12
    };
	
    $scope.qosResult = [];
	
    $scope.listQosResult = function (data) {
        data.forEach(function (qr) {
            try{
                $scope.qosResult.push({
                    tdDate: qr.tddate,
                    tdTime: qr.tdtime,
                    lat: parseFloat(qr.tlat),
                    lng: parseFloat(qr.tlon),
                    oper: qr.oper,
                    bal: qr.bal,
                    rssi: qr.rssi,
                    sysMode: qr.sysmode,
                    smsSuc: qr.smssuccess,
                    smsTri: qr.smstrial,
                    mosCall: qr.moscall,
                    ping: qr.ping,
                    dload: qr.dload,
                    uload: qr.uload
                });
            }
		    catch(err){
                console.log('error list qosResult');
            }
		});
		//after qosResult data loaded
        //update map center - for testing to update leaflet parameter after data loaded
        $scope.centerTest = {
            lat: -6.7104,
            lng: 106.8344,
            zoom: 12
        };
		//end update map center
        $scope.updateSummary();
        $scope.getSystemMode();
        $scope.getMos();
        $scope.getSms();
        $scope.getPing();
        $scope.getDloadUload();
        //$scope.chartPing();
        //$scope.chartDloadUload();
    };

    //Data for Chart
    $scope.updateSummary = function () {
		//filter XL
        var xlQosRslt = $filter('filter')($scope.qosResult, 'XL');
		//avg MOS
        var xlMosSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.mosCall);
		},0));
        $scope.ovXlMos = (xlMosSum / xlQosRslt.length).toFixed(2);
		//SMS delivery rate
        var xlSmsSuc = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseInt(num.smsSuc);
		},0));
        var xlSmsTri = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseInt(num.smsTri);
		},0));
        $scope.ovXlSms = ((xlSmsSuc/xlSmsTri)*100).toFixed(2);
		//avg ping duration
        var xlPing = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.ping);
		},0));
        $scope.ovXlPing = (xlPing / xlQosRslt.length).toFixed(2);
		//avg download speed
        var xlDload = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.dload);
		},0));
        $scope.ovXlDload = (xlDload / xlQosRslt.length).toFixed(2);
		//avg upload speed
		var xlUload = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.uload);
		},0));
        $scope.ovXlUload = (xlUload / xlQosRslt.length).toFixed(2);
		
		//filter INDOSAT
        var isatQosRslt = $filter('filter')($scope.qosResult, 'INDOSAT');
		//avg MOS
        var isatMosSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.mosCall);
		},0));
        $scope.ovIsatMos = (isatMosSum / isatQosRslt.length).toFixed(2);
		//SMS delivery rate
        var isatSmsSuc = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseInt(num.smsSuc);
		},0));
        var isatSmsTri = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseInt(num.smsTri);
		},0));
        $scope.ovIsatSms = ((isatSmsSuc/isatSmsTri)*100).toFixed(2);
		//avg ping duration
        var isatPing = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.ping);
		},0));
        $scope.ovIsatPing = (isatPing / isatQosRslt.length).toFixed(2);
		//avg download speed
        var isatDload = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.dload);
		},0));
        $scope.ovIsatDload = (isatDload / isatQosRslt.length).toFixed(2);
		//avg upload speed
		var isatUload = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.uload);
		},0));
        $scope.ovIsatUload = (isatUload / isatQosRslt.length).toFixed(2);
		
		//filter TELKOMSEL
        var tselQosRslt = $filter('filter')($scope.qosResult, 'TELKOMSEL');
		//avg MOS
        var tselMosSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.mosCall);
		},0));
        $scope.ovTselMos = (tselMosSum / tselQosRslt.length).toFixed(2);
		//SMS delivery rate
        var tselSmsSuc = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseInt(num.smsSuc);
		},0));
        var tselSmsTri = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseInt(num.smsTri);
		},0));
        $scope.ovTselSms = ((tselSmsSuc/tselSmsTri)*100).toFixed(2);
		//avg ping duration
        var tselPing = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.ping);
		},0));
        $scope.ovTselPing = (tselPing / tselQosRslt.length).toFixed(2);
		//avg download speed
        var tselDload = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.dload);
		},0));
        $scope.ovTselDload = (tselDload / tselQosRslt.length).toFixed(2);
		//avg upload speed
		var tselUload = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.uload);
		},0));
        $scope.ovTselUload = (tselUload / tselQosRslt.length).toFixed(2);
	};
	
    $scope.systemMode = [];
    $scope.getSystemMode = function () {
		//filter XL
        var xlSysMode = [];
        var xlQosRslt = $filter('filter')($scope.qosResult, 'XL');
		//filter no service
        var xlNoService = $filter('filter')(xlQosRslt, 'NO SERVICE');
		//filter gsm
        var xlGsm = $filter('filter')(xlQosRslt, 'GSM');
		//filter wcdma
        var xlWcdma = $filter('filter')(xlQosRslt, 'WCDMA');
		//filter edge
        var xlEdge = $filter('filter')(xlQosRslt, 'EDGE');
		//put to array
        xlSysMode.push('XL');
        xlSysMode.push(xlNoService.length);
        xlSysMode.push(xlGsm.length);
        xlSysMode.push(xlWcdma.length);
        xlSysMode.push(xlEdge.length);
		
		//filter INDOSAT
        var isatSysMode = [];
        var isatQosRslt = $filter('filter')($scope.qosResult, 'INDOSAT');
		//filter no service
        var isatNoService = $filter('filter')(isatQosRslt, 'NO SERVICE');
		//filter gsm
        var isatGsm = $filter('filter')(isatQosRslt, 'GSM');
		//filter wcdma
        var isatWcdma = $filter('filter')(isatQosRslt, 'WCDMA');
		//filter edge
        var isatEdge = $filter('filter')(isatQosRslt, 'EDGE');
		//put to array
        isatSysMode.push('Indosat');
        isatSysMode.push(isatNoService.length);
        isatSysMode.push(isatGsm.length);
        isatSysMode.push(isatWcdma.length);
        isatSysMode.push(isatEdge.length);
		
		//filter TELKOMSEL
        var tselSysMode = [];
        var tselQosRslt = $filter('filter')($scope.qosResult, 'TELKOMSEL');
		//filter no service
        var tselNoService = $filter('filter')(tselQosRslt, 'NO SERVICE');
		//filter gsm
        var tselGsm = $filter('filter')(tselQosRslt, 'GSM');
		//filter wcdma
        var tselWcdma = $filter('filter')(tselQosRslt, 'WCDMA');
		//filter edge
        var tselEdge = $filter('filter')(tselQosRslt, 'EDGE');
		//put to array
        tselSysMode.push('Telkomsel');
        tselSysMode.push(tselNoService.length);
        tselSysMode.push(tselGsm.length);
        tselSysMode.push(tselWcdma.length);
        tselSysMode.push(tselEdge.length);
		
		//put to scope array
        $scope.systemMode.push(xlSysMode);
        $scope.systemMode.push(isatSysMode);
        $scope.systemMode.push(tselSysMode);
		//after systemMode data loaded
        $scope.chartSystemMode();
    };

    $scope.mos = [];
    $scope.getMos = function() {
		//filter XL
        var xlMos = [];
        var xlQosRslt = $filter('filter')($scope.qosResult, 'XL');
		//avg MOS
        var xlMosSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.mosCall);
		},0));
        var xlMosVal = (xlMosSum / xlQosRslt.length).toFixed(2);
		//put to array
        xlMos.push('XL');
        xlMos.push(xlMosVal);
        for(var i=0; i<4; i++){
            xlMos.push(0); //no value for other city
		};
		
		//filter INDOSAT
        var isatMos = [];
        var isatQosRslt = $filter('filter')($scope.qosResult, 'INDOSAT');
		//avg MOS
        var isatMosSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.mosCall);
		},0));
        var isatMosVal = (isatMosSum / isatQosRslt.length).toFixed(2);
		//put to array
        isatMos.push('Indosat');
        isatMos.push(isatMosVal);
        for(var i=0; i<4; i++){
            isatMos.push(0); //no value for other city
		};
		
		//filter TELKOMSEL
        var tselMos = [];
        var tselQosRslt = $filter('filter')($scope.qosResult, 'TELKOMSEL');
		//avg MOS
        var tselMosSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.mosCall);
		},0));
        var tselMosVal = (tselMosSum / tselQosRslt.length).toFixed(2);
		//put to array
        tselMos.push('Telkomsel');
        tselMos.push(tselMosVal);
        for(var i=0; i<4; i++){
            tselMos.push(0); //no value for other city
		};
		
		//put to scope array
        $scope.mos.push(xlMos);
        $scope.mos.push(isatMos);
        $scope.mos.push(tselMos);
		//after mos data loaded
        $scope.chartMos();
    };	
	
    $scope.sms = [];
    $scope.getSms = function() {
		//filter XL
        var xlSmsFail = [];
        var xlSmsSuc = [];
        var xlQosRslt = $filter('filter')($scope.qosResult, 'XL');
		//count smsTri and smsSuc
        var xlSmsTriSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseInt(num.smsTri);
        },0));
        var xlSmsSucSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseInt(num.smsSuc);
        },0));
		//put to array
        xlSmsFail.push('XL_Fail');
        xlSmsFail.push(xlSmsTriSum - xlSmsSucSum);
        for(var i=0; i<4; i++){
            xlSmsFail.push(0);
		};
        xlSmsSuc.push('XL_Dlvr');
        xlSmsSuc.push(xlSmsSucSum);
        for(var i=0; i<4; i++){
            xlSmsSuc.push(0);
		};
		
		//filter INDOSAT
        var isatSmsFail = [];
        var isatSmsSuc = [];
        var isatQosRslt = $filter('filter')($scope.qosResult, 'INDOSAT');
		//count smsTri and smsSuc
        var isatSmsTriSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseInt(num.smsTri);
        },0));
        var isatSmsSucSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseInt(num.smsSuc);
        },0));
		//put to array
        isatSmsFail.push('Isat_Fail');
        isatSmsFail.push(isatSmsTriSum - isatSmsSucSum);
        for(var i=0; i<4; i++){
            isatSmsFail.push(0);
		};
        isatSmsSuc.push('Isat_Dlvr');
        isatSmsSuc.push(isatSmsSucSum);
        for(var i=0; i<4; i++){
            isatSmsSuc.push(0);
		};
		
		//filter TELKOMSEL
        var tselSmsFail = [];
        var tselSmsSuc = [];
        var tselQosRslt = $filter('filter')($scope.qosResult, 'TELKOMSEL');
		//count smsTri and smsSuc
        var tselSmsTriSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseInt(num.smsTri);
        },0));
        var tselSmsSucSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseInt(num.smsSuc);
        },0));
		//put to array
        tselSmsFail.push('Tsel_Fail');
        tselSmsFail.push(tselSmsTriSum - tselSmsSucSum);
        for(var i=0; i<4; i++){
            tselSmsFail.push(0);
		};
        tselSmsSuc.push('Tsel_Dlvr');
        tselSmsSuc.push(tselSmsSucSum);
        for(var i=0; i<4; i++){
            tselSmsSuc.push(0);
		};
		
		//put to scope array
		$scope.sms.push(xlSmsFail);
        $scope.sms.push(xlSmsSuc);
		$scope.sms.push(isatSmsFail);
        $scope.sms.push(isatSmsSuc);
		$scope.sms.push(tselSmsFail);
        $scope.sms.push(tselSmsSuc);
		//after sms data loaded
        $scope.chartSms();
	};
	
    $scope.ping = [];
    $scope.getPing = function() {
		//filter XL
        var xlPing = [];
        var xlQosRslt = $filter('filter')($scope.qosResult, 'XL');
		//avg ping duration
        var xlPingSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.ping);
		},0));
        var xlPingVal = (xlPingSum / xlQosRslt.length).toFixed(2);
		//put to array
        xlPing.push('XL');
        xlPing.push(xlPingVal);
        for(var i=0; i<4; i++){
            xlPing.push(0); //no value for other city
		};
		
		//filter INDOSAT
        var isatPing = [];
        var isatQosRslt = $filter('filter')($scope.qosResult, 'INDOSAT');
		//avg ping duration
        var isatPingSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.ping);
		},0));
        var isatPingVal = (isatPingSum / isatQosRslt.length).toFixed(2);
		//put to array
        isatPing.push('Indosat');
        isatPing.push(isatPingVal);
        for(var i=0; i<4; i++){
            isatPing.push(0); //no value for other city
		};
		
		//filter TELKOMSEL
        var tselPing = [];
        var tselQosRslt = $filter('filter')($scope.qosResult, 'TELKOMSEL');
		//avg ping duration
        var tselPingSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.ping);
		},0));
        var tselPingVal = (tselPingSum / tselQosRslt.length).toFixed(2);
		//put to array
        tselPing.push('Telkomsel');
        tselPing.push(tselPingVal);
        for(var i=0; i<4; i++){
            tselPing.push(0); //no value for other city
		};
		
		//put to scope array
        $scope.ping.push(xlPing);
        $scope.ping.push(isatPing);
        $scope.ping.push(tselPing);
		//after ping data loaded
        $scope.chartPing();
		
	};
	
    $scope.dloadUload = [];
    $scope.getDloadUload = function () {
		//filter XL
        var xlDload = [];
        var xlUload = [];
        var xlQosRslt = $filter('filter')($scope.qosResult, 'XL');
		//avg download and upload speed
        var xlDloadSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.dload);
		},0));
        var xlDloadVal = (xlDloadSum / xlQosRslt.length).toFixed(2);
        var xlUloadSum = (_.reduce(xlQosRslt, function (memo,num){
            return memo + parseFloat(num.uload);
		},0));
        var xlUloadVal = (xlUloadSum / xlQosRslt.length).toFixed(2);
		//put to array
        xlDload.push('XL_Dwnld');
        xlDload.push(xlDloadVal);
        for(var i=0; i<4; i++){
            xlDload.push(0); //no value for other city
		};
        xlUload.push('XL_Upld');
        xlUload.push(xlUloadVal);
        for(var i=0; i<4; i++){
            xlUload.push(0); //no value for other city
		};
		
		//filter INDOSAT
        var isatDload = [];
        var isatUload = [];
        var isatQosRslt = $filter('filter')($scope.qosResult, 'INDOSAT');
		//avg download and upload speed
        var isatDloadSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.dload);
		},0));
        var isatDloadVal = (isatDloadSum / isatQosRslt.length).toFixed(2);
        var isatUloadSum = (_.reduce(isatQosRslt, function (memo,num){
            return memo + parseFloat(num.uload);
		},0));
        var isatUloadVal = (isatUloadSum / isatQosRslt.length).toFixed(2);
		//put to array
        isatDload.push('Isat_Dwnld');
        isatDload.push(isatDloadVal);
        for(var i=0; i<4; i++){
            isatDload.push(0); //no value for other city
		};
        isatUload.push('Isat_Upld');
        isatUload.push(isatUloadVal);
        for(var i=0; i<4; i++){
            isatUload.push(0); //no value for other city
		};
		
		//filter TELKOMSEL
        var tselDload = [];
        var tselUload = [];
        var tselQosRslt = $filter('filter')($scope.qosResult, 'TELKOMSEL');
		//avg download and upload speed
        var tselDloadSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.dload);
		},0));
        var tselDloadVal = (tselDloadSum / tselQosRslt.length).toFixed(2);
        var tselUloadSum = (_.reduce(tselQosRslt, function (memo,num){
            return memo + parseFloat(num.uload);
		},0));
        var tselUloadVal = (tselUloadSum / tselQosRslt.length).toFixed(2);
		//put to array
        tselDload.push('Tsel_Dwnld');
        tselDload.push(tselDloadVal);
        for(var i=0; i<4; i++){
            tselDload.push(0); //no value for other city
		};
        tselUload.push('Tsel_Upld');
        tselUload.push(tselUloadVal);
        for(var i=0; i<4; i++){
            tselUload.push(0); //no value for other city
		};
		
		//put to scope array
        $scope.dloadUload.push(xlDload);
        $scope.dloadUload.push(xlUload);
        $scope.dloadUload.push(isatDload);
        $scope.dloadUload.push(isatUload);
        $scope.dloadUload.push(tselDload);
        $scope.dloadUload.push(tselUload);
		
		//after download and upload data loaded
        $scope.chartDloadUload();
	};

    //Charts
    $scope.chartSystemMode = function () {
        c3.generate({
          bindto: '#chartSystemMode',
          data: {
		    columns: $scope.systemMode,
            types: {
                XL: 'bar',
				Indosat: 'bar',
				Telkomsel: 'bar'
			},
			colors: {
                XL: '#8493CA',
                Indosat: '#FFF79A',
                Telkomsel: '#F7977A' 
			}
          },
          axis: {
            x: {
                type: 'categorized',
                categories: ['No Service', 'GSM', 'WCDMA', 'EDGE']
			},
            y: {
                label: 'System Mode'
            }
          }
        });
	};

    $scope.chartMos = function () {
        c3.generate({
          bindto: '#chartMos',
          data: {
            columns: $scope.mos,
            types: {
                XL: 'spline',
				Indosat: 'spline',
                Telkomsel: 'spline'
            },
            colors: {
                XL: '#8493CA',
                Indosat: '#FFF79A',
                Telkomsel: '#F7977A'
			}
		  },
          axis: {
            x: {
                type: 'categorized',
                categories: ['Bandung', 'Cimahi', 'Sukabumi', 'Bogor', 'Depok']
			},
            y: {
                label: 'MOS',
                max: 5,
                min: 0
            }
		  }
		});
    };
	
	$scope.chartSms = function () {
        c3.generate({
          bindto: '#chartSms',
          data: {
            columns: $scope.sms,
            type: 'bar',
            groups: [
                ['XL_Fail','XL_Dlvr'],
                ['Isat_Fail','Isat_Dlvr'],
                ['Tsel_Fail','Tsel_Dlvr']
			],
            colors: {
                XL_Dlvr: '#8493CA',
                XL_Fail: '#D7D7D7',
                Isat_Dlvr: '#FFF79A',
                Isat_Fail: '#C2C2C2',
                Tsel_Dlvr: '#F7977A',
                Tsel_Fail: '#ACACAC'
			}
		  },
		  axis: {
            x: {
                type: 'categorized',
                categories: ['Bandung', 'Cimahi', 'Sukabumi', 'Bogor', 'Depok']
			}
		  }
		});
	};
	
    $scope.chartPing = function () {
        c3.generate({
          bindto: '#chartPing',
          data: {
            columns: $scope.ping,
            types: {
                XL: 'line',
                Indosat: 'line',
                Telkomsel: 'line'
			},
            colors: {
                XL: '#8493CA',
                Indosat: '#FFF79A',
                Telkomsel: '#F7977A'
			}
		  },
          axis: {
            x: {
                type: 'categorized',
                categories: ['Bandung', 'Cimahi', 'Sukabumi', 'Bogor', 'Depok']
			},
            y: {
                label: 'ms'
            }
		  }
		});
    };
	
    $scope.chartDloadUload = function () {
        c3.generate({
          bindto: '#chartDloadUload',
          data: {
            columns: $scope.dloadUload,
            type: 'bar',
            groups: [
                ['XL_Dwnld','XL_Upld'],
                ['Isat_Dwnld','Isat_Upld'],
                ['Tsel_Dwnld','Tsel_Upld']
			],
            colors: {
                XL_Dwnld: '#8493CA',
                XL_Upld: '#0054A6',
                Isat_Dwnld: '#FFF79A',
                Isat_Upld: '#FFF200',
                Tsel_Dwnld: '#F7977A',
                Tsel_Upld: '#ED1C24'
			}
		  },
          axis: {
            x: {
                type: 'categorized',
                categories: ['Bandung', 'Cimahi', 'Sukabumi', 'Bogor', 'Depok']
			},
            y: {
                label: 'Mbits/s'
            }
		  }
		});
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
    $scope.markers = {};
	//end leaflet
	
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
	
	//report
    $scope.drawRestaurantReport = function(){
        var doc = new jsPDF('p', 'mm', 'a4');
        var top = 13.5;
        var left = 15;
        var width = 180;
		var half = 37.5; //start of table
        var height = 270;
        var margin = 5;
        var lineHeight = 8;
        
		//splitting transaction list
        var iArr;
		var jArr;
		var tempArr;
		var chunk = 10; //amount of transactions on a page
		var fPg = true; //indicator for first page
        var page = 1;
		
		for (iArr=0,jArr=$scope.restaurantTransactions.length;iArr<jArr;iArr+=chunk){
            tempArr = $scope.restaurantTransactions.slice(iArr,iArr+chunk);
			
			//check if first page
			if(fPg){
                fPg = false;
			}
			else{
                doc.addPage();
            }
			
			//report border
            doc.setDrawColor(0);
            doc.rect(left, top, width, height, 'stroke');
			
			//document title and date
            doc.setFontSize(28);
            doc.setFontStyle("bold");
            doc.text(left + margin / 4, top + 2.25 * margin, $scope.selectedTaxpayer.name);
            doc.setTextColor(215, 24, 104);
            doc.setFontStyle("italic");
            doc.text(left + 3 * width / 4, top + 2.25 * margin, $scope.todayDate.monYear);
            doc.setTextColor(0);        
            //line under title row
            doc.lines([
                [width, 0]
            ], left, 2 * lineHeight + top)
			
			//create table
            for(var i=0; i <= (tempArr.length + 1); i++){
                //create rows as many as transactions on tempArr + 1 for header row
                doc.lines([
                    [width, 0]
                ], left, half + i * lineHeight)
            
                //create columns of |Id|Date Time|Total(Rp)|Service(Rp)|Receipt|
                doc.lines([
                    [0, i * lineHeight]
                ], left + width / 5, half);
                doc.lines([
                    [0, i * lineHeight]
                ], left + 2 * width / 5, half);
                doc.lines([
                    [0, i * lineHeight]
                ], left + 3 * width / 5, half);
                doc.lines([
                    [0, i * lineHeight]
                ], left + 4 * width / 5, half);
                doc.lines([
                    [0, i * lineHeight]
                ], left + 5 * width / 5, half);
            
                //header row
                doc.setFontSize(8);
                doc.setFontStyle("italic");
                doc.setTextColor(96, 189, 21);
                doc.text('Id', left + margin / 4, half + margin);
                doc.text('Date Time', left + width / 5 + margin / 4, half + margin);
                doc.text('Total(Rp)', left + 2 * width / 5 + margin / 4, half + margin);
                doc.text('Service(Rp)', left + 3 * width / 5 + margin / 4, half + margin);
                doc.text('Receipt', left + 4 * width / 5 + margin / 4, half + margin);
                doc.setTextColor(0);
            }
			
            //fill the table
            var iTrans =1;
            doc.setFontStyle("normal");
            for (var t in tempArr) {
                doc.text(left + margin / 4, iTrans * lineHeight + half + margin , tempArr[t].id.toString());
                doc.text(left + width / 5 + margin / 4, iTrans * lineHeight + half + margin , tempArr[t].time);
                doc.text(left + 2 * width / 5 + margin / 4, iTrans * lineHeight + half + margin , $scope.addDot(tempArr[t].total));
                doc.text(left + 3 * width / 5 + margin / 4, iTrans * lineHeight + half + margin , $scope.addDot(tempArr[t].service));
                doc.text(left + 4 * width / 5 + margin / 4, iTrans * lineHeight + half + margin , tempArr[t].receipt.toString());
                iTrans++;
            }
			
			//page number
            doc.setFontSize(10);
            doc.setFontStyle("bold");
            doc.text(left + width / 2, top + height + lineHeight, page.toString());
            page++;
        }
		
        doc.save('Transaction List_' + $scope.selectedTaxpayer.name + '_' + $scope.todayDate.monYear + '.pdf');
	};
	
	/*end transaction page*/
	
    $scope.$watch('centerTest',function(){
        //$scope.center.lat = $scope.centerTest.lat;
		//$scope.center.lng = $scope.centerTest.lng;
		$scope.qosResult.forEach(function (qr){
		try{
		    $scope.markers.push({
			    lat: qr.lat,
				lng: qr.lng,
				focus: true
			});
		}
		catch(err){
		    console.log("error woy");
		}
		});
		//console.log($scope.markers);
	});
	$scope.$watch('qosResult',function(){
        //start run
		$scope.markers = [
		    {
			    lat: -6.9101,
				lng: 107.6344,
				message: "marker 1"
			},
            {
			    lat: -6.9104,
				lng: 107.6344,
				message: "marker 2"
			}
		];
		//end run
        // $scope.qosResult.forEach(function (qr){
		// try{
		    // $scope.markers.push({
			    // lat: qr.lat,
				// lng: qr.lng
			// });
		// }
		// catch(err){
		    // console.log("error woy");
		// }
		// });
		// console.log($scope.markers);
	});
});