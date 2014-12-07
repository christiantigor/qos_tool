'use strict';

angular.module('qostoolApp')
  .controller('TransRestaurantCtrl', function ($scope, $location, $filter, $http, $templateCache, ngTableParams) {
    
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
        $scope.todayDate.monthNum = today.getMonth() + 1;
        $scope.todayDate.year = yyyy;
        $scope.todayDate.monYear = mm + ' ' + yyyy;
    }
    //end date
	
    $scope.initTransaction = function () {
        $scope.gettingDate();
        $scope.getTaxpayers();
        //$scope.getTaxes();
        //$scope.getTransactions();
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
	
	//cat: bikin servis ?fx=getTaxPayers&id=123456
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
	
    $scope.listTaxpayers = function (taxpayerList) {
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
                    table: t.table,
                    message: '<h5><right><strong>' + t.type + ' - ' + t.name +
					'</strong></right></h5><h6><strong>' + t.address +
					'</strong></h6><h6>Monitored tax: <strong><font color="grey">Rp ' +
					t.monitoredTax + ',00</font></strong></h6><h6>Validated tax: <strong><font color="blue">Rp ' +
					t.validatedTax+ ',00</font><strong></h6>'
                });
            }
		    catch(err){
                console.log('error list taxpayer');
            }
		});
		
		//after taxpayers data loaded
        $scope.currentTaxpayer();		
    };
	
    $scope.currentTaxpayer = function () {
        var selectedTaxpayer;
        var urlParam;
		
        var taxpayerParam = $location.url();
		for (var i=0; i<taxpayerParam.length; i++) {
            if ((taxpayerParam[i] === '=') && (i < taxpayerParam.length)) {
                urlParam = taxpayerParam[i+1];
            }
            else if ((urlParam != undefined) && (i+1 < taxpayerParam.length)) {
                urlParam += taxpayerParam[i+1];
			}
		}
        urlParam += '=';
        //console.log(urlParam);
        selectedTaxpayer = _.filter($scope.taxpayers, function (obj) {
            return obj.id == urlParam;
        });
        $scope.selectedTaxpayer = JSON.parse(JSON.stringify(selectedTaxpayer[0]));
		
        //after selected restaurant is known
        $scope.getTaxes();
        $scope.getTransactions();
	};
	
    $scope.urlTaxes = 'http://testingpurpose.eu5.org/getRestaurantTaxRecords/';
	
    $scope.getTaxes = function () {
	  $http({
        method: 'GET',
        url: $scope.urlTaxes + $scope.selectedTaxpayer.table + '/' + $scope.selectedTaxpayer.id + '/' + $scope.todayDate.year + '/' + $scope.todayDate.monthNum,
        data: '',
        cache: $templateCache }).
      success(function(data) {
        $scope.listTaxes(data);
        return data;
      }).
      error(function(data) {
        $scope.getTaxes();
        return data;
      });
    };
	
    $scope.restaurantTaxes = [];
	
    $scope.listTaxes = function (taxList) {
        var date = [];
        date.push('date');
        var validated = [];
        validated.push('validated');
        var notValidated = [];
        notValidated.push('not-validated');
        var dt;
		
        angular.forEach(taxList, function (objY, year) {
            //console.log(year);
            angular.forEach(objY, function (objM, month) {
                //console.log(month);
                angular.forEach(objM, function (total, objT) {
                    //console.log(total);
                    dt = year+month;
                    date.push(dt);
                    validated.push(total);
					notValidated.push(total-1000000);
                });
			});
		});
        $scope.restaurantTaxes.push(date);
        $scope.restaurantTaxes.push(validated);
        $scope.restaurantTaxes.push(notValidated);

        //after taxes data loaded
        $scope.chartTaxRecords();
		
    };
	
    $scope.urlTransactions = 'http://testingpurpose.eu5.org/getRestaurantTransListByDate/';
	
    $scope.getTransactions = function () {
      $http({
        method: 'GET',
        url: $scope.urlTransactions + $scope.selectedTaxpayer.table + '/' + $scope.selectedTaxpayer.id + '/0' + $scope.todayDate.monthNum + '-' + $scope.todayDate.year + '/720/1',
        data: '',
        cache: $templateCache }).
      success(function(data) {
        $scope.listTransactions(data);
        return data;
      }).
      error(function(data) {
        $scope.getTransactions();
        return data;
      });
    };

    $scope.restaurantTransactions = [];
    var restaurantTransData = []; //for table
    $scope.restaurantTransChart = []; //for transaction chart
	
    $scope.listTransactions = function (transactionList) {
        var date = [];
        date.push('date');
        var cashier01 = [];
        cashier01.push('cashier 01');
        var cashier02 = [];
        cashier02.push('cashier 02');
		
        transactionList.forEach(function (t) {
            try{
                $scope.restaurantTransactions.push({
                    transId: t.transId,
                    dateTime: t.dateTime,
                    total: parseInt(t.total),
                    service: parseInt(t.service),
                    receipt: t.receipt
                });
                restaurantTransData.push({ //data must be put here to show them on table
                    transId: t.transId,
                    dateTime: t.dateTime,
                    total: parseInt(t.total),
                    service: parseInt(t.service),
                    receipt: t.receipt
                });
                date.push(t.dateTime);
                cashier01.push(t.total);
                cashier02.push(t.service);
            }
		    catch(err){
                console.log('error list transaction');
            }
		});
		
        $scope.restaurantTransChart.push(date);
        $scope.restaurantTransChart.push(cashier01);
        $scope.restaurantTransChart.push(cashier02);
		
        //after transactions data loaded
		//console.log($scope.restaurantTransChart);
		$scope.setTransactionTableParams();
        $scope.chartTransRecords();
    };
	
    $scope.chartTaxRecords = function () {
        c3.generate({
          bindto: '#chartTaxRecords',
          data: {
            x: 'date',
            x_format: '%Y%m',
            columns: $scope.restaurantTaxes,
            type: 'bar',
            groups: [
              ['validated', 'not-validated']
            ],
            subchart: {
                show: true
            },
          },
          grid: {
              y: {
                lines: [{value:0}]
              }
            },
            axis: {
              x: {
                type: 'timeseries',
                tick: {
                  format: '%b %y'
                }
              },
              y: {
                label: 'Rp'
              }
            }
          });
    };
	  
    $scope.chartTransRecords = function () {
        c3.generate({
          bindto: '#chartTransRecords',
          data: {
            x: 'date',
            x_format: '%Y-%m-%d %H:%M:%S',
            columns: $scope.restaurantTransChart
          },
          axis: {
            x: {
              type: 'timeseries',
              tick: {
                format: '%d %b %H:%M'
              }
            },
            y: {
              label: 'Transaction'
            }
          },
		  subchart: {
            show: true
          }
        });
    };
	
	//transaction table
    $scope.setTransactionTableParams = function () {
        $scope.transactionTableParams = new ngTableParams({
			page: 1,            // show first page
			count: 10,          // count per page
			filter: {
				transId: ''       // initial filter
			},
			sorting: {
				transId: 'asc'     // initial sorting
			}
		}, {
			total: restaurantTransData.length, // length of data
			getData: function($defer, params) {
				// use build-in angular filter
				var filteredData = params.filter() ?
						$filter('filter')(restaurantTransData, params.filter()) :
						restaurantTransData;
				var orderedData = params.sorting() ?
						$filter('orderBy')(filteredData, params.orderBy()) :
						restaurantTransData;
				params.total(orderedData.length); // set total for recalc pagination
				$defer.resolve(orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count()));
			}
        });
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
		var chunk = 20; //amount of transactions on a page
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
                doc.text('Transaction Id', left + margin / 4, half + margin);
                doc.text('Date', left + width / 5 + margin / 4, half + margin);
                doc.text('Total (Rp)', left + 2 * width / 5 + margin / 4, half + margin);
                doc.text('Service (Rp)', left + 3 * width / 5 + margin / 4, half + margin);
                doc.text('Receipt', left + 4 * width / 5 + margin / 4, half + margin);
                doc.setTextColor(0);
            }
			
            //fill the table
            var iTrans =1;
            doc.setFontStyle("normal");
			//console.log(tempArr);
            for (var t in tempArr) {
                doc.text(left + margin / 4, iTrans * lineHeight + half + margin , tempArr[t].transId);
                doc.text(left + width / 5 + margin / 4, iTrans * lineHeight + half + margin , tempArr[t].dateTime);
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
	
});