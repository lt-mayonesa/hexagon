import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Documentation sidebar
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'getting-started/installation',
        'getting-started/quick-start',
        'getting-started/configuration',
      ],
    },
    {
      type: 'category',
      label: 'Tutorials',
      items: [
        'tutorial-extras/building-custom-tool',
        'tutorial-extras/multi-environment-workflow',
      ],
    },
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/creating-a-cli',
        'guides/tool-types',
        'guides/environments',
        'guides/theming',
        'guides/plugins',
        'guides/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Advanced',
      items: [
        'advanced/custom-tools',
        'advanced/prompting',
        'advanced/action-execution',
        'advanced/hooks',
        'advanced/internationalization',
      ],
    },
  ],

  // API Reference sidebar
  apiSidebar: [
    'api',
    {
      type: 'category',
      label: 'Configuration',
      items: [
        'api/cli',
        'api/tool',
        'api/env',
        'api/runtime-options',
      ],
    },
    {
      type: 'category',
      label: 'Built-in Features',
      items: [
        'api/built-in-tools',
      ],
    },
    {
      type: 'category',
      label: 'Actions',
      items: [
        'api/actions/web',
        'api/actions/shell',
      ],
    },
    {
      type: 'category',
      label: 'Support',
      items: [
        'api/support/output',
        'api/support/hooks',
        'api/support/storage',
      ],
    },
  ],
};

export default sidebars;
