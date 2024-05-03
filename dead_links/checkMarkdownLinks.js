const fs = require('fs');
const path = require('path');
const markdownLinkCheck = require('markdown-link-check');

const directoryPath = '/path/to/directory';

fs.readdir(directoryPath, (err, files) => {
  if (err) {
    console.error('Error reading directory:', err);
    return;
  }

  files.forEach(file => {
    if (path.extname(file) === '.md') {
      const filePath = path.join(directoryPath, file);
      console.log('Checking links in:', filePath);
      fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
          console.error('Error reading file:', err);
          return;
        }
        markdownLinkCheck(data, (err, results) => {
          if (err) {
            console.error('Error checking links:', err);
            return;
          }
          results.forEach(result => {
            if (result.status !== 'alive') {
              console.log(`Broken link found in ${filePath}:`);
              console.log(`  Link: ${result.link}`);
              console.log(`  Error: ${result.error}`);
            }
          });
        });
      });
    }
  });
});
