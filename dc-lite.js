/* Мини-движок прототипа: шаблоны {{...}}, <sc-for>, <sc-if> и класс DCLogic — без внешних зависимостей. */
(function () {
  class DCLogic {
    constructor(props) { this.props = props || {}; this.state = null; }
    setState(patch) {
      const prev = this.state || {};
      const next = typeof patch === 'function' ? patch(prev) : patch;
      this.state = Object.assign({}, prev, next);
      render();
    }
  }
  window.DCLogic = DCLogic;

  const tpl = document.getElementById('dc-tpl');
  const root = document.getElementById('dc-root');
  const code = document.getElementById('dc-logic').textContent;
  const Component = new Function('DCLogic', code + '\n;return Component;')(DCLogic);
  const inst = new Component({});

  const RE = /\{\{([^}]+)\}\}/g;
  function get(scopes, path) {
    path = (path || '').trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    const parts = path.split('.');
    for (const s of scopes) {
      if (s && typeof s === 'object' && parts[0] in s) {
        let v = s;
        for (const p of parts) { if (v == null) return undefined; v = v[p]; }
        return v;
      }
    }
    return undefined;
  }
  function exact(str) { const m = (str || '').match(/^\s*\{\{([^}]+)\}\}\s*$/); return m ? m[1] : null; }
  function interp(str, scopes) { return str.replace(RE, (m, p) => { const v = get(scopes, p); return v == null ? '' : String(v); }); }

  function build(node, scopes, out) {
    for (const ch of Array.from(node.childNodes)) {
      if (ch.nodeType === 3) { out.appendChild(document.createTextNode(interp(ch.nodeValue, scopes))); continue; }
      if (ch.nodeType !== 1) continue;
      const tag = ch.tagName.toLowerCase();
      if (tag === 'sc-for') {
        const list = get(scopes, exact(ch.getAttribute('list'))) || [];
        const as = ch.getAttribute('as') || 'item';
        list.forEach((it, i) => build(ch, [{ [as]: it, index: i }].concat(scopes), out));
        continue;
      }
      if (tag === 'sc-if') {
        if (get(scopes, exact(ch.getAttribute('value')))) build(ch, scopes, out);
        continue;
      }
      const el = document.importNode(ch, false);
      for (const attr of Array.from(el.attributes)) {
        const name = attr.name, val = attr.value;
        if (name.startsWith('hint-')) { el.removeAttribute(name); continue; }
        if (name.startsWith('on')) {
          el.removeAttribute(name);
          const fn = get(scopes, exact(val));
          if (typeof fn === 'function') {
            let evt = name.slice(2);
            const isText = (el.tagName === 'INPUT' && !/^(checkbox|radio)$/i.test(el.type)) || el.tagName === 'TEXTAREA';
            if (evt === 'change' && isText) evt = 'input';
            el.addEventListener(evt, (e) => fn(e));
          }
          continue;
        }
        if (val.indexOf('{{') === -1) continue;
        const k = exact(val);
        if (k && name === 'checked') { el.removeAttribute('checked'); el.checked = !!get(scopes, k); continue; }
        if (k && name === 'value') { const v = get(scopes, k); el.setAttribute('value', v == null ? '' : v); el.value = v == null ? '' : v; continue; }
        el.setAttribute(name, interp(val, scopes));
      }
      build(ch.content || ch, scopes, el);
      out.appendChild(el);
    }
  }

  function render() {
    const vals = inst.renderVals ? inst.renderVals() : {};
    const ae = document.activeElement;
    const focusId = ae && ae.id;
    const sel = ae && typeof ae.selectionStart === 'number' ? [ae.selectionStart, ae.selectionEnd] : null;
    const a11y = document.getElementById('a11y');
    const a11yOn = !!(a11y && a11y.checked);
    const openDetails = Array.from(root.querySelectorAll('details')).map((d) => d.open);
    const frag = document.createDocumentFragment();
    build(tpl.content, [vals], frag);
    root.replaceChildren(frag);
    const a2 = document.getElementById('a11y'); if (a2) a2.checked = a11yOn;
    if (openDetails.length) root.querySelectorAll('details').forEach((d, i) => { if (i < openDetails.length) d.open = openDetails[i]; });
    if (focusId) {
      const n = document.getElementById(focusId);
      if (n) { n.focus({ preventScroll: true }); if (sel && n.setSelectionRange) { try { n.setSelectionRange(sel[0], sel[1]); } catch (e) {} } }
    }
  }
  render();
})();
