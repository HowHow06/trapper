import { defineManifest } from '@crxjs/vite-plugin'

export default defineManifest({
  name: 'Trapper Client',
  description:
    'A chrome extension for scanning XSS vulnerability, as a client for the trapper project.',
  version: '0.1.1',
  manifest_version: 3,
  icons: {
    16: 'img/logo-16.png',
    32: 'img/logo-32.png',
    48: 'img/logo-48.png',
    128: 'img/logo-128.png',
  },
  action: {
    default_popup: 'popup.html',
    default_icon: 'img/logo-48.png',
  },
  options_page: 'options.html',
  background: {
    service_worker: 'src/background/index.js',
    type: 'module',
  },
  content_scripts: [
    {
      matches: ['http://*/*', 'https://*/*'],
      js: ['src/content/index.js'], // can change to jsx when needed
    },
  ],
  web_accessible_resources: [
    {
      resources: ['img/logo-16.png', 'img/logo-32.png', 'img/logo-48.png', 'img/logo-128.png'],
      matches: [],
    },
  ],
  permissions: [],
  // host_permissions: ["http://localhost:3000/", "http://localhost:8000/"], // uncomment this if extension fail to send HTTP-only cookie along with the api calls
})
