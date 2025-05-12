# CHANGELOG


## v0.63.1 (2025-05-12)

### Bug Fixes

- **release**: Use correct publish tool
  ([`1925fa5`](https://github.com/lt-mayonesa/hexagon/commit/1925fa5e0f3810e7c3b582f405487fcd18828caa))

### Chores

- **e2e**: Reordered group tools to fix flaky test
  ([#154](https://github.com/lt-mayonesa/hexagon/pull/154),
  [`9e5e343`](https://github.com/lt-mayonesa/hexagon/commit/9e5e343390fe2dcfdc117bd2c32611fb46f363c6))

ci logs where complaining about initial branch name being master


## v0.63.0 (2025-05-11)

### Chores

- **e2e**: Minor code improvements ([#151](https://github.com/lt-mayonesa/hexagon/pull/151),
  [`ebf4f87`](https://github.com/lt-mayonesa/hexagon/commit/ebf4f87213cddc665deef16e5dc1a6e988432659))

- **tests**: Run e2e tests in parallel ([#90](https://github.com/lt-mayonesa/hexagon/pull/90),
  [`5392dbe`](https://github.com/lt-mayonesa/hexagon/commit/5392dbed2ebd0130814def162c61abcbe2699635))

### Features

- **cwd-tools**: Load tools defined in hexagon_tools yaml
  ([#152](https://github.com/lt-mayonesa/hexagon/pull/152),
  [`93fd728`](https://github.com/lt-mayonesa/hexagon/commit/93fd72878761bf01d4761ca7dc476400e39dfe1f))

added support for loading extra tools if a file named hexagon_tools.yml exists in the current
  working directory.

### Refactoring

- **prompt**: Use Separator tool ([#153](https://github.com/lt-mayonesa/hexagon/pull/153),
  [`faf0cd0`](https://github.com/lt-mayonesa/hexagon/commit/faf0cd05baac2eaba392c46aadb8b5fda2c03ef9))


## v0.62.2 (2025-05-09)

### Bug Fixes

- **errors**: Show traceback on group tools
  ([#150](https://github.com/lt-mayonesa/hexagon/pull/150),
  [`47cae1a`](https://github.com/lt-mayonesa/hexagon/commit/47cae1ab73818d36333bd8f2ce9141da78fae6b4))

### Chores

- **deps**: Bump markdown from 3.7 to 3.8 ([#149](https://github.com/lt-mayonesa/hexagon/pull/149),
  [`2f07726`](https://github.com/lt-mayonesa/hexagon/commit/2f07726e8008c3e4b555e4c94ac7649e03f32bd6))

Bumps [markdown](https://github.com/Python-Markdown/markdown) from 3.7 to 3.8. - [Release
  notes](https://github.com/Python-Markdown/markdown/releases) -
  [Changelog](https://github.com/Python-Markdown/markdown/blob/master/docs/changelog.md) -
  [Commits](https://github.com/Python-Markdown/markdown/compare/3.7...3.8)

--- updated-dependencies: - dependency-name: markdown dependency-version: '3.8'

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump black from 24.10.0 to 25.1.0
  ([#148](https://github.com/lt-mayonesa/hexagon/pull/148),
  [`f164e25`](https://github.com/lt-mayonesa/hexagon/commit/f164e259832b9b5fdabba0c467692131886715ff))

Bumps [black](https://github.com/psf/black) from 24.10.0 to 25.1.0. - [Release
  notes](https://github.com/psf/black/releases) -
  [Changelog](https://github.com/psf/black/blob/main/CHANGES.md) -
  [Commits](https://github.com/psf/black/compare/24.10.0...25.1.0)

--- updated-dependencies: - dependency-name: black dependency-version: 25.1.0

dependency-type: direct:development

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **format**: Apply new black version
  ([`92bc198`](https://github.com/lt-mayonesa/hexagon/commit/92bc1985a14a38dca8c87661f0d3322fbecc1d95))

### Continuous Integration

- **release**: Rollback to user token
  ([`55dd61e`](https://github.com/lt-mayonesa/hexagon/commit/55dd61ef043562f3f860fc2db224a85ef79301ce))

- **release**: Setup correct permission on jobs
  ([`587f7a9`](https://github.com/lt-mayonesa/hexagon/commit/587f7a95cc3ac0cf90c126a21f9739abc0b90a07))

- **release**: Use github token on release
  ([`bd6220d`](https://github.com/lt-mayonesa/hexagon/commit/bd6220d20fa9fdb9f4aff1e0ddd1e78dc35e2475))


## v0.62.1 (2025-05-06)

### Bug Fixes

- **parse**: Changelog on update ([#145](https://github.com/lt-mayonesa/hexagon/pull/145),
  [`d582ae4`](https://github.com/lt-mayonesa/hexagon/commit/d582ae41d69b0d3d3f5506a365935346dbd4d3ef))

kiss

### Chores

- **ci**: Use github token on release
  ([`4762efb`](https://github.com/lt-mayonesa/hexagon/commit/4762efb366cc144918f662ff9512da0cc5a3d87c))

- **deps**: Bump dorny/test-reporter from 1 to 2
  ([#143](https://github.com/lt-mayonesa/hexagon/pull/143),
  [`9571364`](https://github.com/lt-mayonesa/hexagon/commit/9571364216ab1c12fa02e6acc8905bf63c0ef1d2))

Bumps [dorny/test-reporter](https://github.com/dorny/test-reporter) from 1 to 2. - [Release
  notes](https://github.com/dorny/test-reporter/releases) -
  [Changelog](https://github.com/dorny/test-reporter/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/dorny/test-reporter/compare/v1...v2)

--- updated-dependencies: - dependency-name: dorny/test-reporter dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump packaging from 24.1 to 24.2
  ([#122](https://github.com/lt-mayonesa/hexagon/pull/122),
  [`1913e4c`](https://github.com/lt-mayonesa/hexagon/commit/1913e4cb72726dd0a7841f6ba6cb0fbac72a1c89))

Bumps [packaging](https://github.com/pypa/packaging) from 24.1 to 24.2. - [Release
  notes](https://github.com/pypa/packaging/releases) -
  [Changelog](https://github.com/pypa/packaging/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pypa/packaging/compare/24.1...24.2)

--- updated-dependencies: - dependency-name: packaging dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic from 2.8.2 to 2.9.2
  ([#104](https://github.com/lt-mayonesa/hexagon/pull/104),
  [`12b6411`](https://github.com/lt-mayonesa/hexagon/commit/12b64114c3ca92fbee0155c2918db1c33ab5e3da))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.8.2 to 2.9.2. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/main/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.8.2...v2.9.2)

--- updated-dependencies: - dependency-name: pydantic dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic-settings from 2.4.0 to 2.5.2
  ([#102](https://github.com/lt-mayonesa/hexagon/pull/102),
  [`15cf47c`](https://github.com/lt-mayonesa/hexagon/commit/15cf47cf8344b254c7d9b719d571d7fd458a0aab))

Bumps [pydantic-settings](https://github.com/pydantic/pydantic-settings) from 2.4.0 to 2.5.2. -
  [Release notes](https://github.com/pydantic/pydantic-settings/releases) -
  [Commits](https://github.com/pydantic/pydantic-settings/compare/v2.4.0...v2.5.2)

--- updated-dependencies: - dependency-name: pydantic-settings dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump pydantic-settings from 2.5.2 to 2.8.1
  ([#141](https://github.com/lt-mayonesa/hexagon/pull/141),
  [`2731eb7`](https://github.com/lt-mayonesa/hexagon/commit/2731eb73bf206d630dfc63403d60bda24659b867))

Bumps [pydantic-settings](https://github.com/pydantic/pydantic-settings) from 2.5.2 to 2.8.1. -
  [Release notes](https://github.com/pydantic/pydantic-settings/releases) -
  [Commits](https://github.com/pydantic/pydantic-settings/compare/v2.5.2...v2.8.1)

--- updated-dependencies: - dependency-name: pydantic-settings dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump python-semantic-release/python-semantic-release
  ([#139](https://github.com/lt-mayonesa/hexagon/pull/139),
  [`3d5f880`](https://github.com/lt-mayonesa/hexagon/commit/3d5f8804e2a1ed9ae51892942fefff12aa24fe13))

Bumps
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.8.8 to 9.21.0. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.rst)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.8.8...v9.21.0)

--- updated-dependencies: - dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump rich from 13.7.1 to 13.8.1
  ([#100](https://github.com/lt-mayonesa/hexagon/pull/100),
  [`62a13ad`](https://github.com/lt-mayonesa/hexagon/commit/62a13ad0aa1db85e9c59ac9891b38c1b87e4006b))

Bumps [rich](https://github.com/Textualize/rich) from 13.7.1 to 13.8.1. - [Release
  notes](https://github.com/Textualize/rich/releases) -
  [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/Textualize/rich/compare/v13.7.1...v13.8.1)

--- updated-dependencies: - dependency-name: rich dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump rich from 13.8.1 to 14.0.0
  ([#144](https://github.com/lt-mayonesa/hexagon/pull/144),
  [`2973b6c`](https://github.com/lt-mayonesa/hexagon/commit/2973b6cb5eb5c2f6b06dff202d7c542563b9a16a))

Bumps [rich](https://github.com/Textualize/rich) from 13.8.1 to 14.0.0. - [Release
  notes](https://github.com/Textualize/rich/releases) -
  [Changelog](https://github.com/Textualize/rich/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/Textualize/rich/compare/v13.8.1...v14.0.0)

--- updated-dependencies: - dependency-name: rich dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump TrueBrain/actions-flake8 from 2.1 to 2.3
  ([#94](https://github.com/lt-mayonesa/hexagon/pull/94),
  [`3321c46`](https://github.com/lt-mayonesa/hexagon/commit/3321c463df9a528739f3a2134a97ec9998cdf19e))

Bumps [TrueBrain/actions-flake8](https://github.com/truebrain/actions-flake8) from 2.1 to 2.3. -
  [Release notes](https://github.com/truebrain/actions-flake8/releases) -
  [Commits](https://github.com/truebrain/actions-flake8/compare/v2.1...v2.3)

--- updated-dependencies: - dependency-name: TrueBrain/actions-flake8 dependency-type:
  direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump TrueBrain/actions-flake8 from 2.3 to 2.4
  ([#113](https://github.com/lt-mayonesa/hexagon/pull/113),
  [`6520f2e`](https://github.com/lt-mayonesa/hexagon/commit/6520f2e3bdfa5e9b66075069c1cebfa75d293746))

Bumps [TrueBrain/actions-flake8](https://github.com/truebrain/actions-flake8) from 2.3 to 2.4. -
  [Release notes](https://github.com/truebrain/actions-flake8/releases) -
  [Commits](https://github.com/truebrain/actions-flake8/compare/v2.3...v2.4)

--- updated-dependencies: - dependency-name: TrueBrain/actions-flake8 dependency-type:
  direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump black from 24.8.0 to 24.10.0
  ([#109](https://github.com/lt-mayonesa/hexagon/pull/109),
  [`9000f9a`](https://github.com/lt-mayonesa/hexagon/commit/9000f9a480ebaa786751d4b186ee83878eb61b96))

Bumps [black](https://github.com/psf/black) from 24.8.0 to 24.10.0. - [Release
  notes](https://github.com/psf/black/releases) -
  [Changelog](https://github.com/psf/black/blob/main/CHANGES.md) -
  [Commits](https://github.com/psf/black/compare/24.8.0...24.10.0)

--- updated-dependencies: - dependency-name: black dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump flake8-bugbear from 24.4.26 to 24.12.12
  ([#127](https://github.com/lt-mayonesa/hexagon/pull/127),
  [`d6a9322`](https://github.com/lt-mayonesa/hexagon/commit/d6a93221f29d7ff9d2debc6426c6fb44ac1e0e33))

Bumps [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear) from 24.4.26 to 24.12.12. - [Release
  notes](https://github.com/PyCQA/flake8-bugbear/releases) -
  [Commits](https://github.com/PyCQA/flake8-bugbear/compare/24.4.26...24.12.12)

--- updated-dependencies: - dependency-name: flake8-bugbear dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.3.3 to 8.3.5
  ([#142](https://github.com/lt-mayonesa/hexagon/pull/142),
  [`a51c206`](https://github.com/lt-mayonesa/hexagon/commit/a51c20642d2222f1094da7198cc44a9cd103a764))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.3 to 8.3.5. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.3...8.3.5)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Continuous Integration

- **deps**: Migrate to artifact@v4 ([#105](https://github.com/lt-mayonesa/hexagon/pull/105),
  [`09176a7`](https://github.com/lt-mayonesa/hexagon/commit/09176a70663f8ace75d9f027dc8d2b8c1ef9864b))

- **release**: Remove listing dirs
  ([`6cbf706`](https://github.com/lt-mayonesa/hexagon/commit/6cbf706b7620b9b986d249904b30c95e851caec1))


## v0.62.0 (2024-09-21)

### Chores

- **deps**: Bump python-semantic-release/python-semantic-release
  ([#96](https://github.com/lt-mayonesa/hexagon/pull/96),
  [`c02e9d2`](https://github.com/lt-mayonesa/hexagon/commit/c02e9d2fd8ffe20823b0a7a09cc68e976283dfb0))

Bumps
  [python-semantic-release/python-semantic-release](https://github.com/python-semantic-release/python-semantic-release)
  from 9.8.6 to 9.8.8. - [Release
  notes](https://github.com/python-semantic-release/python-semantic-release/releases) -
  [Changelog](https://github.com/python-semantic-release/python-semantic-release/blob/master/CHANGELOG.md)
  -
  [Commits](https://github.com/python-semantic-release/python-semantic-release/compare/v9.8.6...v9.8.8)

--- updated-dependencies: - dependency-name: python-semantic-release/python-semantic-release
  dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps-dev**: Bump pytest from 8.3.2 to 8.3.3
  ([#103](https://github.com/lt-mayonesa/hexagon/pull/103),
  [`3723433`](https://github.com/lt-mayonesa/hexagon/commit/37234338eac1ddd6f76472c634337a73d372fda6))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 8.3.2 to 8.3.3. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/8.3.2...8.3.3)

--- updated-dependencies: - dependency-name: pytest dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

### Continuous Integration

- **dependabot**: Set to run daily
  ([`4eb3206`](https://github.com/lt-mayonesa/hexagon/commit/4eb3206bb85458b7679f654ee0bd0a37845c51e0))

- **release**: Install setuptools before release
  ([`0255451`](https://github.com/lt-mayonesa/hexagon/commit/02554518c25d0fe38df195ed42cdec3bca00b927))

- **release**: Install setuptools before release
  ([`791127c`](https://github.com/lt-mayonesa/hexagon/commit/791127cda44c12baee0da81f073270c85396c4bd))

- **release**: Install wheel before release
  ([`bf528ad`](https://github.com/lt-mayonesa/hexagon/commit/bf528ad17b8510ac9d93fdd5a99f0648af5cac16))

### Features

- **updates**: Use pip to upgrade hexagon ([#92](https://github.com/lt-mayonesa/hexagon/pull/92),
  [`f7e6544`](https://github.com/lt-mayonesa/hexagon/commit/f7e65447e1cc0ba917212be92badfcf69132c778))


## v0.61.0 (2024-08-20)

### Chores

- **ci**: Publish to PyPi
  ([`38b1a2d`](https://github.com/lt-mayonesa/hexagon/commit/38b1a2d75d7423a46a00ac02c50ff265931f3225))

- **deps**: Bump actions/checkout from 3 to 4
  ([#85](https://github.com/lt-mayonesa/hexagon/pull/85),
  [`fa14690`](https://github.com/lt-mayonesa/hexagon/commit/fa146902d735bddce404636871dcd33ee78abf2b))

Bumps [actions/checkout](https://github.com/actions/checkout) from 3 to 4. - [Release
  notes](https://github.com/actions/checkout/releases) -
  [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/actions/checkout/compare/v3...v4)

--- updated-dependencies: - dependency-name: actions/checkout dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump actions/setup-python from 4 to 5
  ([#86](https://github.com/lt-mayonesa/hexagon/pull/86),
  [`1853b6d`](https://github.com/lt-mayonesa/hexagon/commit/1853b6dd4d27f4e84409d13919736b10fb5dac2c))

Bumps [actions/setup-python](https://github.com/actions/setup-python) from 4 to 5. - [Release
  notes](https://github.com/actions/setup-python/releases) -
  [Commits](https://github.com/actions/setup-python/compare/v4...v5)

--- updated-dependencies: - dependency-name: actions/setup-python dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump markdown from 3.6 to 3.7 ([#89](https://github.com/lt-mayonesa/hexagon/pull/89),
  [`d8b0f83`](https://github.com/lt-mayonesa/hexagon/commit/d8b0f830e06de6392027207c276c0d5aaf08ea22))

Bumps [markdown](https://github.com/Python-Markdown/markdown) from 3.6 to 3.7. - [Release
  notes](https://github.com/Python-Markdown/markdown/releases) -
  [Changelog](https://github.com/Python-Markdown/markdown/blob/master/docs/changelog.md) -
  [Commits](https://github.com/Python-Markdown/markdown/compare/3.6...3.7)

--- updated-dependencies: - dependency-name: markdown dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **deps**: Bump nick-fields/retry from 2 to 3
  ([#84](https://github.com/lt-mayonesa/hexagon/pull/84),
  [`dd245aa`](https://github.com/lt-mayonesa/hexagon/commit/dd245aac8a0a5285cf8ef99a5035a4ccfa85ac5b))

Bumps [nick-fields/retry](https://github.com/nick-fields/retry) from 2 to 3. - [Release
  notes](https://github.com/nick-fields/retry/releases) -
  [Changelog](https://github.com/nick-fields/retry/blob/master/.releaserc.js) -
  [Commits](https://github.com/nick-fields/retry/compare/v2...v3)

--- updated-dependencies: - dependency-name: nick-fields/retry dependency-type: direct:production

update-type: version-update:semver-major ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **release**: Configure semantic release v9
  ([`6c95617`](https://github.com/lt-mayonesa/hexagon/commit/6c95617a795b811e5cd066ba5377c49ed1f0c40a))

- **release**: Specify build command
  ([`0dbbf67`](https://github.com/lt-mayonesa/hexagon/commit/0dbbf6776b1cde6cec7e5f31456f6ff22b78f225))

### Features

- Print hexagon package version ([#91](https://github.com/lt-mayonesa/hexagon/pull/91),
  [`b52bfe2`](https://github.com/lt-mayonesa/hexagon/commit/b52bfe2fffc15dcb24ff6ec0064ab43f925ed45c))


## v0.60.0 (2024-08-09)

### Chores

- **deps**: Migrate to pydantic v2 ([#81](https://github.com/lt-mayonesa/hexagon/pull/81),
  [`56ec06e`](https://github.com/lt-mayonesa/hexagon/commit/56ec06e0a1ffcd94530504ddb98cec8598f93911))

- **deps**: Setup dependabot version upgrades
  ([`6c43a24`](https://github.com/lt-mayonesa/hexagon/commit/6c43a2491c79f67f3df09809b54406eb6ca2905b))

### Features

- **prompt**: Allow to provide text suggestions
  ([#88](https://github.com/lt-mayonesa/hexagon/pull/88),
  [`fb1319a`](https://github.com/lt-mayonesa/hexagon/commit/fb1319a7ab7e42acbf76776a8842923d86b17b3e))


## v0.59.0 (2024-04-09)

### Features

- **cli**: Allow configuring entrypoint on install
  ([`ed75377`](https://github.com/lt-mayonesa/hexagon/commit/ed7537743c6fdfe957a095d7ab51b7302df347ec))


## v0.58.1 (2024-04-08)

### Bug Fixes

- **install**: Make bin_path optional arg
  ([`741044a`](https://github.com/lt-mayonesa/hexagon/commit/741044a2244770c18b66dfd972bc1220cab910ad))

### Chores

- **ci**: Fix package step
  ([`5d51e29`](https://github.com/lt-mayonesa/hexagon/commit/5d51e29e017e6fbd493164162f48a8903165729f))


## v0.58.0 (2024-03-30)

### Chores

- **args**: Document .prompt public api
  ([`3c77688`](https://github.com/lt-mayonesa/hexagon/commit/3c7768875faea631d3069a812d2ab973dfbb4550))

- **args**: Fix flake8 errors
  ([`d2197e9`](https://github.com/lt-mayonesa/hexagon/commit/d2197e98204eccd6e6e91d86f9759ba6417d6f1a))

- **ci**: Publish release to pypi
  ([`45eb5fd`](https://github.com/lt-mayonesa/hexagon/commit/45eb5fd75193908478b184e07ced4012690e61f1))

- **deps-dev**: Bump black from 24.2.0 to 24.3.0
  ([#78](https://github.com/lt-mayonesa/hexagon/pull/78),
  [`32da740`](https://github.com/lt-mayonesa/hexagon/commit/32da74066a95a1bbf44787153f518cf81dcd2a3a))

Bumps [black](https://github.com/psf/black) from 24.2.0 to 24.3.0. - [Release
  notes](https://github.com/psf/black/releases) -
  [Changelog](https://github.com/psf/black/blob/main/CHANGES.md) -
  [Commits](https://github.com/psf/black/compare/24.2.0...24.3.0)

--- updated-dependencies: - dependency-name: black dependency-type: direct:development ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **dist**: Min python is 3.9 ([#79](https://github.com/lt-mayonesa/hexagon/pull/79),
  [`017ce49`](https://github.com/lt-mayonesa/hexagon/commit/017ce49c80947a4e2ee9162778ec99ad04253b03))

### Documentation

- **readme**: Install from pypi
  ([`6968d45`](https://github.com/lt-mayonesa/hexagon/commit/6968d45b54222086f940f9b635771214c0352bd5))

### Features

- **logger**: Add file & panel log APIs ([#80](https://github.com/lt-mayonesa/hexagon/pull/80),
  [`5e4a2db`](https://github.com/lt-mayonesa/hexagon/commit/5e4a2dbb9328d43a5921a51cc3b0ed42c6abbea6))

`log.example` & `log.file` take syntax highlighting args

`log.panel` lets users show a box panel

### Refactoring

- **args**: Split args into their own modules
  ([`2eb25b6`](https://github.com/lt-mayonesa/hexagon/commit/2eb25b658626d09f038c813b66713243e5ae38f9))


## v0.57.0 (2024-03-02)

### Chores

- **tests**: Check re-prompting assigns correctly
  ([`6946c72`](https://github.com/lt-mayonesa/hexagon/commit/6946c7208adc588e3919acd9aba844087739cc5a))

### Features

- **prompt**: Allow passing callable to skip_trace
  ([`608d5dd`](https://github.com/lt-mayonesa/hexagon/commit/608d5dd99ee059bdf11528a661b501e70d186a48))

fixes #76


## v0.56.0 (2024-02-19)

### Chores

- **deps**: Remove unused requests lib
  ([`55f114d`](https://github.com/lt-mayonesa/hexagon/commit/55f114d28ab626ebfb1179347b9ecd4f304a5376))

### Features

- **replay**: Allow replaying last command executed
  ([#75](https://github.com/lt-mayonesa/hexagon/pull/75),
  [`7449404`](https://github.com/lt-mayonesa/hexagon/commit/7449404463ae7287989240b447eede6094ccd6ef))

solves #72


## v0.55.0 (2024-02-18)

### Features

- **hexagon**: Added get-json-schema tool ([#73](https://github.com/lt-mayonesa/hexagon/pull/73),
  [`5377fbf`](https://github.com/lt-mayonesa/hexagon/commit/5377fbfaa1d4a82f16ae9d8a08cce740adb883b2))


## v0.54.0 (2024-02-18)

### Chores

- **cli**: Pipenv update command
  ([`17a0e09`](https://github.com/lt-mayonesa/hexagon/commit/17a0e0952069bfe3858b65f78f2edff20dc828fe))

- **deps**: Upgrade packages
  ([`67f5388`](https://github.com/lt-mayonesa/hexagon/commit/67f5388892674accc6cea15abec2b9f589983ad7))

- **i18n**: Check fuzzy strings
  ([`a315ffc`](https://github.com/lt-mayonesa/hexagon/commit/a315ffc1e67512f03fc77ee6162db3e34bc1b5a5))

- **i18n**: Support macos on build command
  ([`142d383`](https://github.com/lt-mayonesa/hexagon/commit/142d3835907308a847c068a1543f547e49976d7f))

### Features

- **prompt**: Allow specifying glob_extra_choices for file glop prompts
  ([#71](https://github.com/lt-mayonesa/hexagon/pull/71),
  [`d2fc570`](https://github.com/lt-mayonesa/hexagon/commit/d2fc570c5b4a4f660c0eeb40f9dc8da00eb01ad5))


## v0.53.2 (2023-11-13)

### Bug Fixes

- **i18n**: Validate existing paths
  ([`0b268e6`](https://github.com/lt-mayonesa/hexagon/commit/0b268e6a96e1886a1dd446b2f7fe483bdcc3adda))


## v0.53.1 (2023-11-12)

### Bug Fixes

- **help**: Don't print usage twice
  ([`603af0f`](https://github.com/lt-mayonesa/hexagon/commit/603af0fb1531bed4475b81c8d9175c1b53d4867e))

### Refactoring

- **help**: Hide help module function
  ([`7d11bd4`](https://github.com/lt-mayonesa/hexagon/commit/7d11bd4cec7a765ceac5cabe51cb416827feb823))


## v0.53.0 (2023-11-12)

### Features

- **args**: Allow passing boolean as key only
  ([#69](https://github.com/lt-mayonesa/hexagon/pull/69),
  [`2174082`](https://github.com/lt-mayonesa/hexagon/commit/2174082a4b2e0c5b210c6d2244d9eeea2775a31e))

for any boolean arg you can use keys: --[name] and --no-[name] (as well as aliases)


## v0.52.1 (2023-11-09)

### Bug Fixes

- **prompt**: Show correct confirm dialog
  ([`c36bbb1`](https://github.com/lt-mayonesa/hexagon/commit/c36bbb12b6a76ee14abc4989ea90c18ec1857a78))

- **tracer**: Lowercase traced bool
  ([`a19f109`](https://github.com/lt-mayonesa/hexagon/commit/a19f109e359623a6f8fe94315f1584dd03a63225))


## v0.52.0 (2023-11-06)

### Chores

- **flake8**: Remove unused imports
  ([`0bee930`](https://github.com/lt-mayonesa/hexagon/commit/0bee93089fd016f49fe17a919c79c5f27c63bb97))

- **prompt**: Prompt_on_access test
  ([`46f1295`](https://github.com/lt-mayonesa/hexagon/commit/46f12955084bbdfd9ae0f9c6bc6dfdd6689f7cba))

### Features

- **prompt**: Allow defining prompt_default ([#66](https://github.com/lt-mayonesa/hexagon/pull/66),
  [`8266843`](https://github.com/lt-mayonesa/hexagon/commit/8266843ecf9766de20435c1cbcac713026113195))


## v0.51.3 (2023-11-05)

### Bug Fixes

- **i18n**: Default to EN even if nothing found
  ([`685bdef`](https://github.com/lt-mayonesa/hexagon/commit/685bdefd14b159d39f2a5106e5d26723e4e867ed))

fixes: #64

### Chores

- **e2e**: Fix typehints for hexagonspec & better logs
  ([`5bc8309`](https://github.com/lt-mayonesa/hexagon/commit/5bc8309df5a53b0086b9b948ad452adc0b857491))

- **e2e**: Print dont wrap long lines
  ([`c68e187`](https://github.com/lt-mayonesa/hexagon/commit/c68e187b22036ea1be92d93ba64a71067a91e32c))

- **nightly**: Improve install message
  ([`35c4335`](https://github.com/lt-mayonesa/hexagon/commit/35c433528391594eaca97c6cb9982f4e95f326f7))


## v0.51.2 (2023-10-30)

### Bug Fixes

- **tracer**: Trace enum values correctly ([#63](https://github.com/lt-mayonesa/hexagon/pull/63),
  [`38475bb`](https://github.com/lt-mayonesa/hexagon/commit/38475bbb50bf252285e6c62eaab2768c15e974da))

* fix(tracer): trace enum values correctly


## v0.51.1 (2023-10-29)

### Bug Fixes

- **tracer**: Execute again display enum correctly
  ([`50d575a`](https://github.com/lt-mayonesa/hexagon/commit/50d575aed1d10516fc531e0f4946ab2655086e5c))


## v0.51.0 (2023-10-29)

### Chores

- **prompt**: Pass extra model fields to validator
  ([`09d69a4`](https://github.com/lt-mayonesa/hexagon/commit/09d69a4ff7e04238fa649e0cab0e6964e6dc630b))

### Features

- **prompt**: Ctrl+p create directory if not exists
  ([#61](https://github.com/lt-mayonesa/hexagon/pull/61),
  [`05002ac`](https://github.com/lt-mayonesa/hexagon/commit/05002ac13c5f492004a8edc99d4a69df965c3ab5))

hexagon types FilePath and DirectoryPath allow to specify nonexistent paths

fixes #30

### Refactoring

- **prompt**: Renames and type hints
  ([`2ef07bf`](https://github.com/lt-mayonesa/hexagon/commit/2ef07bfee431e034188f1df0fea63bcf35f1463c))


## v0.50.0 (2023-10-28)

### Chores

- **deps**: Bump urllib3 from 2.0.5 to 2.0.7 ([#58](https://github.com/lt-mayonesa/hexagon/pull/58),
  [`547da63`](https://github.com/lt-mayonesa/hexagon/commit/547da6332e6ae28d4d5a2a378bcd2af923922f96))

Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.5 to 2.0.7. - [Release
  notes](https://github.com/urllib3/urllib3/releases) -
  [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) -
  [Commits](https://github.com/urllib3/urllib3/compare/v2.0.5...2.0.7)

--- updated-dependencies: - dependency-name: urllib3 dependency-type: indirect ...

Signed-off-by: dependabot[bot] <support@github.com>

Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>

- **e2e**: Hexagon spec hints
  ([`8c4c53a`](https://github.com/lt-mayonesa/hexagon/commit/8c4c53aa4f015ff921adcebe02a644ba50e77c43))

### Features

- **execute**: Arg replacement
  ([`f459405`](https://github.com/lt-mayonesa/hexagon/commit/f459405d306847167b91d8f3257882d43de3a854))

### Refactoring

- Simplify decorators definition
  ([`81b8706`](https://github.com/lt-mayonesa/hexagon/commit/81b8706f92cb05074088fbe214ea9a38bd40e833))


## v0.49.2 (2023-09-27)

### Bug Fixes

- **prompt**: Handle enum default when searchable
  ([#56](https://github.com/lt-mayonesa/hexagon/pull/56),
  [`12e9987`](https://github.com/lt-mayonesa/hexagon/commit/12e9987739c74f2032d5e4251f49debf6d9cdcaf))

### Chores

- **deps**: Update python packages ([#54](https://github.com/lt-mayonesa/hexagon/pull/54),
  [`c66c876`](https://github.com/lt-mayonesa/hexagon/commit/c66c8765e3c00c17dc9a66af1eba16eed78fdd1e))

pydantic 2 not yet supported


## v0.49.1 (2023-09-24)

### Bug Fixes

- **execute**: Handle script relative paths correctly
  ([`9399df5`](https://github.com/lt-mayonesa/hexagon/commit/9399df5070716d0b7642b915b82016a30c95d78a))

- **execute**: Pass first arg to script when env not present
  ([`6cbf4c0`](https://github.com/lt-mayonesa/hexagon/commit/6cbf4c09c69b4b9894dd1ccbb979c54e11b822ca))


## v0.49.0 (2023-09-20)

### Features

- **plugins**: Allow to register plugins from multiple sources
  ([#52](https://github.com/lt-mayonesa/hexagon/pull/52),
  [`2c42112`](https://github.com/lt-mayonesa/hexagon/commit/2c42112cb8df4aa9d3a7436439b6375179f5a777))

changed `plugins_dir` (str) to `plugins` (list[str])

solves #45


## v0.48.4 (2023-09-20)

### Bug Fixes

- **i18n**: Add messages for number & secret hints
  ([#51](https://github.com/lt-mayonesa/hexagon/pull/51),
  [`220fe6c`](https://github.com/lt-mayonesa/hexagon/commit/220fe6ce6142bb68914ea28a0edd4e704b535260))


## v0.48.3 (2023-09-18)

### Bug Fixes

- **hooks**: Terminate background hooks ([#50](https://github.com/lt-mayonesa/hexagon/pull/50),
  [`f7f762f`](https://github.com/lt-mayonesa/hexagon/commit/f7f762f4558b5633d348d2a370a8f2941e8e4dde))


## v0.48.2 (2023-09-13)

### Bug Fixes

- **tracer**: Store Enum value ([#49](https://github.com/lt-mayonesa/hexagon/pull/49),
  [`2b283d2`](https://github.com/lt-mayonesa/hexagon/commit/2b283d2838521f2bb96239f6070b73d9d063026e))

also: - python 3.11 support: dataclass dont allow mutable - drop support for python 3.7


## v0.48.1 (2023-09-12)

### Bug Fixes

- **prompt**: Dont set default on inquiry type Enum
  ([`c604507`](https://github.com/lt-mayonesa/hexagon/commit/c604507fe43320430685527117fb911f51381834))


## v0.48.0 (2023-09-12)

### Features

- **prompt**: Support ints, floats, paths globs, secrets
  ([#46](https://github.com/lt-mayonesa/hexagon/pull/46),
  [`60e39fc`](https://github.com/lt-mayonesa/hexagon/commit/60e39fc200fcd197e96e44960ba7b45d448a358a))


## v0.47.1 (2023-08-07)

### Bug Fixes

- **execute**: Pass user PATH to scripts execution
  ([`6c6157c`](https://github.com/lt-mayonesa/hexagon/commit/6c6157c667563584281dbd553ed9eae8a1904add))


## v0.47.0 (2023-08-07)

### Continuous Integration

- **reports**: Set permissions for publish
  ([`a3d2d47`](https://github.com/lt-mayonesa/hexagon/commit/a3d2d470091bc4bd5488a5c3004bcc7729460b68))

### Features

- Re-organized packages ([#44](https://github.com/lt-mayonesa/hexagon/pull/44),
  [`f90bd8e`](https://github.com/lt-mayonesa/hexagon/commit/f90bd8e8e02de987ccaf6c91003c509cd89ba873))

separated between `runtime` and `support`, also `support` distinguishes between `input` and `output`
  packages

this is a breaking change, but we are in alpha so ¯\_(ツ)_/¯


## v0.46.2 (2023-08-06)

### Bug Fixes

- **update**: Update current git branch
  ([`7417c4d`](https://github.com/lt-mayonesa/hexagon/commit/7417c4dc50a05caaf109696363407d78746fa90f))

when checking for changes only do it against current tracked branch, and keep local in the same

### Continuous Integration

- **e2e**: Retry e2e tests in case of failure
  ([`9ed2889`](https://github.com/lt-mayonesa/hexagon/commit/9ed2889da1cb04e02ec24d35934ac762f796c69e))

sometimes, mostly on python 3.7, one test will fail because it times out when reading STDOUT from an
  HexagonSpec.

Not sure of the root cause so far


## v0.46.1 (2023-08-06)

### Bug Fixes

- **logger**: Check status level on status_aware
  ([`d893dcb`](https://github.com/lt-mayonesa/hexagon/commit/d893dcbc9f437efdf12ef758ae4dd84afd32071a))


## v0.46.0 (2023-08-06)

### Continuous Integration

- **nightly**: Comment PR with link to nightly release
  ([#35](https://github.com/lt-mayonesa/hexagon/pull/35),
  [`b7912de`](https://github.com/lt-mayonesa/hexagon/commit/b7912de23b5cce671cdcfec013792b66149e9b9b))

- **release**: Rollback to using personal access token
  ([`1c83083`](https://github.com/lt-mayonesa/hexagon/commit/1c8308378c26911c94b189559bb8c831449391fa))

- **release**: Use correct gh token
  ([`b0d1a35`](https://github.com/lt-mayonesa/hexagon/commit/b0d1a35edbb0adbe185dd26face3e284375970fa))

### Features

- **args**: Allow to set prompt instruction message
  ([#36](https://github.com/lt-mayonesa/hexagon/pull/36),
  [`b79ee9a`](https://github.com/lt-mayonesa/hexagon/commit/b79ee9affc456d94e3df07e01880d08f31899c5f))

- **prompt**: Show help texts for prompts
  ([`0c4ec1f`](https://github.com/lt-mayonesa/hexagon/commit/0c4ec1f96028ae45f262c6bcb3d6728149d2d387))

hints/helps can be disabled with `options.hints_disabled`


## v0.45.0 (2023-07-29)

### Bug Fixes

- **groups**: Display go back icon correctly
  ([`b214adc`](https://github.com/lt-mayonesa/hexagon/commit/b214adcf3d516472717b0a022ea9ca4199cda0bd))

- **update**: Show status correctly when updating
  ([`169dc99`](https://github.com/lt-mayonesa/hexagon/commit/169dc998bdf4cfdfb006e776c7f83b683bd7e858))

### Features

- **status**: Allow to nest statuses and prompt inside
  ([`d6e194e`](https://github.com/lt-mayonesa/hexagon/commit/d6e194e4c4ee9e352d9f7e484a7ce4d08dc9bcc6))


## v0.44.0 (2023-07-29)

### Bug Fixes

- **dependencies**: Show progress by individual install
  ([`c0a0f2e`](https://github.com/lt-mayonesa/hexagon/commit/c0a0f2ed15fa186a4dd05c9d196e4467497f7394))

- **dependencies**: Use faster tree search
  ([`493aa54`](https://github.com/lt-mayonesa/hexagon/commit/493aa542dfa703b08a553008eedeae2a7a616fe6))

- **install**: Use correct path for dependency install
  ([`f792d01`](https://github.com/lt-mayonesa/hexagon/commit/f792d0121f1cc20f0e95eafe013bfedc325ce58f))

### Documentation

- Rollback changelog
  ([`eee2034`](https://github.com/lt-mayonesa/hexagon/commit/eee2034442be6b9410a2866a58b3f0b1d9261e88))

- **setup**: Update local setup instractions
  ([`12a7da7`](https://github.com/lt-mayonesa/hexagon/commit/12a7da732aabb517e1be83487b5e624fa656dfc8))

### Features

- **args**: Allow to specify default in prompt
  ([`69303d3`](https://github.com/lt-mayonesa/hexagon/commit/69303d3ad38c110a0ff75807dcf580ef2af10fea))


## v0.43.2 (2023-07-24)

### Bug Fixes

- **dependencies**: Handle case when no custom dir present
  ([`ff7a5e8`](https://github.com/lt-mayonesa/hexagon/commit/ff7a5e8292a1120ec4b053ba516ed752e84cba70))

- **errors**: Handle case when no custom dir present
  ([`61362ba`](https://github.com/lt-mayonesa/hexagon/commit/61362ba4f251763bca573f7936c75655a6fa50f4))

- **release**: Empty change to trigger new release
  ([`f4d7492`](https://github.com/lt-mayonesa/hexagon/commit/f4d7492263672d3816f2f9e5fae9ae85cf7c2669))

- **release**: Rollback to v7.34.6
  ([`372fa02`](https://github.com/lt-mayonesa/hexagon/commit/372fa0256fde3e6c1d6ae15ec4a69a1e84aa6e71))

- **update**: Ignore versions entries with chore types
  ([`5e063c4`](https://github.com/lt-mayonesa/hexagon/commit/5e063c4d431f7fdde91c6242bccd1c500cb44dbe))

### Chores

- **e2e**: 3.7 failing test
  ([`cb360b0`](https://github.com/lt-mayonesa/hexagon/commit/cb360b0baacd899e527326a0fae75c880640e769))

- **e2e**: Allow to specify multiple yaml
  ([`5da4d92`](https://github.com/lt-mayonesa/hexagon/commit/5da4d9272cfda5440ea6a55033ddb4dcf6383cc0))

### Continuous Integration

- **release**: Migrate to v8 of semantic release
  ([`ec9a531`](https://github.com/lt-mayonesa/hexagon/commit/ec9a5315abfa8a6f07982d2a6edba87064bf75ee))

### Refactoring

- **dependencies**: Dry up code
  ([`b8a843e`](https://github.com/lt-mayonesa/hexagon/commit/b8a843e46fab26953f6949697fa5d772dc2bb229))


## v0.43.1 (2023-07-09)

### Bug Fixes

- **install**: Use string instead of posixpath
  ([`f645906`](https://github.com/lt-mayonesa/hexagon/commit/f64590691f3e7c7d5c1e7bfa073b01c9806c1821))

- **update**: Ignore errors when updating
  ([`2a40c98`](https://github.com/lt-mayonesa/hexagon/commit/2a40c98cb2154123ba4e2d7428b733afdaae8993))

### Chores

- Removed unused pipenv-setup ([#24](https://github.com/lt-mayonesa/hexagon/pull/24),
  [`ba91768`](https://github.com/lt-mayonesa/hexagon/commit/ba917681fb7a4decd9b0f50166a1abd7a1f7ce37))

- **e2e**: Fix flaky test
  ([`5a946f7`](https://github.com/lt-mayonesa/hexagon/commit/5a946f7f582d99de73d9be29629f572827f8f32e))

- **flake8**: Remove unused variable
  ([`09165d1`](https://github.com/lt-mayonesa/hexagon/commit/09165d180b5e6d0a8aea3ee8492f9aaf8e10debf))

- **update**: Don't use local imports
  ([`0f5e2a6`](https://github.com/lt-mayonesa/hexagon/commit/0f5e2a6189c87a399b1fe15caaf7d8b59567b090))

- **update**: Handle deprecated package pkg_resources
  ([`cc63668`](https://github.com/lt-mayonesa/hexagon/commit/cc636681d185878edcf99deb0cecda1c6c09f882))

- **update**: Parse test version correctly
  ([`20f3517`](https://github.com/lt-mayonesa/hexagon/commit/20f35171d3566e5fdbb923492f63fdd24779662f))

- **update**: Revert local imports usage
  ([`ff32c5b`](https://github.com/lt-mayonesa/hexagon/commit/ff32c5b26f58f3d1ea0e9ff67eeb3ab73f447d45))

### Testing

- **e2e**: Add bigger timeout
  ([`0b148e9`](https://github.com/lt-mayonesa/hexagon/commit/0b148e963524f73c853bd255a15266d91646de4d))

- **e2e**: Extra ouput validation
  ([`c71db14`](https://github.com/lt-mayonesa/hexagon/commit/c71db14bb5444c43c5e60a05fd7c53770c5d63e2))

- **e2e**: Match output
  ([`1dcfecc`](https://github.com/lt-mayonesa/hexagon/commit/1dcfeccc31494bed18f162ace8bc72834fc66d4a))

- **e2e**: Output complete log even on errors
  ([`807d19a`](https://github.com/lt-mayonesa/hexagon/commit/807d19aadc73303c2d5a5af0cd56245dc05ed7ec))

- **e2e**: Use no_border theme instead of default
  ([`b03162b`](https://github.com/lt-mayonesa/hexagon/commit/b03162b7215710d9af46c837d5b79c3a9e764fc7))

- **e2e**: Validate more outputs
  ([`787f329`](https://github.com/lt-mayonesa/hexagon/commit/787f329199d385472a733c028bbdd57dea8bd317))


## v0.43.0 (2023-05-06)

### Features

- **args**: Prompt same arg multiple times and trace
  ([`7a96e23`](https://github.com/lt-mayonesa/hexagon/commit/7a96e23cc8e2c69b6f2e07558bd37041af927830))


## v0.42.1 (2023-05-06)

### Bug Fixes

- **args**: Use correct value when tracing
  ([`f00dac8`](https://github.com/lt-mayonesa/hexagon/commit/f00dac85f2e10621826a9312f5d2eab02271606a))


## v0.42.0 (2023-05-02)

### Features

- **args**: Add prompt API to hexagon args
  ([`6cfb88f`](https://github.com/lt-mayonesa/hexagon/commit/6cfb88fc309a303ee234821754b061ae4606404f))


## v0.41.1 (2023-04-13)

### Bug Fixes

- **args**: Apply default type validation when prompting
  ([`f97911f`](https://github.com/lt-mayonesa/hexagon/commit/f97911faee9d4437d2f92344276a8c69af346270))

### Chores

- **test**: Ignore blank lines when matching outout
  ([`9607636`](https://github.com/lt-mayonesa/hexagon/commit/96076362b10dbc2f3d9f02440346b460b2ef37f9))


## v0.41.0 (2023-04-13)

### Chores

- **dependencies**: Update to newest versions
  ([`c1bc52d`](https://github.com/lt-mayonesa/hexagon/commit/c1bc52daae64de2e51da04e60ad15819c3ca366d))

- **test**: Log hexagon spec steps
  ([`f1a3e00`](https://github.com/lt-mayonesa/hexagon/commit/f1a3e00cd8e8b064a65141d3eee7ca7107fd4a5b))

### Features

- **theme**: Add no_border prompt theme
  ([`bb39265`](https://github.com/lt-mayonesa/hexagon/commit/bb39265274507eeac3c47605d41bc0b21d317de1))

also simplify e2e tests


## v0.40.0 (2023-04-12)

### Features

- **args**: Do not validate special characters on args
  ([`e793175`](https://github.com/lt-mayonesa/hexagon/commit/e79317551d686021d50915c61e25de69d80bf29e))

- **args**: Wrap default value in HexagonArg
  ([`7d5eae4`](https://github.com/lt-mayonesa/hexagon/commit/7d5eae4da5d56768664968dacab08a5ce64b706a))

### Refactoring

- **args**: Rename Field to Arg
  ([`b742568`](https://github.com/lt-mayonesa/hexagon/commit/b742568336920d82b7a7b6e319d62e0e1f31951a))

- **args**: Use positional and optional instances
  ([`b1f9e61`](https://github.com/lt-mayonesa/hexagon/commit/b1f9e613200fe40b48365984a272046c3f34a0cb))


## v0.39.0 (2023-04-10)

### Features

- **args**: Apply model validations when prompting
  ([`86bf096`](https://github.com/lt-mayonesa/hexagon/commit/86bf096817194810d0143bc98bfafad575435115))

- **args**: Prompt for tool arguments from cli_args object
  ([`67d65ab`](https://github.com/lt-mayonesa/hexagon/commit/67d65ab9a4a20cc9b6d7438854cc480decdbbb07))

other fixes

### Refactoring

- **inquirer**: Hide usage behind prompt
  ([`d68d01c`](https://github.com/lt-mayonesa/hexagon/commit/d68d01c9da08343acba94ca81d170bdb3b2ba938))

cleanup of tools seed and docker_registry, they will be added to their own repos

- **tracer**: Store trace object instead of string
  ([`4c79362`](https://github.com/lt-mayonesa/hexagon/commit/4c793622ceea67fb6373089b536de6859daa5e9f))


## v0.38.1 (2023-04-06)

### Bug Fixes

- **args**: Trace all input args and one time only
  ([`8b69454`](https://github.com/lt-mayonesa/hexagon/commit/8b6945487dddf9d4bb31a916743689e1831ee13b))


## v0.38.0 (2023-04-05)

### Continuous Integration

- Adjust workflow naming
  ([`91e94c3`](https://github.com/lt-mayonesa/hexagon/commit/91e94c3034b5f97b6c17cfeb30469deef28a5785))

- Use github environment files
  ([`fbffcc3`](https://github.com/lt-mayonesa/hexagon/commit/fbffcc3b0583aad35dc18a7f7515f4446063b6ee))

### Features

- **execute**: When executing script pass tool & env as envvars
  ([`2c17a33`](https://github.com/lt-mayonesa/hexagon/commit/2c17a332215f1936de97549a450f36aac64cc86a))

### Refactoring

- Centralize error handling in main catch
  ([`dd648bc`](https://github.com/lt-mayonesa/hexagon/commit/dd648bc2986a838cf989c1442a3df19a7147d6bd))

- Reducing main complexity
  ([`40969b6`](https://github.com/lt-mayonesa/hexagon/commit/40969b681f1d06780ff24c23ad1581f6a93c01a2))

- Remove dependency from plugins
  ([`90ab695`](https://github.com/lt-mayonesa/hexagon/commit/90ab69533dd2052fbb4346ca0513a9bf54603dd4))

- Remove logic from hexagon.domain.__init__
  ([`e283f88`](https://github.com/lt-mayonesa/hexagon/commit/e283f88db627039705e55b9184c2052210ab0ced))

- **tracer**: Handle execute again in tracer
  ([`a8b11da`](https://github.com/lt-mayonesa/hexagon/commit/a8b11dabd276648bca88d97322e771c6a78067f0))


## v0.37.0 (2023-04-03)

### Chores

- **i18n**: Fix message id
  ([`b66d48d`](https://github.com/lt-mayonesa/hexagon/commit/b66d48d47589246df7ae4ea1fdf522df9735c4d7))

### Continuous Integration

- **report**: Add comment to PR with tests results
  ([`865b3cc`](https://github.com/lt-mayonesa/hexagon/commit/865b3cc26bab86396fde855ee15a814c1351a972))

### Features

- **args**: Show validation error matching hexagon format
  ([`6027468`](https://github.com/lt-mayonesa/hexagon/commit/6027468e00b645c64b29f08f1313754033971774))


## v0.36.0 (2023-04-02)

### Features

- **args**: Show help text for tools
  ([`9e387a7`](https://github.com/lt-mayonesa/hexagon/commit/9e387a7f0872029fd703c0bb87fba35ac6b7aa71))


## v0.35.1 (2023-04-01)

### Bug Fixes

- **args**: Handle case when last optional arg has missing value
  ([`e05004b`](https://github.com/lt-mayonesa/hexagon/commit/e05004bf393ed79bf3a7283fe4d8938aa3a5d236))


## v0.35.0 (2023-04-01)

### Bug Fixes

- **args**: Support extend on python 3.7
  ([`e4c0581`](https://github.com/lt-mayonesa/hexagon/commit/e4c0581a75a635dfb43f1a7166e1f0fd023b7a6d))

### Chores

- **e2e**: Always print command output
  ([`d9a88a6`](https://github.com/lt-mayonesa/hexagon/commit/d9a88a683ef22725189dff7ae2717aa0a6a43e4d))

### Continuous Integration

- **report**: Use wildcard for reports
  ([`ceb4dcd`](https://github.com/lt-mayonesa/hexagon/commit/ceb4dcd9765e24399c6b8083961aea7e4f8f003a))

### Features

- **args**: Added support for tool args
  ([`ebd5443`](https://github.com/lt-mayonesa/hexagon/commit/ebd5443d2d732099765cd7fb869e8cc70818b85e))

users define a class Args(ToolArgs) in their python actions that will automagically parse CLI input
  args specific for this action

### Refactoring

- **args**: Rename support module
  ([`26c3cd5`](https://github.com/lt-mayonesa/hexagon/commit/26c3cd56675484efae39b755f4a7eb52ad09a945))


## v0.34.0 (2023-03-27)

### Chores

- Updating directories structure
  ([`7174bb2`](https://github.com/lt-mayonesa/hexagon/commit/7174bb24221843ed4946bd8f32cb3d663f2eff28))

new structure should be more easy to follow

- **e2e**: Set terminal COLUMNS size to 200
  ([`99b431e`](https://github.com/lt-mayonesa/hexagon/commit/99b431e8408a63cd5ccbb9f2c78a65f50ae96c9f))

### Continuous Integration

- **report**: Added unit tests junit report
  ([`6cc05e9`](https://github.com/lt-mayonesa/hexagon/commit/6cc05e9f7b790146f6c674beaea67deb1e946b60))

### Features

- **tracer**: Add support for optional cli_args
  ([`a7b5a9d`](https://github.com/lt-mayonesa/hexagon/commit/a7b5a9d9779c3990687db31c83f20393dd552bec))


## v0.33.0 (2023-03-26)

### Chores

- Fix flake8 reports
  ([`29167b5`](https://github.com/lt-mayonesa/hexagon/commit/29167b55c409d5dfc57f0f0c31375ac88755b5f5))

- **i18n**: Update po line references
  ([`8b35967`](https://github.com/lt-mayonesa/hexagon/commit/8b359677218c25dda69d82a7fe79057a8d42604e))

- **test**: Stub i18n for unit tests
  ([`5e60597`](https://github.com/lt-mayonesa/hexagon/commit/5e60597a18b1730c5149f760539a2b0685a3be80))

### Features

- **cli-args**: Pass extra cli args to execution of actions
  ([`528827a`](https://github.com/lt-mayonesa/hexagon/commit/528827a3130abbbd4318846036130f9370ff55f0))

- python actions receive a dict, ie: {'foo': 'bar'} - command actions receive the extra args as-is,
  ie: --foo bar

### Refactoring

- Use decorator for execute hook
  ([`ce5d8dc`](https://github.com/lt-mayonesa/hexagon/commit/ce5d8dc5c72f0f6a1b9f229ea02c305902514223))

- **cli-args**: Use argparse for better support
  ([`d26d33f`](https://github.com/lt-mayonesa/hexagon/commit/d26d33f4335c8be4507d8adede345ec46b4e16d7))


## v0.32.0 (2023-03-16)

### Chores

- **e2e**: Skip timeout when debugging
  ([`c5523a9`](https://github.com/lt-mayonesa/hexagon/commit/c5523a9cda1e94b8a4455bae0f3a02afab20eae6))

### Continuous Integration

- **report**: Use github token
  ([`6e78d9c`](https://github.com/lt-mayonesa/hexagon/commit/6e78d9cc107b93f05b05621bb6d81f70421441b1))

### Features

- **options**: Allow override options at yaml level
  ([`08f4258`](https://github.com/lt-mayonesa/hexagon/commit/08f425800f4b719cceb3391e59a1965c7f57c856))

let users defines values in cli.options to override some hexagon configurations, ie: update checks,
  themes, etc.

fixes #2


## v0.31.0 (2023-03-13)

### Continuous Integration

- **test**: Upload test report to github
  ([`4a76871`](https://github.com/lt-mayonesa/hexagon/commit/4a76871b4b052aae4a28d42b7a9c5415dc9b7c36))

- **test**: Use java-junit reporter
  ([`057d1b3`](https://github.com/lt-mayonesa/hexagon/commit/057d1b37c182eb925e9dfcba089c03a321204441))

### Features

- **analytics**: Remove support for tracking
  ([`e8adefe`](https://github.com/lt-mayonesa/hexagon/commit/e8adefe440294988742d93d7bcd13454b2e03696))


## v0.30.0 (2023-03-12)

### Continuous Integration

- Update project metadata
  ([`a7c311d`](https://github.com/lt-mayonesa/hexagon/commit/a7c311dc8e5968102841961d7fa352a4bd263ac6))

- **devex**: Use personal access token
  ([`4996bc3`](https://github.com/lt-mayonesa/hexagon/commit/4996bc3d902efd1bd64d849f471487fba3f990a6))

### Features

- **messages**: Show path when installing dependencies
  ([`b060dcc`](https://github.com/lt-mayonesa/hexagon/commit/b060dcc8b4311dbf03713b0ef76a0056b222cf96))


## v0.29.0 (2023-03-12)

### Bug Fixes

- Added packaging to dependencies ([#44](https://github.com/lt-mayonesa/hexagon/pull/44),
  [`6b5ddec`](https://github.com/lt-mayonesa/hexagon/commit/6b5ddec86d53ca0f8d64f3f3938f959a084ae375))

- Allow for tools with no alias
  ([`eb25e89`](https://github.com/lt-mayonesa/hexagon/commit/eb25e8976581bc9f39852b93444c91b6a074210f))

- Changelog in hexagon update ([#48](https://github.com/lt-mayonesa/hexagon/pull/48),
  [`c6ab57d`](https://github.com/lt-mayonesa/hexagon/commit/c6ab57de27d3d0f8d4d441e198f273b0cd204554))

- Hexagon auto-update ([#42](https://github.com/lt-mayonesa/hexagon/pull/42),
  [`2720c6a`](https://github.com/lt-mayonesa/hexagon/commit/2720c6a1d1e1a2ecb2682244702a3b313a1a9a0d))

- Print help gaps
  ([`e130331`](https://github.com/lt-mayonesa/hexagon/commit/e130331f4e347c57e0bcb246b476063452c15911))

do not add gap after description if it's the last in the list

solves #32

- Simplify always true cli.command
  ([`c72de85`](https://github.com/lt-mayonesa/hexagon/commit/c72de855b7f8a0e236a9ea100d0e2662f8d90895))

- **action**: Validate action is valid module identifier
  ([#78](https://github.com/lt-mayonesa/hexagon/pull/78),
  [`e583078`](https://github.com/lt-mayonesa/hexagon/commit/e5830787b96432c2c142f96a5850089c5958ace9))

- **alias**: Source new aliases ([#64](https://github.com/lt-mayonesa/hexagon/pull/64),
  [`c13f59b`](https://github.com/lt-mayonesa/hexagon/commit/c13f59b454e7c3df45efd3c3267eb0ed32cad1a8))

when creating an OS alias source the file so the user has the alias on path

- **analytics**: Register user_id and client_id
  ([`18a621e`](https://github.com/lt-mayonesa/hexagon/commit/18a621ed1b6998644ff5bcdb59218393fc7e726f))

- **analytics**: Switch user_id and client_id scope
  ([`6718c7c`](https://github.com/lt-mayonesa/hexagon/commit/6718c7cb94c8a2693d795cfc97339bf6dd9a6678))

- **create-tool**: __templates dir and custom tools path
  ([#9](https://github.com/lt-mayonesa/hexagon/pull/9),
  [`5ebde69`](https://github.com/lt-mayonesa/hexagon/commit/5ebde697b840e5da0ea62341ef22831ecc53a50d))

- During setup configuration.custom_tools_path is handled as absolute or relative to YAML -
  HEXAGON_CONFIG_FILE .yaml can now take any name - __templates dir takes into account *.md files -
  e2e excluded from dist

- **create-tool**: Change ordering of YAML key insert
  ([`1ce6024`](https://github.com/lt-mayonesa/hexagon/commit/1ce6024b06f6b6cfbf0b0af8db6d6703a79efd35))

- **create-tool**: Readme lost during package
  ([#77](https://github.com/lt-mayonesa/hexagon/pull/77),
  [`b7238cd`](https://github.com/lt-mayonesa/hexagon/commit/b7238cddbcc07c09e5e20eb10d9e5dd7f396516f))

- **create-tool**: Templates directory not published
  ([`0f1e85c`](https://github.com/lt-mayonesa/hexagon/commit/0f1e85c45969d1f1f5cd7ab9dbb0b4018f9a8243))

use os.path.join on create_new_tool

- **e2e**: Refactored tests, improved output assert message
  ([#18](https://github.com/lt-mayonesa/hexagon/pull/18),
  [`fa41c0d`](https://github.com/lt-mayonesa/hexagon/commit/fa41c0d315e1c91f84421c5c0a0fb36ac37855c3))

- **execute**: Fail with custom message when action not found
  ([`5ea46f2`](https://github.com/lt-mayonesa/hexagon/commit/5ea46f21aa69dfd5de615d67ac823034b6854ac4))

- **execute**: Pass env object correctly
  ([`86bbc68`](https://github.com/lt-mayonesa/hexagon/commit/86bbc689001339f0bfc128b25520244ed7f966ec))

- **execute**: Run install_cli and other internal tools
  ([#2](https://github.com/lt-mayonesa/hexagon/pull/2),
  [`71cc90b`](https://github.com/lt-mayonesa/hexagon/commit/71cc90b9493332825f78163854422db5d2ec493d))

- **execute**: Use subprocess shell=True ([#38](https://github.com/lt-mayonesa/hexagon/pull/38),
  [`6d5e1e8`](https://github.com/lt-mayonesa/hexagon/commit/6d5e1e8e2e6ce62ca15acbf9d002d3ae6d0881ef))

execute commands spawning an intermediate shell process (shell=True) for a more native experience.
  Also use sh instead of bash as default shell

fixes #37

- **execute-again**: Show command aliases correctly
  ([`922e554`](https://github.com/lt-mayonesa/hexagon/commit/922e5547c214f3819c9159eea174da28c3bd3856))

do a recursive search of tools and envs to find the aliases applied black formatting

- **help**: Help expecting dict crashes
  ([`cf86f99`](https://github.com/lt-mayonesa/hexagon/commit/cf86f99c56e9c5a4affe426021b3230ef342d99f))

- **help**: Optional alias
  ([`3cf1f6a`](https://github.com/lt-mayonesa/hexagon/commit/3cf1f6a46276468fc7a9ae5bbb4445ff4f544d11))

do not print "(alias)" in help when tool has none

- **help**: Support tools with no long_name
  ([`46c0f89`](https://github.com/lt-mayonesa/hexagon/commit/46c0f896dfb63288b3662b8d08499c6c66998b47))

- **i18n**: Missing translation strings ([#76](https://github.com/lt-mayonesa/hexagon/pull/76),
  [`97a1068`](https://github.com/lt-mayonesa/hexagon/commit/97a1068ec8c4eb771466676a84215a0b458fc84c))

use str.format so all strings are translated correctly

- **i18n**: Search local and system dirs
  ([`af62986`](https://github.com/lt-mayonesa/hexagon/commit/af6298632e78c289f2bf50b855a63a93526efd89))

lookup is done: 1. HEXAGON_LOCALES_DIR if present 2. local install dir (~/.local) 4. system install
  dir (/usr/local) 6. default gettext lookup dir or fallback

- **install**: Wrong action definition for tool install
  ([`425dfd3`](https://github.com/lt-mayonesa/hexagon/commit/425dfd349da6c60361ef69839752126632c67bd7))

- **install-cli**: Only store bin_path if prompted
  ([`32dbc6c`](https://github.com/lt-mayonesa/hexagon/commit/32dbc6c0c5081b1a4db589f49e3b5fa8498c9a74))

- **last-command**: Store last command whe tool executed directly
  ([`1f6c887`](https://github.com/lt-mayonesa/hexagon/commit/1f6c8875317245b599b18063420650277d9d27b8))

- **save-alias**: Bash on fresh install ([#8](https://github.com/lt-mayonesa/hexagon/pull/8),
  [`1754d2c`](https://github.com/lt-mayonesa/hexagon/commit/1754d2c02fde3231a142bc2fa51c344eef390e37))

Co-authored-by: Joaco Campero <joaquin@redb.ee>

- **save-alias**: Create aliases file if does not exist
  ([`9055055`](https://github.com/lt-mayonesa/hexagon/commit/9055055c8def45fc1b84c5b13388be50e259f86a))

- **tracer**: Do not print alias for internal tools
  ([`5d798fe`](https://github.com/lt-mayonesa/hexagon/commit/5d798fe1d49b12b36bcf74decc1765468c888422))

- **wax**: Make classifier optional
  ([`4e8ff5b`](https://github.com/lt-mayonesa/hexagon/commit/4e8ff5bce035883b49a21f062c4a543529983f69))

- **wax**: Show classifier when no long_name
  ([`bc8a485`](https://github.com/lt-mayonesa/hexagon/commit/bc8a485ced377d6ddd78ae7617a6fc1f6d2ad889))

- **yaml**: Handle error for None values
  ([`33300c6`](https://github.com/lt-mayonesa/hexagon/commit/33300c6463ab7f0accdccf0b46ed7fb96be64ac4))

- **yaml**: Print YAML path
  ([`bfc60ae`](https://github.com/lt-mayonesa/hexagon/commit/bfc60ae1b60f2664934f999176067dfe374b2015))

### Chores

- Added open source license
  ([`4985837`](https://github.com/lt-mayonesa/hexagon/commit/4985837e47ccc501f7bbeb99cb59aed38283e5bd))

- Fix flake8 errors
  ([`c9e067d`](https://github.com/lt-mayonesa/hexagon/commit/c9e067d7e9f60fa648886d7b8bf99f1230f08217))

- Fix strings in spanish
  ([`1ddedf7`](https://github.com/lt-mayonesa/hexagon/commit/1ddedf777509029d8ae33107198740d57d7f5839))

- Rollback to version 0.8.0
  ([`0aa3057`](https://github.com/lt-mayonesa/hexagon/commit/0aa30578f5295e445be0ba5412b9c2334c3c0149))

- Update dependencies ([#84](https://github.com/lt-mayonesa/hexagon/pull/84),
  [`e970496`](https://github.com/lt-mayonesa/hexagon/commit/e970496618200f7ff0b2a75e107ddc7455a0547b))

black was breaking in CI so dependencies needed to be updated

- **ci**: Do not release on PR
  ([`b186229`](https://github.com/lt-mayonesa/hexagon/commit/b186229a0bbec44d1f3ed7290ad1d23c8f5df896))

- **ci**: Fix flake8 action
  ([`1b8e229`](https://github.com/lt-mayonesa/hexagon/commit/1b8e229ea49c4258fcb8c23488c6a8ab92d11d29))

- **ci**: Lint with github action ([#6](https://github.com/lt-mayonesa/hexagon/pull/6),
  [`9a571aa`](https://github.com/lt-mayonesa/hexagon/commit/9a571aa6dcec2b27707494a449a14b517228c665))

- **ci**: Release commit subject
  ([`fdd833d`](https://github.com/lt-mayonesa/hexagon/commit/fdd833d1bcdbcb7003fdd2f6af15bbaf0bc1d70b))

- **ci**: Sync TODOs comments with issues
  ([`3a8020e`](https://github.com/lt-mayonesa/hexagon/commit/3a8020e98b39ffe08835552ea739b7804f02a12c))

- **ci**: Use official flake8 action
  ([`9ac7863`](https://github.com/lt-mayonesa/hexagon/commit/9ac78637ec77f8eca381513d7ac28e85b85c824b))

- **ci**: Use version number in README
  ([`3d6ea08`](https://github.com/lt-mayonesa/hexagon/commit/3d6ea0811544c895d7fc37210bb8ed939f205c77))

- **create-tool**: Template tool in english
  ([`38e996e`](https://github.com/lt-mayonesa/hexagon/commit/38e996ec7a9ffa5a38a1fd773bb1a0d4f3b78500))

- **e2e**: Missing comma on run command
  ([`bce20d1`](https://github.com/lt-mayonesa/hexagon/commit/bce20d192ab1c669d8fb281e9dea1ceb528ed562))

- **i18n**: Use MANIFEST for data
  ([`ba3e5e6`](https://github.com/lt-mayonesa/hexagon/commit/ba3e5e6c9158f77e90c47167a7e866fd40b5ae01))

- **IDE**: Setup black file watcher correctly
  ([`d2fa58c`](https://github.com/lt-mayonesa/hexagon/commit/d2fa58cb28464ac536c1e8473e0fd92896d6988d))

- **package**: Pipenv use setup.py install_requires
  ([`b8f0ec2`](https://github.com/lt-mayonesa/hexagon/commit/b8f0ec25cac4aaeef394d45dc7471e915eea3bae))

### Code Style

- **black**: Automate code linting with black
  ([#10](https://github.com/lt-mayonesa/hexagon/pull/10),
  [`5372299`](https://github.com/lt-mayonesa/hexagon/commit/53722998c9649f5bf555edcfc7d12a9a06e57c4c))

### Continuous Integration

- Update dependencies and workflows
  ([`4bace03`](https://github.com/lt-mayonesa/hexagon/commit/4bace0396f573d212e332b94dc17a5504c3539a9))

- **build**: Agrego action de package
  ([`f9e8376`](https://github.com/lt-mayonesa/hexagon/commit/f9e8376e97df4c247871ec00f6b170937e95cb01))

- **guidelines**: Use versions from lockfile
  ([`794af5b`](https://github.com/lt-mayonesa/hexagon/commit/794af5b045f041b21e9d3482bd1c0c106b9e88a8))

- **package**: Use Pipfile.lock for install_requires deps
  ([#66](https://github.com/lt-mayonesa/hexagon/pull/66),
  [`ad01850`](https://github.com/lt-mayonesa/hexagon/commit/ad0185098546eb689263752b4a1b438a65e10200))

also generate a hexagon build in place for e2e tests

- **publish**: Publicar en repositorio
  ([`49217de`](https://github.com/lt-mayonesa/hexagon/commit/49217de25a01d829bcc1ffb39245c705072020ad))

- **release**: Compilar correctamente tar.gz
  ([`9f44350`](https://github.com/lt-mayonesa/hexagon/commit/9f4435059b7ae9000b707727933916f366cce6dc))

- **release**: Correcciones de packaging
  ([`c55f35c`](https://github.com/lt-mayonesa/hexagon/commit/c55f35cea1184287cb7211c0b1d39f13883c1b12))

- **release**: Correr con tags
  ([`1b076ff`](https://github.com/lt-mayonesa/hexagon/commit/1b076ff9263a2ec823cab0929e13f90005c5f7a8))

- **release**: Do not pump version in package workflow
  ([`25164d1`](https://github.com/lt-mayonesa/hexagon/commit/25164d1d2c100988e899bafda6f48ac49347ff07))

- **release**: Execute release outside matrix
  ([`45eca58`](https://github.com/lt-mayonesa/hexagon/commit/45eca58c7d0c762ca8830e02d71f7e0fb07c5ae6))

- **release**: Fix indent error
  ([`2a8269c`](https://github.com/lt-mayonesa/hexagon/commit/2a8269c4b035eccd74b3c7b814f97e311b8e3a5e))

- **release**: Subir asset de release
  ([`1165c4a`](https://github.com/lt-mayonesa/hexagon/commit/1165c4a6896ccf36ed39c755fa5bf0547b79e511))

- **release**: Uso de semantic release
  ([`421177e`](https://github.com/lt-mayonesa/hexagon/commit/421177ee6b40d40063262a8e1dbb58ae18a1911a))

- **security**: Use personal access token for release
  ([`d52be3b`](https://github.com/lt-mayonesa/hexagon/commit/d52be3b197a44601d321adb980f420d5a9f9e6e1))

- **tests**: Ejecución de tests
  ([`2219798`](https://github.com/lt-mayonesa/hexagon/commit/2219798abd9bd29783807ccd674db94aa01ce6bd))

### Documentation

- Adding gif example to readme
  ([`e2b4c1b`](https://github.com/lt-mayonesa/hexagon/commit/e2b4c1ba0e082ec998a63ba497dd627022037c1b))

- Basic readme content
  ([`7a82b34`](https://github.com/lt-mayonesa/hexagon/commit/7a82b3490f2b112c9a35fad4a789de1d2341ad69))

- Better resolution gif
  ([`897eeee`](https://github.com/lt-mayonesa/hexagon/commit/897eeee4ed1472ab993a36eadd1408161d2a2317))

- English, slogan, and reference to template repo
  ([`9a9fc96`](https://github.com/lt-mayonesa/hexagon/commit/9a9fc96f42d4ea81a57bda822de7c098d31015a6))

- Update README to be compatible with v0.12.0
  ([`d25ff3d`](https://github.com/lt-mayonesa/hexagon/commit/d25ff3d59ae072125378bdbb81d2015ad8bc0eb8))

- Yaml example in readme
  ([`86c28d1`](https://github.com/lt-mayonesa/hexagon/commit/86c28d126535e3fb6cd229b623666666aa0e1bd3))

- **release**: Correct regex for README version
  ([`f9b973a`](https://github.com/lt-mayonesa/hexagon/commit/f9b973a514efc0370a32d5b95a515ed461a508c2))

- **release**: Version update comment
  ([`c6a9617`](https://github.com/lt-mayonesa/hexagon/commit/c6a9617e7943adef2095b1a768548c8692cefd67))

### Features

- Auto-update for clis ([#49](https://github.com/lt-mayonesa/hexagon/pull/49),
  [`a03d3e0`](https://github.com/lt-mayonesa/hexagon/commit/a03d3e00c27a39e72298e3f5979711162ded6f1d))

* feat: auto-update for clis

- Define tools & envs as lists ([#26](https://github.com/lt-mayonesa/hexagon/pull/26),
  [`4db03b4`](https://github.com/lt-mayonesa/hexagon/commit/4db03b4e279bf2c82f6c9e8af8265026ea6e25c6))

- Detect and install dependencies (Python, NodeJS) for CLIs
  ([#72](https://github.com/lt-mayonesa/hexagon/pull/72),
  [`febdb38`](https://github.com/lt-mayonesa/hexagon/commit/febdb383e442a5e3cbc528e2c80729b72b651da4))

detect and install dependencies (Python, NodeJS) for CLIs on install and update

closes #71 Co-authored-by: Joaco Campero <joaquin@redb.ee>

Co-authored-by: Joaquin Campero <juacocampero@gmail.com>

- Handle keyboard interrupt gracefully
  ([`a65daa2`](https://github.com/lt-mayonesa/hexagon/commit/a65daa26c3de305a2bacafe7f7a64f9295914c94))

- Nested tools, for grouping and organizing ([#54](https://github.com/lt-mayonesa/hexagon/pull/54),
  [`b5831fd`](https://github.com/lt-mayonesa/hexagon/commit/b5831fdc4f69a6765973f1f5ce1a41ea58d8218c))

* feat: nested tools, for grouping and organizing

- Options by env variables, local options file or defaults
  ([#52](https://github.com/lt-mayonesa/hexagon/pull/52),
  [`6687b94`](https://github.com/lt-mayonesa/hexagon/commit/6687b94a53723f56fb683d53ad26c1a64dd3d025))

* feat: options by env variables, local options file or defaults

- Plugins and hooks ([#61](https://github.com/lt-mayonesa/hexagon/pull/61),
  [`b7f1c08`](https://github.com/lt-mayonesa/hexagon/commit/b7f1c080129c53fcf28db424a0bcca5630e4febd))

* feat: plugins and hooks

- Project setup
  ([`d28bcc9`](https://github.com/lt-mayonesa/hexagon/commit/d28bcc95017ea6214523bdbd03d3b7f78dfb3fc6))

- Springboot, react, nextjs seeds ([#63](https://github.com/lt-mayonesa/hexagon/pull/63),
  [`951b3ab`](https://github.com/lt-mayonesa/hexagon/commit/951b3ab8df92a5cfccc379c0b8cee824dff16cf2))

feat: springboot, react, nextjs seeds

- **action**: Allow defining action as list of commands
  ([`fcc20f1`](https://github.com/lt-mayonesa/hexagon/commit/fcc20f1f30a9ebfcbaa50d99ab3a7897d7af07ca))

- **analytics**: Log and send hexagon usage events
  ([#57](https://github.com/lt-mayonesa/hexagon/pull/57),
  [`c096900`](https://github.com/lt-mayonesa/hexagon/commit/c0969009862e1763ac79d5f5c82d5ee110f4ec88))

events sent: - session start - tool selected (prompt or args) - env selected (prompt or args) -
  action executed - session end

- **config**: Custom tools dir relative to YAML
  ([`fe3e26b`](https://github.com/lt-mayonesa/hexagon/commit/fe3e26bd3598ece02e9fd06ae4397b14edce6947))

- **config**: Only show install cli when no config
  ([`9413f99`](https://github.com/lt-mayonesa/hexagon/commit/9413f99ffa23f562f68acddfe99c73e817e74e3e))

- **custom-tool**: Allow projects to register custom tools
  ([`1cac9ca`](https://github.com/lt-mayonesa/hexagon/commit/1cac9ca80e369f9c05c1dcc3363386d4af0d6828))

hexagon will check for cli.custom_tools_dir in config YAML, if exists it will load that directory as
  a path for python modules.

- **dependencies**: Show status on deps install
  ([#87](https://github.com/lt-mayonesa/hexagon/pull/87),
  [`f84d00b`](https://github.com/lt-mayonesa/hexagon/commit/f84d00b855e6548ec869252075dc0c9b4289457a))

- **domain**: Map YAML to pydantic BaseModel ([#24](https://github.com/lt-mayonesa/hexagon/pull/24),
  [`727a09a`](https://github.com/lt-mayonesa/hexagon/commit/727a09a01f11c34b1225fdcab609b02b2ffbff09))

- **envs**: Make tool.envs optional
  ([`efeec06`](https://github.com/lt-mayonesa/hexagon/commit/efeec064404830ca33c6b4751f55455190c6b9e2))

in tool definition envs dict is now optional

- **execute**: Command actions, closes #22 ([#23](https://github.com/lt-mayonesa/hexagon/pull/23),
  [`26a9e05`](https://github.com/lt-mayonesa/hexagon/commit/26a9e051b497354c55177398f95ef98b0b4149bb))

* feat(execute): command actions, closes #22

- **execute**: Display action errors nicely to user
  ([#43](https://github.com/lt-mayonesa/hexagon/pull/43),
  [`b8ab97f`](https://github.com/lt-mayonesa/hexagon/commit/b8ab97f377bb10fe7c5533c5bbdbbd19938a74b1))

Print errors nicely when python action import fails due to dependency errors, or when fails
  executing due to user errors in script.

- **execute**: Execute action with extension
  ([`fe622a8`](https://github.com/lt-mayonesa/hexagon/commit/fe622a8942d91eb3c2f5c9cbe88d1aac22f1ea0f))

let users define an action with other scripting languages, for now only .js and .sh are supported

- **groups**: Allow for inline groups in YAML
  ([`d29a587`](https://github.com/lt-mayonesa/hexagon/commit/d29a58748dac4e2a60dc0760d526cf78ed2c1034))

refactored group loading, so it is done at configuration time instead of execution time

- **i18n**: Added EN and ES transltions + CI ([#73](https://github.com/lt-mayonesa/hexagon/pull/73),
  [`7c65e74`](https://github.com/lt-mayonesa/hexagon/commit/7c65e740dd74cc7c0e0bdb2ba75587f185d327d2))

- **install**: Install custom cli from YAML
  ([`cb25d68`](https://github.com/lt-mayonesa/hexagon/commit/cb25d680fa2af6448a79e61631542dabc08991a9))

- **install**: Warn commands dir not in PATH ([#86](https://github.com/lt-mayonesa/hexagon/pull/86),
  [`9b42bd4`](https://github.com/lt-mayonesa/hexagon/commit/9b42bd4bc765112e4d799e4c4ca57c128fddbb10))

- **install-cli**: Use shell scripts instead of aliases
  ([`c3d7ed7`](https://github.com/lt-mayonesa/hexagon/commit/c3d7ed76fce7bfae2448554fdb322f777ea5d59d))

- **internal-tools**: Create a new tool
  ([`dfc13aa`](https://github.com/lt-mayonesa/hexagon/commit/dfc13aacf77ec17ba735a519dd4bfbce29047731))

prompt the user for parameters and register the new tool in the YAML and create the python modules
  if action is new

- **prompt**: Sort tools by type
  ([`ef71eae`](https://github.com/lt-mayonesa/hexagon/commit/ef71eae1e2b5bb0b7b996efa5a1c694b52f31235))

- **storage**: Add get_local_config_dir() function
  ([#79](https://github.com/lt-mayonesa/hexagon/pull/79),
  [`ec817d2`](https://github.com/lt-mayonesa/hexagon/commit/ec817d2d4b3bfdd962c6a2dc51216e3b0b53c1ca))

- **styles**: Basic support for hexagon themes
  ([#14](https://github.com/lt-mayonesa/hexagon/pull/14),
  [`b5dd966`](https://github.com/lt-mayonesa/hexagon/commit/b5dd966a221cab477e33adec27fb54fdfc6efefb))

- **support**: Storage api, closes #17 ([#21](https://github.com/lt-mayonesa/hexagon/pull/21),
  [`f8cc5b3`](https://github.com/lt-mayonesa/hexagon/commit/f8cc5b374df56c084c2b1cc48ba0a35c44c6a46e))

* feat(support): storage api, closes #17

- **updates**: Hexagon auto update ([#35](https://github.com/lt-mayonesa/hexagon/pull/35),
  [`16b93ff`](https://github.com/lt-mayonesa/hexagon/commit/16b93ffab29aa817c22b4a9b06e6dda43cc54fc7))

periodically check the latest version of hexagon and suggest for updates

relates to #34

- **yaml**: Show a more precise error to users
  ([#27](https://github.com/lt-mayonesa/hexagon/pull/27),
  [`b635964`](https://github.com/lt-mayonesa/hexagon/commit/b635964789a54006f3f3b4dc31196940487b687f))

closes #20

### Refactoring

- Tool-env selection, follow up to #26, closes #28
  ([#29](https://github.com/lt-mayonesa/hexagon/pull/29),
  [`e42fa36`](https://github.com/lt-mayonesa/hexagon/commit/e42fa36064e0133825d656de0bd55bf48aade684))

- **actions**: Rename 'tools' package to 'actions'
  ([`9cf4d40`](https://github.com/lt-mayonesa/hexagon/commit/9cf4d408f712cecb1799adb5a284db89a0f801c9))

- **create-tool**: Use config for yaml manipulation
  ([`66fe025`](https://github.com/lt-mayonesa/hexagon/commit/66fe02508e58c17ca733ada414eca6cbee1df381))

- **execute**: Use recommended import method
  ([`c4de3b4`](https://github.com/lt-mayonesa/hexagon/commit/c4de3b4ca66ff6902584505c99d5b99f81124de2))

- **i18n**: Use _ installed as builtin
  ([`d1fe739`](https://github.com/lt-mayonesa/hexagon/commit/d1fe73917dacad08032d64c064ecfb0f691875a2))

- **install**: Correct tool naming
  ([`8d5c497`](https://github.com/lt-mayonesa/hexagon/commit/8d5c497526bf3bdd1294e7c83cf57294d6de545f))

- **packages**: Separate cli and support modules
  ([#19](https://github.com/lt-mayonesa/hexagon/pull/19),
  [`2a05218`](https://github.com/lt-mayonesa/hexagon/commit/2a0521867204aebda615b72c88ab104778651cfc))

- **status**: Use rich status instead of halo
  ([`708d3e3`](https://github.com/lt-mayonesa/hexagon/commit/708d3e3d34f4896a4ff3ffc3f32a96c86acfedea))

- **updates**: Re-group changelog logic ([#85](https://github.com/lt-mayonesa/hexagon/pull/85),
  [`526d168`](https://github.com/lt-mayonesa/hexagon/commit/526d1684c30ddfb184d90f58c1b6bc7c34d3cb5d))

- **updates**: Spinner decorator ([#62](https://github.com/lt-mayonesa/hexagon/pull/62),
  [`2769517`](https://github.com/lt-mayonesa/hexagon/commit/27695178360f9b2755022de0a6c0c3f00cf6065f))

decorate functions with with_spinner to display a spinner for long running processes

### Testing

- E2e execute tool minor fix
  ([`66f681d`](https://github.com/lt-mayonesa/hexagon/commit/66f681da354b4c5f50408a8875bce493ce84ffd3))

- Fix broken tests
  ([`a0ed63b`](https://github.com/lt-mayonesa/hexagon/commit/a0ed63b81b4cf056b339e9948b7a90712d057fa3))

- **e2e**: Add coverage for help module
  ([`2f1f913`](https://github.com/lt-mayonesa/hexagon/commit/2f1f91313a1f97d9e8260c1b0d83e19d181f1a4d))

- **e2e**: Create_new_tool, solves #11 ([#12](https://github.com/lt-mayonesa/hexagon/pull/12),
  [`d540e14`](https://github.com/lt-mayonesa/hexagon/commit/d540e14a38efc974d1610dea18648886bf39ade1))

* test(e2e): create_new_tool, solves #11

- **e2e**: Dynamic line width output assertion
  ([#46](https://github.com/lt-mayonesa/hexagon/pull/46),
  [`c1aece1`](https://github.com/lt-mayonesa/hexagon/commit/c1aece12c313dd973d1909d10a0e28657c4115fb))

* test(e2e): dynamic line width output assertion with max number of lines and line delimiter options

- **e2e**: Execute_tool, python modules and node/bash scripts
  ([#13](https://github.com/lt-mayonesa/hexagon/pull/13),
  [`4501ba4`](https://github.com/lt-mayonesa/hexagon/commit/4501ba461a1bd0be6f2fb41fc617265330b88a7e))

python tools now receive 4 arguments in their main method

- **e2e**: Fix print_help test setup
  ([`fd3b3bf`](https://github.com/lt-mayonesa/hexagon/commit/fd3b3bf7fe2d98e653765b96d05209b6d6ef52ca))

- **e2e**: Fix return code assertion ([#33](https://github.com/lt-mayonesa/hexagon/pull/33),
  [`8a9cea3`](https://github.com/lt-mayonesa/hexagon/commit/8a9cea37df9b9ff41dea737802fed7d4f7799717))

- **e2e**: Improved assertion for cli output ([#7](https://github.com/lt-mayonesa/hexagon/pull/7),
  [`e2404f1`](https://github.com/lt-mayonesa/hexagon/commit/e2404f131f8f0890a92d46cffbb00474f1ec2990))

* test(e2e): improved assertion for cli output

- **e2e**: New spec functions, unified config utils
  ([`4dc6460`](https://github.com/lt-mayonesa/hexagon/commit/4dc6460b132d426882c7b47414a820a3380030df))

- **execute**: Split cases in two due to terminal trimming
  ([#45](https://github.com/lt-mayonesa/hexagon/pull/45),
  [`0ed4ec9`](https://github.com/lt-mayonesa/hexagon/commit/0ed4ec92cc7d8dcbc0ef770b78c5c8322e11448a))

- **install-cli**: Fix broken test
  ([`de720e7`](https://github.com/lt-mayonesa/hexagon/commit/de720e76823a3644bd140cae5d3f6b360b7a9669))

- **tracer**: Tests when trace empty
  ([`ab298dd`](https://github.com/lt-mayonesa/hexagon/commit/ab298dd5aaecc59496950543565a44e8d57c1572))
