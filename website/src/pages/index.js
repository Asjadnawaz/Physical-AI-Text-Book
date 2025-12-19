import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Read the Textbook 📚
          </Link>
          <Link
            className="button button--primary button--lg"
            to="/docs/chapter-1">
            Start Learning →
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive online textbook on Physical AI & Humanoid Robotics">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h3>Physical AI Foundations</h3>
                  <p>Explore the fundamental principles of Physical AI and embodied cognition that form the basis of intelligent physical systems.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h3>Humanoid Robotics</h3>
                  <p>Discover the cutting-edge research and engineering principles behind humanoid robot design and control.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <h3>Advanced Locomotion</h3>
                  <p>Master the complex algorithms and control systems that enable dynamic movement and balance in physical agents.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.about}>
          <div className="container padding-vert--lg">
            <div className="row">
              <div className="col col--12">
                <div className="text--center">
                  <h2>About This Textbook</h2>
                  <p>
                    This comprehensive textbook provides a thorough introduction to Physical AI and Humanoid Robotics,
                    combining theoretical foundations with practical applications. Designed for students, researchers,
                    and practitioners in robotics and artificial intelligence.
                  </p>

                  <div className="margin-vert--lg">
                    <Link
                      className="button button--outline button--secondary button--lg"
                      to="/docs/about-textbook">
                      About the Textbook Structure
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.cta}>
          <div className="container padding-vert--lg">
            <div className="row">
              <div className="col col--12">
                <div className="text--center">
                  <h2>Ready to Dive In?</h2>
                  <p>
                    Start your journey into the fascinating world of Physical AI and Humanoid Robotics.
                    Whether you're a beginner or an experienced practitioner, this textbook offers
                    insights and knowledge to advance your understanding.
                  </p>
                  <div className={styles.buttons}>
                    <Link
                      className="button button--primary button--lg margin-horiz--sm"
                      to="/docs/intro">
                      Begin Reading
                    </Link>
                    <Link
                      className="button button--secondary button--lg margin-horiz--sm"
                      to="/docs/chapter-1/section-1">
                      Jump to Chapter 1
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}