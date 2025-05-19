import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Simple Configuration',
    Svg: require('@site/static/img/hexagon_simple_config.svg').default,
    description: (
      <>
        Define your CLI using simple YAML files. No complex coding required - just
        describe your tools, environments, and actions.
      </>
    ),
  },
  {
    title: 'Multiple Tool Types',
    Svg: require('@site/static/img/hexagon_tool_types.svg').default,
    description: (
      <>
        Create various tool types including web links, shell commands, and custom functions.
        Organize tools into logical groups for better usability.
      </>
    ),
  },
  {
    title: 'Environment Support',
    Svg: require('@site/static/img/hexagon_environments.svg').default,
    description: (
      <>
        Configure different environments (dev, qa, prod) with environment-specific
        settings for each tool. Switch between environments with a simple flag.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
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
