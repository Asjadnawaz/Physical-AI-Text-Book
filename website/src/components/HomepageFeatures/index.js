import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Comprehensive Coverage',
    description: (
      <>
        Complete coverage of Physical AI and Humanoid Robotics from fundamentals to advanced topics.
      </>
    ),
  },
  {
    title: 'Interactive Learning',
    description: (
      <>
        Engaging content with practical examples, exercises, and real-world applications.
      </>
    ),
  },
  {
    title: ' cutting-edge Research',
    description: (
      <>
        Up-to-date information on the latest developments in robotics and AI research.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}