# Changelog

<!--next-version-placeholder-->

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
