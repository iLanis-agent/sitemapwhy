// node test-engine.js file.jsonl [more.jsonl]: compares engine verdicts with libxml2 + the real sitemaps.org XSDs (oracle.py output).
const S = require('./engine.js'), fs = require('fs');
let n = 0, mism = [], wfMis = 0, tot = { wf: 0, valid: 0 };
for (const f of process.argv.slice(2)) for (const l of fs.readFileSync(f, 'utf8').split('\n').filter(Boolean)) {
  const r = JSON.parse(l); n++;
  const c = S.check(r.doc, '');
  const wf = c.status !== 'malformed';
  if (r.wf) tot.wf++; if (r.valid) tot.valid++;
  if (wf !== r.wf) { wfMis++; mism.push({ k: 'wf', engine: c.status, oracle: r.wf, doc: r.doc.slice(0, 300), msg: c.issues[0] && c.issues[0].msg }); continue; }
  if (wf && c.schemaValid !== r.valid) mism.push({ k: 'valid', engine: c.schemaValid, oracle: r.valid, doc: r.doc.slice(0, 400), msg: (c.issues[0] || {}).msg });
}
console.log(JSON.stringify({ docs: n, wellFormedByOracle: tot.wf, schemaValidByOracle: tot.valid, wfMismatches: wfMis, mismatches: mism.length }));
mism.slice(0, +process.env.SHOW || 0).forEach(m => console.log(JSON.stringify(m)));
