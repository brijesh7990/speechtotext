import React from 'react';
import styles from './Loader.module.css'; // Import the CSS module

const Loader: React.FC = () => {
  return (
    <div className={styles.loader}>
      <div className={styles.loadingText}>
        Loading<span className={styles.dot}>.</span>
        <span className={styles.dot}>.</span>
        <span className={styles.dot}>.</span>
      </div>
      <div className={styles.loadingBarBackground}>
        <div className={styles.loadingBar}>
          <div className={styles.whiteBarsContainer}>
            {Array.from({ length: 10 }, (_, index) => (
              <div key={index} className={styles.whiteBar}></div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Loader;
