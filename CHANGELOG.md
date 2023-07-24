# CHANGELOG



## v0.43.3 (2023-07-24)

### Fix

* fix(update): ignore versions entries with chore types ([`5e063c4`](https://github.com/lt-mayonesa/hexagon/commit/5e063c4d431f7fdde91c6242bccd1c500cb44dbe))

### Refactor

* refactor(dependencies): dry up code ([`b8a843e`](https://github.com/lt-mayonesa/hexagon/commit/b8a843e46fab26953f6949697fa5d772dc2bb229))


## v0.43.2 (2023-07-24)

### Chore

* chore(e2e): 3.7 failing test ([`cb360b0`](https://github.com/lt-mayonesa/hexagon/commit/cb360b0baacd899e527326a0fae75c880640e769))

* chore(e2e): allow to specify multiple yaml ([`5da4d92`](https://github.com/lt-mayonesa/hexagon/commit/5da4d9272cfda5440ea6a55033ddb4dcf6383cc0))

### Fix

* fix(dependencies): handle case when no custom dir present ([`ff7a5e8`](https://github.com/lt-mayonesa/hexagon/commit/ff7a5e8292a1120ec4b053ba516ed752e84cba70))

* fix(errors): handle case when no custom dir present ([`61362ba`](https://github.com/lt-mayonesa/hexagon/commit/61362ba4f251763bca573f7936c75655a6fa50f4))


## v0.43.1 (2023-07-09)

### Chore

* chore(e2e): fix flaky test ([`5a946f7`](https://github.com/lt-mayonesa/hexagon/commit/5a946f7f582d99de73d9be29629f572827f8f32e))

* chore(flake8): remove unused variable ([`09165d1`](https://github.com/lt-mayonesa/hexagon/commit/09165d180b5e6d0a8aea3ee8492f9aaf8e10debf))

* chore: removed unused pipenv-setup (#24) ([`ba91768`](https://github.com/lt-mayonesa/hexagon/commit/ba917681fb7a4decd9b0f50166a1abd7a1f7ce37))

* chore(update): parse test version correctly ([`20f3517`](https://github.com/lt-mayonesa/hexagon/commit/20f35171d3566e5fdbb923492f63fdd24779662f))

* chore(update): revert local imports usage ([`ff32c5b`](https://github.com/lt-mayonesa/hexagon/commit/ff32c5b26f58f3d1ea0e9ff67eeb3ab73f447d45))

* chore(update): don&#39;t use local imports ([`0f5e2a6`](https://github.com/lt-mayonesa/hexagon/commit/0f5e2a6189c87a399b1fe15caaf7d8b59567b090))

* chore(update): handle deprecated package pkg_resources ([`cc63668`](https://github.com/lt-mayonesa/hexagon/commit/cc636681d185878edcf99deb0cecda1c6c09f882))

### Fix

* fix(update): ignore errors when updating ([`2a40c98`](https://github.com/lt-mayonesa/hexagon/commit/2a40c98cb2154123ba4e2d7428b733afdaae8993))

* fix(install): use string instead of posixpath ([`f645906`](https://github.com/lt-mayonesa/hexagon/commit/f64590691f3e7c7d5c1e7bfa073b01c9806c1821))

### Test

* test(e2e): extra ouput validation ([`c71db14`](https://github.com/lt-mayonesa/hexagon/commit/c71db14bb5444c43c5e60a05fd7c53770c5d63e2))

* test(e2e): use no_border theme instead of default ([`b03162b`](https://github.com/lt-mayonesa/hexagon/commit/b03162b7215710d9af46c837d5b79c3a9e764fc7))

* test(e2e): validate more outputs ([`787f329`](https://github.com/lt-mayonesa/hexagon/commit/787f329199d385472a733c028bbdd57dea8bd317))

* test(e2e): output complete log even on errors ([`807d19a`](https://github.com/lt-mayonesa/hexagon/commit/807d19aadc73303c2d5a5af0cd56245dc05ed7ec))

* test(e2e): match output ([`1dcfecc`](https://github.com/lt-mayonesa/hexagon/commit/1dcfeccc31494bed18f162ace8bc72834fc66d4a))

* test(e2e): add bigger timeout ([`0b148e9`](https://github.com/lt-mayonesa/hexagon/commit/0b148e963524f73c853bd255a15266d91646de4d))


## v0.43.0 (2023-05-06)

### Feature

* feat(args): prompt same arg multiple times and trace ([`7a96e23`](https://github.com/lt-mayonesa/hexagon/commit/7a96e23cc8e2c69b6f2e07558bd37041af927830))


## v0.42.1 (2023-05-06)

### Fix

* fix(args): use correct value when tracing ([`f00dac8`](https://github.com/lt-mayonesa/hexagon/commit/f00dac85f2e10621826a9312f5d2eab02271606a))


## v0.42.0 (2023-05-02)

### Feature

* feat(args): add prompt API to hexagon args ([`6cfb88f`](https://github.com/lt-mayonesa/hexagon/commit/6cfb88fc309a303ee234821754b061ae4606404f))


## v0.41.1 (2023-04-13)

### Chore

* chore(test): ignore blank lines when matching outout ([`9607636`](https://github.com/lt-mayonesa/hexagon/commit/96076362b10dbc2f3d9f02440346b460b2ef37f9))

### Fix

* fix(args): apply default type validation when prompting ([`f97911f`](https://github.com/lt-mayonesa/hexagon/commit/f97911faee9d4437d2f92344276a8c69af346270))


## v0.41.0 (2023-04-13)

### Chore

* chore(test): log hexagon spec steps ([`f1a3e00`](https://github.com/lt-mayonesa/hexagon/commit/f1a3e00cd8e8b064a65141d3eee7ca7107fd4a5b))

* chore(dependencies): update to newest versions ([`c1bc52d`](https://github.com/lt-mayonesa/hexagon/commit/c1bc52daae64de2e51da04e60ad15819c3ca366d))

### Feature

* feat(theme): add no_border prompt theme

also simplify e2e tests ([`bb39265`](https://github.com/lt-mayonesa/hexagon/commit/bb39265274507eeac3c47605d41bc0b21d317de1))


## v0.40.0 (2023-04-12)

### Feature

* feat(args): do not validate special characters on args ([`e793175`](https://github.com/lt-mayonesa/hexagon/commit/e79317551d686021d50915c61e25de69d80bf29e))

* feat(args): wrap default value in HexagonArg ([`7d5eae4`](https://github.com/lt-mayonesa/hexagon/commit/7d5eae4da5d56768664968dacab08a5ce64b706a))

### Refactor

* refactor(args): rename Field to Arg ([`b742568`](https://github.com/lt-mayonesa/hexagon/commit/b742568336920d82b7a7b6e319d62e0e1f31951a))

* refactor(args): use positional and optional instances ([`b1f9e61`](https://github.com/lt-mayonesa/hexagon/commit/b1f9e613200fe40b48365984a272046c3f34a0cb))


## v0.39.0 (2023-04-10)

### Feature

* feat(args): apply model validations when prompting ([`86bf096`](https://github.com/lt-mayonesa/hexagon/commit/86bf096817194810d0143bc98bfafad575435115))

* feat(args): prompt for tool arguments from cli_args object

other fixes ([`67d65ab`](https://github.com/lt-mayonesa/hexagon/commit/67d65ab9a4a20cc9b6d7438854cc480decdbbb07))

### Refactor

* refactor(inquirer): hide usage behind prompt

cleanup of tools seed and docker_registry, they will be added to their own repos ([`d68d01c`](https://github.com/lt-mayonesa/hexagon/commit/d68d01c9da08343acba94ca81d170bdb3b2ba938))

* refactor(tracer): store trace object instead of string ([`4c79362`](https://github.com/lt-mayonesa/hexagon/commit/4c793622ceea67fb6373089b536de6859daa5e9f))


## v0.38.1 (2023-04-06)

### Fix

* fix(args): trace all input args and one time only ([`8b69454`](https://github.com/lt-mayonesa/hexagon/commit/8b6945487dddf9d4bb31a916743689e1831ee13b))


## v0.38.0 (2023-04-05)

### Ci

* ci: use github environment files ([`fbffcc3`](https://github.com/lt-mayonesa/hexagon/commit/fbffcc3b0583aad35dc18a7f7515f4446063b6ee))

* ci: adjust workflow naming ([`91e94c3`](https://github.com/lt-mayonesa/hexagon/commit/91e94c3034b5f97b6c17cfeb30469deef28a5785))

### Feature

* feat(execute): when executing script pass tool &amp; env as envvars ([`2c17a33`](https://github.com/lt-mayonesa/hexagon/commit/2c17a332215f1936de97549a450f36aac64cc86a))

### Refactor

* refactor(tracer): handle execute again in tracer ([`a8b11da`](https://github.com/lt-mayonesa/hexagon/commit/a8b11dabd276648bca88d97322e771c6a78067f0))

* refactor: remove dependency from plugins ([`90ab695`](https://github.com/lt-mayonesa/hexagon/commit/90ab69533dd2052fbb4346ca0513a9bf54603dd4))

* refactor: reducing main complexity ([`40969b6`](https://github.com/lt-mayonesa/hexagon/commit/40969b681f1d06780ff24c23ad1581f6a93c01a2))

* refactor: remove logic from hexagon.domain.__init__ ([`e283f88`](https://github.com/lt-mayonesa/hexagon/commit/e283f88db627039705e55b9184c2052210ab0ced))

* refactor: centralize error handling in main catch ([`dd648bc`](https://github.com/lt-mayonesa/hexagon/commit/dd648bc2986a838cf989c1442a3df19a7147d6bd))


## v0.37.0 (2023-04-03)

### Chore

* chore(i18n): fix message id ([`b66d48d`](https://github.com/lt-mayonesa/hexagon/commit/b66d48d47589246df7ae4ea1fdf522df9735c4d7))

### Ci

* ci(report): add comment to PR with tests results ([`865b3cc`](https://github.com/lt-mayonesa/hexagon/commit/865b3cc26bab86396fde855ee15a814c1351a972))

### Feature

* feat(args): show validation error matching hexagon format ([`6027468`](https://github.com/lt-mayonesa/hexagon/commit/6027468e00b645c64b29f08f1313754033971774))


## v0.36.0 (2023-04-02)

### Feature

* feat(args): show help text for tools ([`9e387a7`](https://github.com/lt-mayonesa/hexagon/commit/9e387a7f0872029fd703c0bb87fba35ac6b7aa71))


## v0.35.1 (2023-04-01)

### Fix

* fix(args): handle case when last optional arg has missing value ([`e05004b`](https://github.com/lt-mayonesa/hexagon/commit/e05004bf393ed79bf3a7283fe4d8938aa3a5d236))


## v0.35.0 (2023-04-01)

### Chore

* chore(e2e): always print command output ([`d9a88a6`](https://github.com/lt-mayonesa/hexagon/commit/d9a88a683ef22725189dff7ae2717aa0a6a43e4d))

### Ci

* ci(report): use wildcard for reports ([`ceb4dcd`](https://github.com/lt-mayonesa/hexagon/commit/ceb4dcd9765e24399c6b8083961aea7e4f8f003a))

### Feature

* feat(args): added support for tool args

users define a class Args(ToolArgs) in their python actions that will automagically parse CLI input args specific for this action ([`ebd5443`](https://github.com/lt-mayonesa/hexagon/commit/ebd5443d2d732099765cd7fb869e8cc70818b85e))

### Fix

* fix(args): support extend on python 3.7 ([`e4c0581`](https://github.com/lt-mayonesa/hexagon/commit/e4c0581a75a635dfb43f1a7166e1f0fd023b7a6d))

### Refactor

* refactor(args): rename support module ([`26c3cd5`](https://github.com/lt-mayonesa/hexagon/commit/26c3cd56675484efae39b755f4a7eb52ad09a945))


## v0.34.0 (2023-03-27)

### Chore

* chore(e2e): set terminal COLUMNS size to 200 ([`99b431e`](https://github.com/lt-mayonesa/hexagon/commit/99b431e8408a63cd5ccbb9f2c78a65f50ae96c9f))

* chore: updating directories structure

new structure should be more easy to follow ([`7174bb2`](https://github.com/lt-mayonesa/hexagon/commit/7174bb24221843ed4946bd8f32cb3d663f2eff28))

### Ci

* ci(report): added unit tests junit report ([`6cc05e9`](https://github.com/lt-mayonesa/hexagon/commit/6cc05e9f7b790146f6c674beaea67deb1e946b60))

### Feature

* feat(tracer): add support for optional cli_args ([`a7b5a9d`](https://github.com/lt-mayonesa/hexagon/commit/a7b5a9d9779c3990687db31c83f20393dd552bec))


## v0.33.0 (2023-03-26)

### Chore

* chore: fix flake8 reports ([`29167b5`](https://github.com/lt-mayonesa/hexagon/commit/29167b55c409d5dfc57f0f0c31375ac88755b5f5))

* chore(i18n): update po line references ([`8b35967`](https://github.com/lt-mayonesa/hexagon/commit/8b359677218c25dda69d82a7fe79057a8d42604e))

* chore(test): stub i18n for unit tests ([`5e60597`](https://github.com/lt-mayonesa/hexagon/commit/5e60597a18b1730c5149f760539a2b0685a3be80))

### Feature

* feat(cli-args): pass extra cli args to execution of actions

 - python actions receive a dict, ie: {&#39;foo&#39;: &#39;bar&#39;}
 - command actions receive the extra args as-is, ie: --foo bar ([`528827a`](https://github.com/lt-mayonesa/hexagon/commit/528827a3130abbbd4318846036130f9370ff55f0))

### Refactor

* refactor(cli-args): use argparse for better support ([`d26d33f`](https://github.com/lt-mayonesa/hexagon/commit/d26d33f4335c8be4507d8adede345ec46b4e16d7))

* refactor: use decorator for execute hook ([`ce5d8dc`](https://github.com/lt-mayonesa/hexagon/commit/ce5d8dc5c72f0f6a1b9f229ea02c305902514223))


## v0.32.0 (2023-03-16)

### Chore

* chore(e2e): skip timeout when debugging ([`c5523a9`](https://github.com/lt-mayonesa/hexagon/commit/c5523a9cda1e94b8a4455bae0f3a02afab20eae6))

### Ci

* ci(report): use github token ([`6e78d9c`](https://github.com/lt-mayonesa/hexagon/commit/6e78d9cc107b93f05b05621bb6d81f70421441b1))

### Feature

* feat(options): allow override options at yaml level

let users defines values in cli.options to override some hexagon configurations, ie: update checks, themes, etc.

fixes #2 ([`08f4258`](https://github.com/lt-mayonesa/hexagon/commit/08f425800f4b719cceb3391e59a1965c7f57c856))


## v0.31.0 (2023-03-13)

### Ci

* ci(test): use java-junit reporter ([`057d1b3`](https://github.com/lt-mayonesa/hexagon/commit/057d1b37c182eb925e9dfcba089c03a321204441))

* ci(test): upload test report to github ([`4a76871`](https://github.com/lt-mayonesa/hexagon/commit/4a76871b4b052aae4a28d42b7a9c5415dc9b7c36))

### Feature

* feat(analytics): remove support for tracking ([`e8adefe`](https://github.com/lt-mayonesa/hexagon/commit/e8adefe440294988742d93d7bcd13454b2e03696))


## v0.30.0 (2023-03-12)

### Ci

* ci: update project metadata ([`a7c311d`](https://github.com/lt-mayonesa/hexagon/commit/a7c311dc8e5968102841961d7fa352a4bd263ac6))

* ci(devex): use personal access token ([`4996bc3`](https://github.com/lt-mayonesa/hexagon/commit/4996bc3d902efd1bd64d849f471487fba3f990a6))

### Feature

* feat(messages): show path when installing dependencies ([`b060dcc`](https://github.com/lt-mayonesa/hexagon/commit/b060dcc8b4311dbf03713b0ef76a0056b222cf96))


## v0.29.0 (2023-03-12)

### Chore

* chore(IDE): setup black file watcher correctly ([`d2fa58c`](https://github.com/lt-mayonesa/hexagon/commit/d2fa58cb28464ac536c1e8473e0fd92896d6988d))

* chore: update dependencies (#84)


black was breaking in CI so dependencies needed to be updated ([`e970496`](https://github.com/lt-mayonesa/hexagon/commit/e970496618200f7ff0b2a75e107ddc7455a0547b))

* chore(e2e): missing comma on run command ([`bce20d1`](https://github.com/lt-mayonesa/hexagon/commit/bce20d192ab1c669d8fb281e9dea1ceb528ed562))

* chore(i18n): use MANIFEST for data ([`ba3e5e6`](https://github.com/lt-mayonesa/hexagon/commit/ba3e5e6c9158f77e90c47167a7e866fd40b5ae01))

* chore: fix strings in spanish ([`1ddedf7`](https://github.com/lt-mayonesa/hexagon/commit/1ddedf777509029d8ae33107198740d57d7f5839))

* chore: added open source license ([`4985837`](https://github.com/lt-mayonesa/hexagon/commit/4985837e47ccc501f7bbeb99cb59aed38283e5bd))

* chore(ci): sync TODOs comments with issues ([`3a8020e`](https://github.com/lt-mayonesa/hexagon/commit/3a8020e98b39ffe08835552ea739b7804f02a12c))

* chore: fix flake8 errors ([`c9e067d`](https://github.com/lt-mayonesa/hexagon/commit/c9e067d7e9f60fa648886d7b8bf99f1230f08217))

* chore(create-tool): template tool in english ([`38e996e`](https://github.com/lt-mayonesa/hexagon/commit/38e996ec7a9ffa5a38a1fd773bb1a0d4f3b78500))

* chore: rollback to version 0.8.0 ([`0aa3057`](https://github.com/lt-mayonesa/hexagon/commit/0aa30578f5295e445be0ba5412b9c2334c3c0149))

* chore(ci): use official flake8 action ([`9ac7863`](https://github.com/lt-mayonesa/hexagon/commit/9ac78637ec77f8eca381513d7ac28e85b85c824b))

* chore(ci): fix flake8 action ([`1b8e229`](https://github.com/lt-mayonesa/hexagon/commit/1b8e229ea49c4258fcb8c23488c6a8ab92d11d29))

* chore(ci): lint with github action (#6) ([`9a571aa`](https://github.com/lt-mayonesa/hexagon/commit/9a571aa6dcec2b27707494a449a14b517228c665))

* chore(ci): use version number in README ([`3d6ea08`](https://github.com/lt-mayonesa/hexagon/commit/3d6ea0811544c895d7fc37210bb8ed939f205c77))

* chore(package): pipenv use setup.py install_requires ([`b8f0ec2`](https://github.com/lt-mayonesa/hexagon/commit/b8f0ec25cac4aaeef394d45dc7471e915eea3bae))

* chore(ci): do not release on PR ([`b186229`](https://github.com/lt-mayonesa/hexagon/commit/b186229a0bbec44d1f3ed7290ad1d23c8f5df896))

* chore(ci): release commit subject ([`fdd833d`](https://github.com/lt-mayonesa/hexagon/commit/fdd833d1bcdbcb7003fdd2f6af15bbaf0bc1d70b))

### Ci

* ci(security): use personal access token for release ([`d52be3b`](https://github.com/lt-mayonesa/hexagon/commit/d52be3b197a44601d321adb980f420d5a9f9e6e1))

* ci: update dependencies and workflows ([`4bace03`](https://github.com/lt-mayonesa/hexagon/commit/4bace0396f573d212e332b94dc17a5504c3539a9))

* ci(guidelines): use versions from lockfile ([`794af5b`](https://github.com/lt-mayonesa/hexagon/commit/794af5b045f041b21e9d3482bd1c0c106b9e88a8))

* ci(release): do not pump version in package workflow ([`25164d1`](https://github.com/lt-mayonesa/hexagon/commit/25164d1d2c100988e899bafda6f48ac49347ff07))

* ci(package): use Pipfile.lock for install_requires deps (#66)


also generate a hexagon build in place for e2e tests ([`ad01850`](https://github.com/lt-mayonesa/hexagon/commit/ad0185098546eb689263752b4a1b438a65e10200))

* ci(release): fix indent error ([`2a8269c`](https://github.com/lt-mayonesa/hexagon/commit/2a8269c4b035eccd74b3c7b814f97e311b8e3a5e))

* ci(release): execute release outside matrix ([`45eca58`](https://github.com/lt-mayonesa/hexagon/commit/45eca58c7d0c762ca8830e02d71f7e0fb07c5ae6))

* ci(release): uso de semantic release ([`421177e`](https://github.com/lt-mayonesa/hexagon/commit/421177ee6b40d40063262a8e1dbb58ae18a1911a))

* ci(release): correcciones de packaging ([`c55f35c`](https://github.com/lt-mayonesa/hexagon/commit/c55f35cea1184287cb7211c0b1d39f13883c1b12))

* ci(release): correr con tags ([`1b076ff`](https://github.com/lt-mayonesa/hexagon/commit/1b076ff9263a2ec823cab0929e13f90005c5f7a8))

* ci(release): compilar correctamente tar.gz ([`9f44350`](https://github.com/lt-mayonesa/hexagon/commit/9f4435059b7ae9000b707727933916f366cce6dc))

* ci(release): subir asset de release ([`1165c4a`](https://github.com/lt-mayonesa/hexagon/commit/1165c4a6896ccf36ed39c755fa5bf0547b79e511))

* ci(publish): publicar en repositorio ([`49217de`](https://github.com/lt-mayonesa/hexagon/commit/49217de25a01d829bcc1ffb39245c705072020ad))

* ci(tests): ejecución de tests ([`2219798`](https://github.com/lt-mayonesa/hexagon/commit/2219798abd9bd29783807ccd674db94aa01ce6bd))

* ci(build): agrego action de package ([`f9e8376`](https://github.com/lt-mayonesa/hexagon/commit/f9e8376e97df4c247871ec00f6b170937e95cb01))

### Documentation

* docs: better resolution gif ([`897eeee`](https://github.com/lt-mayonesa/hexagon/commit/897eeee4ed1472ab993a36eadd1408161d2a2317))

* docs: adding gif example to readme ([`e2b4c1b`](https://github.com/lt-mayonesa/hexagon/commit/e2b4c1ba0e082ec998a63ba497dd627022037c1b))

* docs: update README to be compatible with v0.12.0 ([`d25ff3d`](https://github.com/lt-mayonesa/hexagon/commit/d25ff3d59ae072125378bdbb81d2015ad8bc0eb8))

* docs: english, slogan, and reference to template repo ([`9a9fc96`](https://github.com/lt-mayonesa/hexagon/commit/9a9fc96f42d4ea81a57bda822de7c098d31015a6))

* docs: yaml example in readme ([`86c28d1`](https://github.com/lt-mayonesa/hexagon/commit/86c28d126535e3fb6cd229b623666666aa0e1bd3))

* docs(release): correct regex for README version ([`f9b973a`](https://github.com/lt-mayonesa/hexagon/commit/f9b973a514efc0370a32d5b95a515ed461a508c2))

* docs: basic readme content ([`7a82b34`](https://github.com/lt-mayonesa/hexagon/commit/7a82b3490f2b112c9a35fad4a789de1d2341ad69))

* docs(release): version update comment ([`c6a9617`](https://github.com/lt-mayonesa/hexagon/commit/c6a9617e7943adef2095b1a768548c8692cefd67))

### Feature

* feat(action): allow defining action as list of commands ([`fcc20f1`](https://github.com/lt-mayonesa/hexagon/commit/fcc20f1f30a9ebfcbaa50d99ab3a7897d7af07ca))

* feat(dependencies): show status on deps install (#87) ([`f84d00b`](https://github.com/lt-mayonesa/hexagon/commit/f84d00b855e6548ec869252075dc0c9b4289457a))

* feat(install): warn commands dir not in PATH (#86) ([`9b42bd4`](https://github.com/lt-mayonesa/hexagon/commit/9b42bd4bc765112e4d799e4c4ca57c128fddbb10))

* feat: detect and install dependencies (Python, NodeJS) for CLIs (#72)


detect and install dependencies (Python, NodeJS) for CLIs on install and update

closes #71
Co-authored-by: Joaco Campero &lt;joaquin@redb.ee&gt;
Co-authored-by: Joaquin Campero &lt;juacocampero@gmail.com&gt; ([`febdb38`](https://github.com/lt-mayonesa/hexagon/commit/febdb383e442a5e3cbc528e2c80729b72b651da4))

* feat(groups): allow for inline groups in YAML

refactored group loading, so it is done at configuration time instead of execution time ([`d29a587`](https://github.com/lt-mayonesa/hexagon/commit/d29a58748dac4e2a60dc0760d526cf78ed2c1034))

* feat(storage): add get_local_config_dir() function (#79) ([`ec817d2`](https://github.com/lt-mayonesa/hexagon/commit/ec817d2d4b3bfdd962c6a2dc51216e3b0b53c1ca))

* feat(i18n): added EN and ES transltions + CI (#73) ([`7c65e74`](https://github.com/lt-mayonesa/hexagon/commit/7c65e740dd74cc7c0e0bdb2ba75587f185d327d2))

* feat(install-cli): use shell scripts instead of aliases ([`c3d7ed7`](https://github.com/lt-mayonesa/hexagon/commit/c3d7ed76fce7bfae2448554fdb322f777ea5d59d))

* feat: springboot, react, nextjs seeds (#63)

feat: springboot, react, nextjs seeds ([`951b3ab`](https://github.com/lt-mayonesa/hexagon/commit/951b3ab8df92a5cfccc379c0b8cee824dff16cf2))

* feat: plugins and hooks (#61)

* feat: plugins and hooks ([`b7f1c08`](https://github.com/lt-mayonesa/hexagon/commit/b7f1c080129c53fcf28db424a0bcca5630e4febd))

* feat(analytics): log and send hexagon usage events (#57)


events sent:
 - session start
 - tool selected (prompt or args)
 - env selected (prompt or args)
 - action executed
 - session end ([`c096900`](https://github.com/lt-mayonesa/hexagon/commit/c0969009862e1763ac79d5f5c82d5ee110f4ec88))

* feat: options by env variables, local options file or defaults (#52)

* feat: options by env variables, local options file or defaults ([`6687b94`](https://github.com/lt-mayonesa/hexagon/commit/6687b94a53723f56fb683d53ad26c1a64dd3d025))

* feat: nested tools, for grouping and organizing (#54)

* feat: nested tools, for grouping and organizing ([`b5831fd`](https://github.com/lt-mayonesa/hexagon/commit/b5831fdc4f69a6765973f1f5ce1a41ea58d8218c))

* feat: auto-update for clis (#49)

* feat: auto-update for clis ([`a03d3e0`](https://github.com/lt-mayonesa/hexagon/commit/a03d3e00c27a39e72298e3f5979711162ded6f1d))

* feat(execute): display action errors nicely to user (#43)


Print errors nicely when python action import fails due to dependency errors, or when fails executing due to user errors in script. ([`b8ab97f`](https://github.com/lt-mayonesa/hexagon/commit/b8ab97f377bb10fe7c5533c5bbdbbd19938a74b1))

* feat(updates): hexagon auto update (#35)

periodically check the latest version of hexagon and suggest for updates

relates to #34 ([`16b93ff`](https://github.com/lt-mayonesa/hexagon/commit/16b93ffab29aa817c22b4a9b06e6dda43cc54fc7))

* feat(yaml): show a more precise error to users (#27)


closes #20 ([`b635964`](https://github.com/lt-mayonesa/hexagon/commit/b635964789a54006f3f3b4dc31196940487b687f))

* feat: define tools &amp; envs as lists (#26) ([`4db03b4`](https://github.com/lt-mayonesa/hexagon/commit/4db03b4e279bf2c82f6c9e8af8265026ea6e25c6))

* feat(domain): map YAML to pydantic BaseModel (#24) ([`727a09a`](https://github.com/lt-mayonesa/hexagon/commit/727a09a01f11c34b1225fdcab609b02b2ffbff09))

* feat(execute): command actions, closes #22 (#23)

* feat(execute): command actions, closes #22 ([`26a9e05`](https://github.com/lt-mayonesa/hexagon/commit/26a9e051b497354c55177398f95ef98b0b4149bb))

* feat(support): storage api, closes #17 (#21)

* feat(support): storage api, closes #17 ([`f8cc5b3`](https://github.com/lt-mayonesa/hexagon/commit/f8cc5b374df56c084c2b1cc48ba0a35c44c6a46e))

* feat(styles): basic support for hexagon themes (#14) ([`b5dd966`](https://github.com/lt-mayonesa/hexagon/commit/b5dd966a221cab477e33adec27fb54fdfc6efefb))

* feat(execute): execute action with extension

let users define an action with other scripting languages, for now only .js and .sh are supported ([`fe622a8`](https://github.com/lt-mayonesa/hexagon/commit/fe622a8942d91eb3c2f5c9cbe88d1aac22f1ea0f))

* feat(internal-tools): create a new tool

prompt the user for parameters and register the new tool in the YAML and create the python modules if action is new ([`dfc13aa`](https://github.com/lt-mayonesa/hexagon/commit/dfc13aacf77ec17ba735a519dd4bfbce29047731))

* feat(config): only show install cli when no config ([`9413f99`](https://github.com/lt-mayonesa/hexagon/commit/9413f99ffa23f562f68acddfe99c73e817e74e3e))

* feat(config): custom tools dir relative to YAML ([`fe3e26b`](https://github.com/lt-mayonesa/hexagon/commit/fe3e26bd3598ece02e9fd06ae4397b14edce6947))

* feat(prompt): sort tools by type ([`ef71eae`](https://github.com/lt-mayonesa/hexagon/commit/ef71eae1e2b5bb0b7b996efa5a1c694b52f31235))

* feat(custom-tool): allow projects to register custom tools

hexagon will check for cli.custom_tools_dir in config YAML, if exists it will load that directory as a path for python modules. ([`1cac9ca`](https://github.com/lt-mayonesa/hexagon/commit/1cac9ca80e369f9c05c1dcc3363386d4af0d6828))

* feat: handle keyboard interrupt gracefully ([`a65daa2`](https://github.com/lt-mayonesa/hexagon/commit/a65daa26c3de305a2bacafe7f7a64f9295914c94))

* feat(install): install custom cli from YAML ([`cb25d68`](https://github.com/lt-mayonesa/hexagon/commit/cb25d680fa2af6448a79e61631542dabc08991a9))

* feat(envs): make tool.envs optional

in tool definition envs dict is now optional ([`efeec06`](https://github.com/lt-mayonesa/hexagon/commit/efeec064404830ca33c6b4751f55455190c6b9e2))

* feat: project setup ([`d28bcc9`](https://github.com/lt-mayonesa/hexagon/commit/d28bcc95017ea6214523bdbd03d3b7f78dfb3fc6))

### Fix

* fix(install-cli): only store bin_path if prompted ([`32dbc6c`](https://github.com/lt-mayonesa/hexagon/commit/32dbc6c0c5081b1a4db589f49e3b5fa8498c9a74))

* fix: print help gaps

do not add gap after description if it&#39;s the last in the list

solves #32 ([`e130331`](https://github.com/lt-mayonesa/hexagon/commit/e130331f4e347c57e0bcb246b476063452c15911))

* fix(execute-again): show command aliases correctly

do a recursive search of tools and envs to find the aliases
applied black formatting ([`922e554`](https://github.com/lt-mayonesa/hexagon/commit/922e5547c214f3819c9159eea174da28c3bd3856))

* fix(action): validate action is valid module identifier (#78) ([`e583078`](https://github.com/lt-mayonesa/hexagon/commit/e5830787b96432c2c142f96a5850089c5958ace9))

* fix(create-tool): README lost during package (#77) ([`b7238cd`](https://github.com/lt-mayonesa/hexagon/commit/b7238cddbcc07c09e5e20eb10d9e5dd7f396516f))

* fix(i18n): missing translation strings (#76)


use str.format so all strings are translated correctly ([`97a1068`](https://github.com/lt-mayonesa/hexagon/commit/97a1068ec8c4eb771466676a84215a0b458fc84c))

* fix(i18n): search local and system dirs

lookup is done:
 1. HEXAGON_LOCALES_DIR if present
 2. local install dir (~/.local)
 4. system install dir (/usr/local)
 6. default gettext lookup dir or fallback ([`af62986`](https://github.com/lt-mayonesa/hexagon/commit/af6298632e78c289f2bf50b855a63a93526efd89))

* fix(yaml): print YAML path ([`bfc60ae`](https://github.com/lt-mayonesa/hexagon/commit/bfc60ae1b60f2664934f999176067dfe374b2015))

* fix(alias): source new aliases (#64)


when creating an OS alias source the file so the user has the alias on path ([`c13f59b`](https://github.com/lt-mayonesa/hexagon/commit/c13f59b454e7c3df45efd3c3267eb0ed32cad1a8))

* fix(analytics): switch user_id and client_id scope ([`6718c7c`](https://github.com/lt-mayonesa/hexagon/commit/6718c7cb94c8a2693d795cfc97339bf6dd9a6678))

* fix(analytics): register user_id and client_id ([`18a621e`](https://github.com/lt-mayonesa/hexagon/commit/18a621ed1b6998644ff5bcdb59218393fc7e726f))

* fix: changelog in hexagon update (#48) ([`c6ab57d`](https://github.com/lt-mayonesa/hexagon/commit/c6ab57de27d3d0f8d4d441e198f273b0cd204554))

* fix: added packaging to dependencies (#44) ([`6b5ddec`](https://github.com/lt-mayonesa/hexagon/commit/6b5ddec86d53ca0f8d64f3f3938f959a084ae375))

* fix: hexagon auto-update (#42) ([`2720c6a`](https://github.com/lt-mayonesa/hexagon/commit/2720c6a1d1e1a2ecb2682244702a3b313a1a9a0d))

* fix(execute): use subprocess shell=True (#38)


execute commands spawning an intermediate shell process (shell=True) for a more native experience. Also use sh instead of bash as default shell

fixes #37 ([`6d5e1e8`](https://github.com/lt-mayonesa/hexagon/commit/6d5e1e8e2e6ce62ca15acbf9d002d3ae6d0881ef))

* fix(yaml): handle error for None values ([`33300c6`](https://github.com/lt-mayonesa/hexagon/commit/33300c6463ab7f0accdccf0b46ed7fb96be64ac4))

* fix: simplify always true cli.command ([`c72de85`](https://github.com/lt-mayonesa/hexagon/commit/c72de855b7f8a0e236a9ea100d0e2662f8d90895))

* fix(last-command): store last command whe tool executed directly ([`1f6c887`](https://github.com/lt-mayonesa/hexagon/commit/1f6c8875317245b599b18063420650277d9d27b8))

* fix(help): help expecting dict crashes ([`cf86f99`](https://github.com/lt-mayonesa/hexagon/commit/cf86f99c56e9c5a4affe426021b3230ef342d99f))

* fix(execute): pass env object correctly ([`86bbc68`](https://github.com/lt-mayonesa/hexagon/commit/86bbc689001339f0bfc128b25520244ed7f966ec))

* fix(e2e): refactored tests, improved output assert message (#18) ([`fa41c0d`](https://github.com/lt-mayonesa/hexagon/commit/fa41c0d315e1c91f84421c5c0a0fb36ac37855c3))

* fix(create-tool): __templates dir and custom tools path (#9)

 - During setup configuration.custom_tools_path is handled as absolute or relative to YAML
 - HEXAGON_CONFIG_FILE .yaml can now take any name
 - __templates dir takes into account *.md files
 - e2e excluded from dist ([`5ebde69`](https://github.com/lt-mayonesa/hexagon/commit/5ebde697b840e5da0ea62341ef22831ecc53a50d))

* fix(save-alias): bash on fresh install (#8)



Co-authored-by: Joaco Campero &lt;joaquin@redb.ee&gt; ([`1754d2c`](https://github.com/lt-mayonesa/hexagon/commit/1754d2c02fde3231a142bc2fa51c344eef390e37))

* fix(create-tool): templates directory not published

use os.path.join on create_new_tool ([`0f1e85c`](https://github.com/lt-mayonesa/hexagon/commit/0f1e85c45969d1f1f5cd7ab9dbb0b4018f9a8243))

* fix(tracer): do not print alias for internal tools ([`5d798fe`](https://github.com/lt-mayonesa/hexagon/commit/5d798fe1d49b12b36bcf74decc1765468c888422))

* fix(save-alias): create aliases file if does not exist ([`9055055`](https://github.com/lt-mayonesa/hexagon/commit/9055055c8def45fc1b84c5b13388be50e259f86a))

* fix(execute): run install_cli and other internal tools (#2) ([`71cc90b`](https://github.com/lt-mayonesa/hexagon/commit/71cc90b9493332825f78163854422db5d2ec493d))

* fix(wax): make classifier optional ([`4e8ff5b`](https://github.com/lt-mayonesa/hexagon/commit/4e8ff5bce035883b49a21f062c4a543529983f69))

* fix(create-tool): change ordering of YAML key insert ([`1ce6024`](https://github.com/lt-mayonesa/hexagon/commit/1ce6024b06f6b6cfbf0b0af8db6d6703a79efd35))

* fix(help): support tools with no long_name ([`46c0f89`](https://github.com/lt-mayonesa/hexagon/commit/46c0f896dfb63288b3662b8d08499c6c66998b47))

* fix(wax): show classifier when no long_name ([`bc8a485`](https://github.com/lt-mayonesa/hexagon/commit/bc8a485ced377d6ddd78ae7617a6fc1f6d2ad889))

* fix(execute): fail with custom message when action not found ([`5ea46f2`](https://github.com/lt-mayonesa/hexagon/commit/5ea46f21aa69dfd5de615d67ac823034b6854ac4))

* fix: allow for tools with no alias ([`eb25e89`](https://github.com/lt-mayonesa/hexagon/commit/eb25e8976581bc9f39852b93444c91b6a074210f))

* fix(install): wrong action definition for tool install ([`425dfd3`](https://github.com/lt-mayonesa/hexagon/commit/425dfd349da6c60361ef69839752126632c67bd7))

* fix(help): optional alias

do not print &#34;(alias)&#34; in help when tool has none ([`3cf1f6a`](https://github.com/lt-mayonesa/hexagon/commit/3cf1f6a46276468fc7a9ae5bbb4445ff4f544d11))

### Refactor

* refactor(updates): re-group changelog logic (#85) ([`526d168`](https://github.com/lt-mayonesa/hexagon/commit/526d1684c30ddfb184d90f58c1b6bc7c34d3cb5d))

* refactor(i18n): use _ installed as builtin ([`d1fe739`](https://github.com/lt-mayonesa/hexagon/commit/d1fe73917dacad08032d64c064ecfb0f691875a2))

* refactor(status): use rich status instead of halo ([`708d3e3`](https://github.com/lt-mayonesa/hexagon/commit/708d3e3d34f4896a4ff3ffc3f32a96c86acfedea))

* refactor(updates): spinner decorator (#62)


decorate functions with with_spinner to display a spinner for long running processes ([`2769517`](https://github.com/lt-mayonesa/hexagon/commit/27695178360f9b2755022de0a6c0c3f00cf6065f))

* refactor(actions): rename &#39;tools&#39; package to &#39;actions&#39; ([`9cf4d40`](https://github.com/lt-mayonesa/hexagon/commit/9cf4d408f712cecb1799adb5a284db89a0f801c9))

* refactor: tool-env selection, follow up to #26, closes #28 (#29) ([`e42fa36`](https://github.com/lt-mayonesa/hexagon/commit/e42fa36064e0133825d656de0bd55bf48aade684))

* refactor(packages): separate cli and support modules (#19) ([`2a05218`](https://github.com/lt-mayonesa/hexagon/commit/2a0521867204aebda615b72c88ab104778651cfc))

* refactor(create-tool): use config for yaml manipulation ([`66fe025`](https://github.com/lt-mayonesa/hexagon/commit/66fe02508e58c17ca733ada414eca6cbee1df381))

* refactor(execute): use recommended import method ([`c4de3b4`](https://github.com/lt-mayonesa/hexagon/commit/c4de3b4ca66ff6902584505c99d5b99f81124de2))

* refactor(install): correct tool naming ([`8d5c497`](https://github.com/lt-mayonesa/hexagon/commit/8d5c497526bf3bdd1294e7c83cf57294d6de545f))

### Style

* style(black): automate code linting with black (#10) ([`5372299`](https://github.com/lt-mayonesa/hexagon/commit/53722998c9649f5bf555edcfc7d12a9a06e57c4c))

### Test

* test: fix broken tests ([`a0ed63b`](https://github.com/lt-mayonesa/hexagon/commit/a0ed63b81b4cf056b339e9948b7a90712d057fa3))

* test: e2e execute tool minor fix ([`66f681d`](https://github.com/lt-mayonesa/hexagon/commit/66f681da354b4c5f50408a8875bce493ce84ffd3))

* test(e2e): dynamic line width output assertion (#46)

* test(e2e): dynamic line width output assertion with max number of lines and line delimiter options ([`c1aece1`](https://github.com/lt-mayonesa/hexagon/commit/c1aece12c313dd973d1909d10a0e28657c4115fb))

* test(execute): split cases in two due to terminal trimming (#45) ([`0ed4ec9`](https://github.com/lt-mayonesa/hexagon/commit/0ed4ec92cc7d8dcbc0ef770b78c5c8322e11448a))

* test(install-cli): fix broken test ([`de720e7`](https://github.com/lt-mayonesa/hexagon/commit/de720e76823a3644bd140cae5d3f6b360b7a9669))

* test(e2e): fix return code assertion (#33) ([`8a9cea3`](https://github.com/lt-mayonesa/hexagon/commit/8a9cea37df9b9ff41dea737802fed7d4f7799717))

* test(e2e): fix print_help test setup ([`fd3b3bf`](https://github.com/lt-mayonesa/hexagon/commit/fd3b3bf7fe2d98e653765b96d05209b6d6ef52ca))

* test(e2e): add coverage for help module ([`2f1f913`](https://github.com/lt-mayonesa/hexagon/commit/2f1f91313a1f97d9e8260c1b0d83e19d181f1a4d))

* test(e2e): new spec functions, unified config utils ([`4dc6460`](https://github.com/lt-mayonesa/hexagon/commit/4dc6460b132d426882c7b47414a820a3380030df))

* test(e2e): execute_tool, python modules and node/bash scripts (#13)

python tools now receive 4 arguments in their main method ([`4501ba4`](https://github.com/lt-mayonesa/hexagon/commit/4501ba461a1bd0be6f2fb41fc617265330b88a7e))

* test(e2e): create_new_tool, solves #11 (#12)

* test(e2e): create_new_tool, solves #11 ([`d540e14`](https://github.com/lt-mayonesa/hexagon/commit/d540e14a38efc974d1610dea18648886bf39ade1))

* test(e2e): improved assertion for cli output (#7)

* test(e2e): improved assertion for cli output ([`e2404f1`](https://github.com/lt-mayonesa/hexagon/commit/e2404f131f8f0890a92d46cffbb00474f1ec2990))

* test(tracer): tests when trace empty ([`ab298dd`](https://github.com/lt-mayonesa/hexagon/commit/ab298dd5aaecc59496950543565a44e8d57c1572))

### Unknown

* Update hexagon spinner (#47)

* fix: update hexagon spinner ([`2e1e4cd`](https://github.com/lt-mayonesa/hexagon/commit/2e1e4cd43d785a7b664360ad49533ed3e0af09d8))

* Pruebas e2e (#3)

test(e2e):e2e tests setup ([`a8d5c97`](https://github.com/lt-mayonesa/hexagon/commit/a8d5c97d93927d3c1e0502c7f6a6bfc44bec8e41))
