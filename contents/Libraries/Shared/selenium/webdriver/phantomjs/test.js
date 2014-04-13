var page = require('webpage').create();
page.open('http://legendas.tv/busca?q=Grimm%20s03e14%20DIMENSION', function() {
  page.render('test.png');
  phantom.exit();
});