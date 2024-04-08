# Changelog

<!--next-version-placeholder-->

## v0.58.1 (2024-04-08)

### Fix

* **install:** Make bin_path optional arg ([`741044a`](https://github.com/lt-mayonesa/hexagon/commit/741044a2244770c18b66dfd972bc1220cab910ad))

## v0.58.0 (2024-03-30)

### Feature

* **logger:** Add file & panel log APIs ([#80](https://github.com/lt-mayonesa/hexagon/issues/80)) ([`5e4a2db`](https://github.com/lt-mayonesa/hexagon/commit/5e4a2dbb9328d43a5921a51cc3b0ed42c6abbea6))

### Documentation

* **readme:** Install from pypi ([`6968d45`](https://github.com/lt-mayonesa/hexagon/commit/6968d45b54222086f940f9b635771214c0352bd5))

## v0.57.0 (2024-03-02)

### Feature

* **prompt:** Allow passing callable to skip_trace ([`608d5dd`](https://github.com/lt-mayonesa/hexagon/commit/608d5dd99ee059bdf11528a661b501e70d186a48))

## v0.56.0 (2024-02-19)

### Feature

* **replay:** Allow replaying last command executed ([#75](https://github.com/lt-mayonesa/hexagon/issues/75)) ([`7449404`](https://github.com/lt-mayonesa/hexagon/commit/7449404463ae7287989240b447eede6094ccd6ef))

## v0.55.0 (2024-02-18)

### Feature

* **hexagon:** Added get-json-schema tool ([#73](https://github.com/lt-mayonesa/hexagon/issues/73)) ([`5377fbf`](https://github.com/lt-mayonesa/hexagon/commit/5377fbfaa1d4a82f16ae9d8a08cce740adb883b2))

## v0.54.0 (2024-02-18)

### Feature

* **prompt:** Allow specifying glob_extra_choices for file glop prompts ([#71](https://github.com/lt-mayonesa/hexagon/issues/71)) ([`d2fc570`](https://github.com/lt-mayonesa/hexagon/commit/d2fc570c5b4a4f660c0eeb40f9dc8da00eb01ad5))

## v0.53.2 (2023-11-13)

### Fix

* **i18n:** Validate existing paths ([`0b268e6`](https://github.com/lt-mayonesa/hexagon/commit/0b268e6a96e1886a1dd446b2f7fe483bdcc3adda))

## v0.53.1 (2023-11-12)

### Fix

* **help:** Don't print usage twice ([`603af0f`](https://github.com/lt-mayonesa/hexagon/commit/603af0fb1531bed4475b81c8d9175c1b53d4867e))

## v0.53.0 (2023-11-12)

### Feature

* **args:** Allow passing boolean as key only ([#69](https://github.com/lt-mayonesa/hexagon/issues/69)) ([`2174082`](https://github.com/lt-mayonesa/hexagon/commit/2174082a4b2e0c5b210c6d2244d9eeea2775a31e))

## v0.52.1 (2023-11-09)

### Fix

* **tracer:** Lowercase traced bool ([`a19f109`](https://github.com/lt-mayonesa/hexagon/commit/a19f109e359623a6f8fe94315f1584dd03a63225))
* **prompt:** Show correct confirm dialog ([`c36bbb1`](https://github.com/lt-mayonesa/hexagon/commit/c36bbb12b6a76ee14abc4989ea90c18ec1857a78))

## v0.52.0 (2023-11-06)

### Feature

* **prompt:** Allow defining prompt_default ([#66](https://github.com/lt-mayonesa/hexagon/issues/66)) ([`8266843`](https://github.com/lt-mayonesa/hexagon/commit/8266843ecf9766de20435c1cbcac713026113195))

## v0.51.3 (2023-11-05)

### Fix

* **i18n:** Default to EN even if nothing found ([`685bdef`](https://github.com/lt-mayonesa/hexagon/commit/685bdefd14b159d39f2a5106e5d26723e4e867ed))

## v0.51.2 (2023-10-30)

### Fix

* **tracer:** Trace enum values correctly ([#63](https://github.com/lt-mayonesa/hexagon/issues/63)) ([`38475bb`](https://github.com/lt-mayonesa/hexagon/commit/38475bbb50bf252285e6c62eaab2768c15e974da))

## v0.51.1 (2023-10-29)

### Fix

* **tracer:** Execute again display enum correctly ([`50d575a`](https://github.com/lt-mayonesa/hexagon/commit/50d575aed1d10516fc531e0f4946ab2655086e5c))

## v0.51.0 (2023-10-29)

### Feature

* **prompt:** CTRL+P create directory if not exists ([#61](https://github.com/lt-mayonesa/hexagon/issues/61)) ([`05002ac`](https://github.com/lt-mayonesa/hexagon/commit/05002ac13c5f492004a8edc99d4a69df965c3ab5))

## v0.50.0 (2023-10-28)

### Feature

* **execute:** Arg replacement ([`f459405`](https://github.com/lt-mayonesa/hexagon/commit/f459405d306847167b91d8f3257882d43de3a854))

## v0.49.2 (2023-09-27)

### Fix

* **prompt:** Handle enum default when searchable ([#56](https://github.com/lt-mayonesa/hexagon/issues/56)) ([`12e9987`](https://github.com/lt-mayonesa/hexagon/commit/12e9987739c74f2032d5e4251f49debf6d9cdcaf))

## v0.49.1 (2023-09-24)

### Fix

* **execute:** Handle script relative paths correctly ([`9399df5`](https://github.com/lt-mayonesa/hexagon/commit/9399df5070716d0b7642b915b82016a30c95d78a))
* **execute:** Pass first arg to script when env not present ([`6cbf4c0`](https://github.com/lt-mayonesa/hexagon/commit/6cbf4c09c69b4b9894dd1ccbb979c54e11b822ca))

## v0.49.0 (2023-09-20)

### Feature

* **plugins:** Allow to register plugins from multiple sources ([#52](https://github.com/lt-mayonesa/hexagon/issues/52)) ([`2c42112`](https://github.com/lt-mayonesa/hexagon/commit/2c42112cb8df4aa9d3a7436439b6375179f5a777))

## v0.48.4 (2023-09-20)

### Fix

* **i18n:** Add messages for number & secret hints ([#51](https://github.com/lt-mayonesa/hexagon/issues/51)) ([`220fe6c`](https://github.com/lt-mayonesa/hexagon/commit/220fe6ce6142bb68914ea28a0edd4e704b535260))

## v0.48.3 (2023-09-18)

### Fix

* **hooks:** Terminate background hooks ([#50](https://github.com/lt-mayonesa/hexagon/issues/50)) ([`f7f762f`](https://github.com/lt-mayonesa/hexagon/commit/f7f762f4558b5633d348d2a370a8f2941e8e4dde))

## v0.48.2 (2023-09-13)

### Fix

* **tracer:** Store Enum value ([#49](https://github.com/lt-mayonesa/hexagon/issues/49)) ([`2b283d2`](https://github.com/lt-mayonesa/hexagon/commit/2b283d2838521f2bb96239f6070b73d9d063026e))

## v0.48.1 (2023-09-12)

### Fix

* **prompt:** Dont set default on inquiry type Enum ([`c604507`](https://github.com/lt-mayonesa/hexagon/commit/c604507fe43320430685527117fb911f51381834))

## v0.48.0 (2023-09-12)

### Feature

* **prompt:** Support ints, floats, paths globs, secrets ([#46](https://github.com/lt-mayonesa/hexagon/issues/46)) ([`60e39fc`](https://github.com/lt-mayonesa/hexagon/commit/60e39fc200fcd197e96e44960ba7b45d448a358a))

## v0.47.1 (2023-08-07)

### Fix

* **execute:** Pass user PATH to scripts execution ([`6c6157c`](https://github.com/lt-mayonesa/hexagon/commit/6c6157c667563584281dbd553ed9eae8a1904add))

## v0.47.0 (2023-08-07)

### Feature

* Re-organized packages ([#44](https://github.com/lt-mayonesa/hexagon/issues/44)) ([`f90bd8e`](https://github.com/lt-mayonesa/hexagon/commit/f90bd8e8e02de987ccaf6c91003c509cd89ba873))

## v0.46.2 (2023-08-06)

### Fix

* **update:** Update current git branch ([`7417c4d`](https://github.com/lt-mayonesa/hexagon/commit/7417c4dc50a05caaf109696363407d78746fa90f))

## v0.46.1 (2023-08-06)

### Fix

* **logger:** Check status level on status_aware ([`d893dcb`](https://github.com/lt-mayonesa/hexagon/commit/d893dcbc9f437efdf12ef758ae4dd84afd32071a))

## v0.46.0 (2023-08-06)

### Feature

* **prompt:** Show help texts for prompts ([`0c4ec1f`](https://github.com/lt-mayonesa/hexagon/commit/0c4ec1f96028ae45f262c6bcb3d6728149d2d387))
* **args:** Allow to set prompt instruction message ([#36](https://github.com/lt-mayonesa/hexagon/issues/36)) ([`b79ee9a`](https://github.com/lt-mayonesa/hexagon/commit/b79ee9affc456d94e3df07e01880d08f31899c5f))

## v0.45.0 (2023-07-29)

### Feature

* **status:** Allow to nest statuses and prompt inside ([`d6e194e`](https://github.com/lt-mayonesa/hexagon/commit/d6e194e4c4ee9e352d9f7e484a7ce4d08dc9bcc6))

### Fix

* **groups:** Display go back icon correctly ([`b214adc`](https://github.com/lt-mayonesa/hexagon/commit/b214adcf3d516472717b0a022ea9ca4199cda0bd))
* **update:** Show status correctly when updating ([`169dc99`](https://github.com/lt-mayonesa/hexagon/commit/169dc998bdf4cfdfb006e776c7f83b683bd7e858))

## v0.44.0 (2023-07-29)

### Feature

* **args:** Allow to specify default in prompt ([`69303d3`](https://github.com/lt-mayonesa/hexagon/commit/69303d3ad38c110a0ff75807dcf580ef2af10fea))

### Fix

* **install:** Use correct path for dependency install ([`f792d01`](https://github.com/lt-mayonesa/hexagon/commit/f792d0121f1cc20f0e95eafe013bfedc325ce58f))
* **dependencies:** Show progress by individual install ([`c0a0f2e`](https://github.com/lt-mayonesa/hexagon/commit/c0a0f2ed15fa186a4dd05c9d196e4467497f7394))
* **dependencies:** Use faster tree search ([`493aa54`](https://github.com/lt-mayonesa/hexagon/commit/493aa542dfa703b08a553008eedeae2a7a616fe6))

### Documentation

* **setup:** Update local setup instractions ([`12a7da7`](https://github.com/lt-mayonesa/hexagon/commit/12a7da732aabb517e1be83487b5e624fa656dfc8))
* Rollback changelog ([`eee2034`](https://github.com/lt-mayonesa/hexagon/commit/eee2034442be6b9410a2866a58b3f0b1d9261e88))

## v0.42.0 (2023-07-25)

### Fix

* **release:** Rollback to v7.34.6 ([`372fa02`](https://github.com/lt-mayonesa/hexagon/commit/372fa0256fde3e6c1d6ae15ec4a69a1e84aa6e71))
* **release:** Empty change to trigger new release ([`f4d7492`](https://github.com/lt-mayonesa/hexagon/commit/f4d7492263672d3816f2f9e5fae9ae85cf7c2669))
* **update:** Ignore versions entries with chore types ([`5e063c4`](https://github.com/lt-mayonesa/hexagon/commit/5e063c4d431f7fdde91c6242bccd1c500cb44dbe))
* **dependencies:** Handle case when no custom dir present ([`ff7a5e8`](https://github.com/lt-mayonesa/hexagon/commit/ff7a5e8292a1120ec4b053ba516ed752e84cba70))
* **errors:** Handle case when no custom dir present ([`61362ba`](https://github.com/lt-mayonesa/hexagon/commit/61362ba4f251763bca573f7936c75655a6fa50f4))

## v0.43.1 (2023-07-09)

### Fix

* **update:** Ignore errors when updating ([`2a40c98`](https://github.com/lt-mayonesa/hexagon/commit/2a40c98cb2154123ba4e2d7428b733afdaae8993))
* **install:** Use string instead of posixpath ([`f645906`](https://github.com/lt-mayonesa/hexagon/commit/f64590691f3e7c7d5c1e7bfa073b01c9806c1821))

## v0.43.0 (2023-05-06)
### Feature
* **args:** Prompt same arg multiple times and trace ([`7a96e23`](https://github.com/lt-mayonesa/hexagon/commit/7a96e23cc8e2c69b6f2e07558bd37041af927830))

## v0.42.1 (2023-05-06)
### Fix
* **args:** Use correct value when tracing ([`f00dac8`](https://github.com/lt-mayonesa/hexagon/commit/f00dac85f2e10621826a9312f5d2eab02271606a))

## v0.42.0 (2023-05-02)
### Feature
* **args:** Add prompt API to hexagon args ([`6cfb88f`](https://github.com/lt-mayonesa/hexagon/commit/6cfb88fc309a303ee234821754b061ae4606404f))

## v0.41.1 (2023-04-13)
### Fix
* **args:** Apply default type validation when prompting ([`f97911f`](https://github.com/lt-mayonesa/hexagon/commit/f97911faee9d4437d2f92344276a8c69af346270))

## v0.41.0 (2023-04-13)
### Feature
* **theme:** Add no_border prompt theme ([`bb39265`](https://github.com/lt-mayonesa/hexagon/commit/bb39265274507eeac3c47605d41bc0b21d317de1))

## v0.40.0 (2023-04-12)
### Feature
* **args:** Do not validate special characters on args ([`e793175`](https://github.com/lt-mayonesa/hexagon/commit/e79317551d686021d50915c61e25de69d80bf29e))
* **args:** Wrap default value in HexagonArg ([`7d5eae4`](https://github.com/lt-mayonesa/hexagon/commit/7d5eae4da5d56768664968dacab08a5ce64b706a))

## v0.39.0 (2023-04-10)
### Feature
* **args:** Apply model validations when prompting ([`86bf096`](https://github.com/lt-mayonesa/hexagon/commit/86bf096817194810d0143bc98bfafad575435115))
* **args:** Prompt for tool arguments from cli_args object ([`67d65ab`](https://github.com/lt-mayonesa/hexagon/commit/67d65ab9a4a20cc9b6d7438854cc480decdbbb07))

## v0.38.1 (2023-04-06)
### Fix
* **args:** Trace all input args and one time only ([`8b69454`](https://github.com/lt-mayonesa/hexagon/commit/8b6945487dddf9d4bb31a916743689e1831ee13b))

## v0.38.0 (2023-04-05)
### Feature
* **execute:** When executing script pass tool & env as envvars ([`2c17a33`](https://github.com/lt-mayonesa/hexagon/commit/2c17a332215f1936de97549a450f36aac64cc86a))

## v0.37.0 (2023-04-03)
### Feature
* **args:** Show validation error matching hexagon format ([`6027468`](https://github.com/lt-mayonesa/hexagon/commit/6027468e00b645c64b29f08f1313754033971774))

## v0.36.0 (2023-04-02)
### Feature
* **args:** Show help text for tools ([`9e387a7`](https://github.com/lt-mayonesa/hexagon/commit/9e387a7f0872029fd703c0bb87fba35ac6b7aa71))

## v0.35.1 (2023-04-01)
### Fix
* **args:** Handle case when last optional arg has missing value ([`e05004b`](https://github.com/lt-mayonesa/hexagon/commit/e05004bf393ed79bf3a7283fe4d8938aa3a5d236))

## v0.35.0 (2023-04-01)
### Feature
* **args:** Added support for tool args ([`ebd5443`](https://github.com/lt-mayonesa/hexagon/commit/ebd5443d2d732099765cd7fb869e8cc70818b85e))

### Fix
* **args:** Support extend on python 3.7 ([`e4c0581`](https://github.com/lt-mayonesa/hexagon/commit/e4c0581a75a635dfb43f1a7166e1f0fd023b7a6d))

## v0.34.0 (2023-03-27)
### Feature
* **tracer:** Add support for optional cli_args ([`a7b5a9d`](https://github.com/lt-mayonesa/hexagon/commit/a7b5a9d9779c3990687db31c83f20393dd552bec))

## v0.33.0 (2023-03-26)
### Feature
* **cli-args:** Pass extra cli args to execution of actions ([`528827a`](https://github.com/lt-mayonesa/hexagon/commit/528827a3130abbbd4318846036130f9370ff55f0))

## v0.32.0 (2023-03-16)
### Feature
* **options:** Allow override options at yaml level ([`08f4258`](https://github.com/lt-mayonesa/hexagon/commit/08f425800f4b719cceb3391e59a1965c7f57c856))

## v0.31.0 (2023-03-13)
### Feature
* **analytics:** Remove support for tracking ([`e8adefe`](https://github.com/lt-mayonesa/hexagon/commit/e8adefe440294988742d93d7bcd13454b2e03696))

## v0.30.0 (2023-03-12)
### Feature
* **messages:** Show path when installing dependencies ([`b060dcc`](https://github.com/lt-mayonesa/hexagon/commit/b060dcc8b4311dbf03713b0ef76a0056b222cf96))

## v0.29.0 (2023-03-12)
### Feature
* **action:** Allow defining action as list of commands ([`fcc20f1`](https://github.com/lt-mayonesa/hexagon/commit/fcc20f1f30a9ebfcbaa50d99ab3a7897d7af07ca))

## v0.28.0 (2022-07-18)
### Feature
* **dependencies:** Show status on deps install ([#87](https://github.com/redbeestudios/hexagon/issues/87)) ([`f84d00b`](https://github.com/redbeestudios/hexagon/commit/f84d00b855e6548ec869252075dc0c9b4289457a))

## v0.27.0 (2022-07-18)
### Feature
* **install:** Warn commands dir not in PATH ([#86](https://github.com/redbeestudios/hexagon/issues/86)) ([`9b42bd4`](https://github.com/redbeestudios/hexagon/commit/9b42bd4bc765112e4d799e4c4ca57c128fddbb10))

## v0.26.1 (2022-06-26)
### Fix
* **install-cli:** Only store bin_path if prompted ([`32dbc6c`](https://github.com/redbeestudios/hexagon/commit/32dbc6c0c5081b1a4db589f49e3b5fa8498c9a74))

## v0.26.0 (2022-05-30)
### Feature
* Detect and install dependencies (Python, NodeJS) for CLIs ([#72](https://github.com/redbeestudios/hexagon/issues/72)) ([`febdb38`](https://github.com/redbeestudios/hexagon/commit/febdb383e442a5e3cbc528e2c80729b72b651da4))

## v0.25.1 (2022-05-28)
### Fix
* Print help gaps ([`e130331`](https://github.com/redbeestudios/hexagon/commit/e130331f4e347c57e0bcb246b476063452c15911))

## v0.25.0 (2022-02-25)
### Feature
* **groups:** Allow for inline groups in YAML ([`d29a587`](https://github.com/redbeestudios/hexagon/commit/d29a58748dac4e2a60dc0760d526cf78ed2c1034))

### Fix
* **execute-again:** Show command aliases correctly ([`922e554`](https://github.com/redbeestudios/hexagon/commit/922e5547c214f3819c9159eea174da28c3bd3856))

## v0.24.0 (2022-02-23)
### Feature
* **storage:** Add get_local_config_dir() function ([#79](https://github.com/redbeestudios/hexagon/issues/79)) ([`ec817d2`](https://github.com/redbeestudios/hexagon/commit/ec817d2d4b3bfdd962c6a2dc51216e3b0b53c1ca))

## v0.23.4 (2022-02-23)
### Fix
* **action:** Validate action is valid module identifier ([#78](https://github.com/redbeestudios/hexagon/issues/78)) ([`e583078`](https://github.com/redbeestudios/hexagon/commit/e5830787b96432c2c142f96a5850089c5958ace9))

## v0.23.3 (2022-02-17)
### Fix
* **create-tool:** README lost during package ([#77](https://github.com/redbeestudios/hexagon/issues/77)) ([`b7238cd`](https://github.com/redbeestudios/hexagon/commit/b7238cddbcc07c09e5e20eb10d9e5dd7f396516f))

## v0.23.2 (2022-02-17)
### Fix
* **i18n:** Missing translation strings ([#76](https://github.com/redbeestudios/hexagon/issues/76)) ([`97a1068`](https://github.com/redbeestudios/hexagon/commit/97a1068ec8c4eb771466676a84215a0b458fc84c))

## v0.23.1 (2022-02-08)
### Fix
* **i18n:** Search local and system dirs ([`af62986`](https://github.com/redbeestudios/hexagon/commit/af6298632e78c289f2bf50b855a63a93526efd89))

## v0.23.0 (2022-01-21)
### Feature
* **i18n:** Added EN and ES transltions + CI ([#73](https://github.com/redbeestudios/hexagon/issues/73)) ([`7c65e74`](https://github.com/redbeestudios/hexagon/commit/7c65e740dd74cc7c0e0bdb2ba75587f185d327d2))

## v0.22.1 (2021-12-28)
### Fix
* **yaml:** Print YAML path ([`bfc60ae`](https://github.com/redbeestudios/hexagon/commit/bfc60ae1b60f2664934f999176067dfe374b2015))

### Documentation
* Better resolution gif ([`897eeee`](https://github.com/redbeestudios/hexagon/commit/897eeee4ed1472ab993a36eadd1408161d2a2317))
* Adding gif example to readme ([`e2b4c1b`](https://github.com/redbeestudios/hexagon/commit/e2b4c1ba0e082ec998a63ba497dd627022037c1b))

## v0.22.0 (2021-11-11)
### Feature
* **install-cli:** Use shell scripts instead of aliases ([`c3d7ed7`](https://github.com/redbeestudios/hexagon/commit/c3d7ed76fce7bfae2448554fdb322f777ea5d59d))

## v0.21.1 (2021-11-10)
### Fix
* **alias:** Source new aliases ([#64](https://github.com/redbeestudios/hexagon/issues/64)) ([`c13f59b`](https://github.com/redbeestudios/hexagon/commit/c13f59b454e7c3df45efd3c3267eb0ed32cad1a8))

## v0.21.0 (2021-10-04)
### Feature
* Springboot, react, nextjs seeds ([#63](https://github.com/redbeestudios/hexagon/issues/63)) ([`951b3ab`](https://github.com/redbeestudios/hexagon/commit/951b3ab8df92a5cfccc379c0b8cee824dff16cf2))

## v0.20.0 (2021-09-20)
### Feature
* Plugins and hooks ([#61](https://github.com/redbeestudios/hexagon/issues/61)) ([`b7f1c08`](https://github.com/redbeestudios/hexagon/commit/b7f1c080129c53fcf28db424a0bcca5630e4febd))

## v0.19.2 (2021-09-10)
### Fix
* **analytics:** Switch user_id and client_id scope ([`6718c7c`](https://github.com/redbeestudios/hexagon/commit/6718c7cb94c8a2693d795cfc97339bf6dd9a6678))

## v0.19.1 (2021-09-10)
### Fix
* **analytics:** Register user_id and client_id ([`18a621e`](https://github.com/redbeestudios/hexagon/commit/18a621ed1b6998644ff5bcdb59218393fc7e726f))

## v0.19.0 (2021-09-07)
### Feature
* **analytics:** Log and send hexagon usage events ([#57](https://github.com/redbeestudios/hexagon/issues/57)) ([`c096900`](https://github.com/redbeestudios/hexagon/commit/c0969009862e1763ac79d5f5c82d5ee110f4ec88))

## v0.18.0 (2021-08-27)
### Feature
* Options by env variables, local options file or defaults ([#52](https://github.com/redbeestudios/hexagon/issues/52)) ([`6687b94`](https://github.com/redbeestudios/hexagon/commit/6687b94a53723f56fb683d53ad26c1a64dd3d025))

## v0.17.0 (2021-08-27)
### Feature
* Nested tools, for grouping and organizing ([#54](https://github.com/redbeestudios/hexagon/issues/54)) ([`b5831fd`](https://github.com/redbeestudios/hexagon/commit/b5831fdc4f69a6765973f1f5ce1a41ea58d8218c))

## v0.16.0 (2021-08-24)
### Feature
* Auto-update for clis ([#49](https://github.com/redbeestudios/hexagon/issues/49)) ([`a03d3e0`](https://github.com/redbeestudios/hexagon/commit/a03d3e00c27a39e72298e3f5979711162ded6f1d))

## v0.15.1 (2021-08-20)
### Fix
* Changelog in hexagon update ([#48](https://github.com/redbeestudios/hexagon/issues/48)) ([`c6ab57d`](https://github.com/redbeestudios/hexagon/commit/c6ab57de27d3d0f8d4d441e198f273b0cd204554))

## v0.15.0 (2021-07-26)
### Feature
* **execute:** Display action errors nicely to user ([#43](https://github.com/redbeestudios/hexagon/issues/43)) ([`b8ab97f`](https://github.com/redbeestudios/hexagon/commit/b8ab97f377bb10fe7c5533c5bbdbbd19938a74b1))

## v0.14.2 (2021-07-23)
### Fix
* Added packaging to dependencies ([#44](https://github.com/redbeestudios/hexagon/issues/44)) ([`6b5ddec`](https://github.com/redbeestudios/hexagon/commit/6b5ddec86d53ca0f8d64f3f3938f959a084ae375))

## v0.14.1 (2021-07-21)
### Fix
* Hexagon auto-update ([#42](https://github.com/redbeestudios/hexagon/issues/42)) ([`2720c6a`](https://github.com/redbeestudios/hexagon/commit/2720c6a1d1e1a2ecb2682244702a3b313a1a9a0d))

## v0.14.0 (2021-07-20)
### Feature
* **updates:** Hexagon auto update ([#35](https://github.com/redbeestudios/hexagon/issues/35)) ([`16b93ff`](https://github.com/redbeestudios/hexagon/commit/16b93ffab29aa817c22b4a9b06e6dda43cc54fc7))

## v0.13.5 (2021-07-20)
### Fix
* **execute:** Use subprocess shell=True ([#38](https://github.com/redbeestudios/hexagon/issues/38)) ([`6d5e1e8`](https://github.com/redbeestudios/hexagon/commit/6d5e1e8e2e6ce62ca15acbf9d002d3ae6d0881ef))

## v0.13.4 (2021-07-19)
### Fix
* **yaml:** Handle error for None values ([`33300c6`](https://github.com/redbeestudios/hexagon/commit/33300c6463ab7f0accdccf0b46ed7fb96be64ac4))

## v0.13.3 (2021-07-17)
### Fix
* Simplify always true cli.command ([`c72de85`](https://github.com/redbeestudios/hexagon/commit/c72de855b7f8a0e236a9ea100d0e2662f8d90895))

## v0.13.2 (2021-07-17)
### Fix
* **last-command:** Store last command whe tool executed directly ([`1f6c887`](https://github.com/redbeestudios/hexagon/commit/1f6c8875317245b599b18063420650277d9d27b8))

## v0.13.1 (2021-07-13)
### Fix
* **help:** Help expecting dict crashes ([`cf86f99`](https://github.com/redbeestudios/hexagon/commit/cf86f99c56e9c5a4affe426021b3230ef342d99f))

## v0.13.0 (2021-07-13)
### Feature
* **yaml:** Show a more precise error to users ([#27](https://github.com/redbeestudios/hexagon/issues/27)) ([`b635964`](https://github.com/redbeestudios/hexagon/commit/b635964789a54006f3f3b4dc31196940487b687f))

## v0.12.0 (2021-07-12)
### Feature
* Define tools & envs as lists ([#26](https://github.com/redbeestudios/hexagon/issues/26)) ([`4db03b4`](https://github.com/redbeestudios/hexagon/commit/4db03b4e279bf2c82f6c9e8af8265026ea6e25c6))

## v0.11.0 (2021-07-10)
### Feature
* **domain:** Map YAML to pydantic BaseModel ([#24](https://github.com/redbeestudios/hexagon/issues/24)) ([`727a09a`](https://github.com/redbeestudios/hexagon/commit/727a09a01f11c34b1225fdcab609b02b2ffbff09))

## v0.10.0 (2021-07-08)
### Feature
* **execute:** Command actions, closes #22 ([#23](https://github.com/redbeestudios/hexagon/issues/23)) ([`26a9e05`](https://github.com/redbeestudios/hexagon/commit/26a9e051b497354c55177398f95ef98b0b4149bb))

## v0.9.0 (2021-07-07)
### Feature
* **support:** Storage api, closes #17 ([#21](https://github.com/redbeestudios/hexagon/issues/21)) ([`f8cc5b3`](https://github.com/redbeestudios/hexagon/commit/f8cc5b374df56c084c2b1cc48ba0a35c44c6a46e))

## v0.8.2 (2021-07-03)
### Fix
* **execute:** Pass env object correctly ([`86bbc68`](https://github.com/redbeestudios/hexagon/commit/86bbc689001339f0bfc128b25520244ed7f966ec))

## v0.8.1 (2021-07-02)


## v0.8.0 (2021-07-01)
### Feature
* **styles:** Basic support for hexagon themes ([#14](https://github.com/redbeestudios/hexagon/issues/14)) ([`b5dd966`](https://github.com/redbeestudios/hexagon/commit/b5dd966a221cab477e33adec27fb54fdfc6efefb))

### Documentation
* English, slogan, and reference to template repo ([`9a9fc96`](https://github.com/redbeestudios/hexagon/commit/9a9fc96f42d4ea81a57bda822de7c098d31015a6))

## v0.7.6 (2021-06-25)
### Fix
* **create-tool:** __templates dir and custom tools path ([#9](https://github.com/redbeestudios/hexagon/issues/9)) ([`5ebde69`](https://github.com/redbeestudios/hexagon/commit/5ebde697b840e5da0ea62341ef22831ecc53a50d))

## v0.7.5 (2021-06-25)
### Fix
* **save-alias:** Bash on fresh install ([#8](https://github.com/redbeestudios/hexagon/issues/8)) ([`1754d2c`](https://github.com/redbeestudios/hexagon/commit/1754d2c02fde3231a142bc2fa51c344eef390e37))

## v0.7.4 (2021-06-23)
### Fix
* **create-tool:** Templates directory not published ([`0f1e85c`](https://github.com/redbeestudios/hexagon/commit/0f1e85c45969d1f1f5cd7ab9dbb0b4018f9a8243))

## v0.7.3 (2021-06-22)
### Fix
* **tracer:** Do not print alias for internal tools ([`5d798fe`](https://github.com/redbeestudios/hexagon/commit/5d798fe1d49b12b36bcf74decc1765468c888422))

## v0.7.2 (2021-06-19)
### Fix
* **save-alias:** Create aliases file if does not exist ([`9055055`](https://github.com/redbeestudios/hexagon/commit/9055055c8def45fc1b84c5b13388be50e259f86a))

### Documentation
* Yaml example in readme ([`86c28d1`](https://github.com/redbeestudios/hexagon/commit/86c28d126535e3fb6cd229b623666666aa0e1bd3))

## v0.7.1 (2021-06-17)
### Fix
* **execute:** Run install_cli and other internal tools ([#2](https://github.com/redbeestudios/hexagon/issues/2)) ([`71cc90b`](https://github.com/redbeestudios/hexagon/commit/71cc90b9493332825f78163854422db5d2ec493d))

## v0.7.0 (2021-06-17)
### Feature
* **execute:** Execute action with extension ([`fe622a8`](https://github.com/redbeestudios/hexagon/commit/fe622a8942d91eb3c2f5c9cbe88d1aac22f1ea0f))

## v0.6.0 (2021-06-16)
### Feature
* **internal-tools:** Create a new tool ([`dfc13aa`](https://github.com/redbeestudios/hexagon/commit/dfc13aacf77ec17ba735a519dd4bfbce29047731))

### Fix
* **wax:** Make classifier optional ([`4e8ff5b`](https://github.com/redbeestudios/hexagon/commit/4e8ff5bce035883b49a21f062c4a543529983f69))
* **create-tool:** Change ordering of YAML key insert ([`1ce6024`](https://github.com/redbeestudios/hexagon/commit/1ce6024b06f6b6cfbf0b0af8db6d6703a79efd35))
* **help:** Support tools with no long_name ([`46c0f89`](https://github.com/redbeestudios/hexagon/commit/46c0f896dfb63288b3662b8d08499c6c66998b47))
* **wax:** Show classifier when no long_name ([`bc8a485`](https://github.com/redbeestudios/hexagon/commit/bc8a485ced377d6ddd78ae7617a6fc1f6d2ad889))
* **execute:** Fail with custom message when action not found ([`5ea46f2`](https://github.com/redbeestudios/hexagon/commit/5ea46f21aa69dfd5de615d67ac823034b6854ac4))

## v0.5.0 (2021-06-12)
### Feature
* **config:** Only show install cli when no config ([`9413f99`](https://github.com/redbeestudios/hexagon/commit/9413f99ffa23f562f68acddfe99c73e817e74e3e))

### Fix
* Allow for tools with no alias ([`eb25e89`](https://github.com/redbeestudios/hexagon/commit/eb25e8976581bc9f39852b93444c91b6a074210f))

## v0.4.1 (2021-06-11)
### Fix
* **install:** Wrong action definition for tool install ([`425dfd3`](https://github.com/redbeestudios/hexagon/commit/425dfd349da6c60361ef69839752126632c67bd7))

## v0.4.0 (2021-06-11)
### Feature
* **config:** Custom tools dir relative to YAML ([`fe3e26b`](https://github.com/redbeestudios/hexagon/commit/fe3e26bd3598ece02e9fd06ae4397b14edce6947))

## v0.3.0 (2021-06-11)
### Feature
* **prompt:** Sort tools by type ([`ef71eae`](https://github.com/redbeestudios/hexagon/commit/ef71eae1e2b5bb0b7b996efa5a1c694b52f31235))
* **custom-tool:** Allow projects to register custom tools ([`1cac9ca`](https://github.com/redbeestudios/hexagon/commit/1cac9ca80e369f9c05c1dcc3363386d4af0d6828))

### Documentation
* **release:** Correct regex for README version ([`f9b973a`](https://github.com/redbeestudios/hexagon/commit/f9b973a514efc0370a32d5b95a515ed461a508c2))

## v0.2.0 (2021-06-10)
### Feature
* Handle keyboard interrupt gracefully ([`a65daa2`](https://github.com/redbeestudios/hexagon/commit/a65daa26c3de305a2bacafe7f7a64f9295914c94))
* **install:** Install custom cli from YAML ([`cb25d68`](https://github.com/redbeestudios/hexagon/commit/cb25d680fa2af6448a79e61631542dabc08991a9))

### Documentation
* Basic readme content ([`7a82b34`](https://github.com/redbeestudios/hexagon/commit/7a82b3490f2b112c9a35fad4a789de1d2341ad69))

## v0.1.0 (2021-06-06)
### Feature
* **envs:** Make tool.envs optional ([`efeec06`](https://github.com/redbeestudios/hexagon/commit/efeec064404830ca33c6b4751f55455190c6b9e2))

## v0.0.6 (2021-06-06)
### Fix
* **help:** Optional alias ([`3cf1f6a`](https://github.com/redbeestudios/hexagon/commit/3cf1f6a46276468fc7a9ae5bbb4445ff4f544d11))

### Documentation
* **release:** Version update comment ([`c6a9617`](https://github.com/redbeestudios/hexagon/commit/c6a9617e7943adef2095b1a768548c8692cefd67))
