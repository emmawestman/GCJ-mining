/**
 * Scrape job title, url, and location from Taleo jobs page at https://l3com.taleo.net/careersection/l3_ext_us/jobsearch.ftl
 *
 * Usage: $ casperjs scraper.js
 */
var casper = require("casper").create();

var url = 'https://code.google.com/codejam/contest/6254486/scoreboard';
var stats = []

var terminate = function(){
  this.echo("Timed out, exiting");
  casper.finish();
};

var processPage = function (){
  stats = this.evaluate(getTableData)
  require('utils').dump(stats);
};



var getTableData = function(){
  var table_rows = document.querySelectorAll("tbody#scb-table-body");
  return Array.prototype.map.call(table_rows, function(tr) {
    return {
        username : tr.querySelector('td').textContent,
        rank: tr.querySelector('td').textContent,
        penalty: tr.querySelector('td[class=scb-player-name]').textContent
    };
  });
};

casper.start(url);
casper.waitForSelector('table#scb-score-table', processPage, terminate,10000);
casper.run();
