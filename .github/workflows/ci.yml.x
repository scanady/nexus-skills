name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  validate-and-build:
    name: Validate skills, rebuild catalog, build plugins + site
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Validate skills
        run: node bin/validate-skills.js

      - name: Scan skills
        run: python bin/scan-skills.py skills -o skill-catalog-scan.json

      - name: Rebuild catalog
        run: python bin/rebuild-catalog.py

      - name: Detect catalog drift
        if: github.event_name == 'pull_request'
        run: |
          if ! git diff --quiet -- skill-catalog.json skill-catalog-scan.json; then
            echo "::warning::Catalog files differ from committed copy. Run 'npm run scan && npm run catalog' locally and commit the result."
            git diff --stat -- skill-catalog.json skill-catalog-scan.json
          fi

      - name: Build Claude plugins
        run: node bin/build-plugins.js

      - name: Detect plugin manifest drift
        if: github.event_name == 'pull_request'
        run: |
          if ! git diff --quiet -- .claude-plugin/marketplace.json .claude-plugin/plugin.json; then
            echo "::warning::Plugin manifests differ from committed copy. Run 'npm run build:plugins' locally and commit the result."
            git diff --stat -- .claude-plugin/marketplace.json .claude-plugin/plugin.json
          fi

      - name: Build Pages site
        run: node bin/build-site.js

      - name: Upload site artifact
        uses: actions/upload-artifact@v4
        with:
          name: site-${{ github.sha }}
          path: dist/site/
          retention-days: 14

      - name: Upload plugin bundles
        uses: actions/upload-artifact@v4
        with:
          name: plugins-${{ github.sha }}
          path: dist/plugins/
          retention-days: 14
