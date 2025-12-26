// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'about-textbook',
      label: 'About This Textbook'
    },
    {
      type: 'category',
      label: 'Introduction',
      items: ['intro'],
      link: {
        type: 'doc',
        id: 'intro',
      }
    },
    {
      type: 'category',
      label: 'Chapter 1: Foundations',
      items: [
        'chapter-1/index',
        'chapter-1/section-1',
        'chapter-1/section-2',
        'chapter-1/section-3'
      ],
      link: {
        type: 'doc',
        id: 'chapter-1/index',
      }
    },
    {
      type: 'category',
      label: 'Chapter 2: Core Concepts',
      items: [
        'chapter-2/index',
        'chapter-2/section-1'
      ],
      link: {
        type: 'doc',
        id: 'chapter-2/index',
      }
    },
    {
      type: 'category',
      label: 'Chapter 3: Locomotion and Movement',
      items: [
        'chapter-3/index',
        'chapter-3/section-1'
      ],
      link: {
        type: 'doc',
        id: 'chapter-3/index',
      }
    },
    {
      type: 'category',
      label: 'Resources',
      items: [
        'glossary',
        'references',
        'exercises'
      ]
    }
    // Additional chapters will be added as they are created
  ],
};

module.exports = sidebars;