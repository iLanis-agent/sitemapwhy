// Checks of the protocol-text rules (not covered by the XSD oracle), using the examples on sitemaps.org/protocol.html.
const S = require('./engine.js'); let bad = 0;
function ok(name, c) { if (!c) { bad++; console.log('FAIL', name); } else console.log('ok  ', name); }
const H = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
const u = x => '<url><loc>' + x + '</loc></url>';
const warns = (xml, loc) => S.check(xml, loc).issues.filter(i => i.tag === 'loc').length;
const L = 'http://example.com/catalog/sitemap.xml';
ok('valid example in catalog/', warns(H + u('http://example.com/catalog/show?item=23') + u('http://example.com/catalog/show?item=233&amp;user=3453') + '</urlset>', L) === 0);
ok('image/show is not valid in catalog/sitemap.xml', warns(H + u('http://example.com/image/show?item=23') + '</urlset>', L) === 1);
ok('https vs http dropped', warns(H + u('https://example.com/catalog/page1.php') + '</urlset>', L) === 1);
ok('subdomain dropped', warns(H + u('http://subdomain.example.com/x') + '</urlset>', 'http://www.example.com/sitemap.xml') === 1);
ok('port must be repeated', warns(H + u('http://www.example.com/a') + '</urlset>', 'http://www.example.com:100/sitemap.xml') === 1 && warns(H + u('http://www.example.com:100/a') + '</urlset>', 'http://www.example.com:100/sitemap.xml') === 0);
const many = H + u('http://a.com/x').repeat(50001) + '</urlset>';
ok('50,001 URLs flagged', S.check(many, '').issues.some(i => i.tag === 'url' && /50,000/.test(i.msg)));
ok('50,000 URLs not flagged', !S.check(H + u('http://a.com/x').repeat(50000) + '</urlset>', '').issues.some(i => i.tag === 'url'));
ok('2,048 chars ok, 2,049 not', S.check(H + u('http://a.com/' + 'a'.repeat(2035)) + '</urlset>').schemaValid && !S.check(H + u('http://a.com/' + 'a'.repeat(2036)) + '</urlset>').schemaValid);
ok('lowercase scheme/host compare', warns(H + u('HTTP://EXAMPLE.COM/catalog/a') + '</urlset>', L) === 0);
process.exit(bad ? 1 : 0);
