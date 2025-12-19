# Quickstart: Docusaurus Textbook Development

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager
- Git for version control

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Navigate to the website directory:
   ```bash
   cd website
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

## Development

1. Start the development server:
   ```bash
   npm start
   ```

   This will start a local development server and open your site in a browser at `http://localhost:3000`.

2. Edit content in the `docs/` directory to update textbook content.

3. The site will automatically reload when you make changes.

## Build

To build the static site for production:

```bash
npm run build
```

The built site will be in the `build/` directory and can be deployed to any static hosting service.

## Adding New Content

1. Create new markdown files in the `docs/` directory
2. Add proper frontmatter to your content:
   ```markdown
   ---
   sidebar_label: 'Your Content Title'
   sidebar_position: 10  # Position in sidebar
   ---
   ```

3. Update `sidebars.js` to include your new content in the navigation

## Custom Components

The textbook includes custom components like the LearningObjectives component:

```markdown
import LearningObjectives from '@site/src/components/LearningObjectives';

<LearningObjectives objectives={[
  'First learning objective',
  'Second learning objective'
]} />
```

## Theming

Custom styles are in `src/css/custom.css`. The theme uses a color scheme appropriate for educational content with good readability.

## Deployment

The site can be deployed to GitHub Pages, Netlify, Vercel, or any static hosting service.

For GitHub Pages deployment, run:
```bash
GIT_USER=<Your GitHub username> npm run deploy
```